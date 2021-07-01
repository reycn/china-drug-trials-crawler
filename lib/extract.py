import re
import time

import pandas as pd
from lxml import etree
from termcolor import cprint

from lib.df import save_df
from lib.text import main_researchers as mr
from lib.text import remove_spaces as rms
from lib.text import tbody_to_json as tj

# from df import save_df
# from text import tbody_to_json as tj
# from text import remove_spaces as rms
# from text import main_researchers as mr

HEAD = [
    'ID', '实验数据ID', '实验数据获取时间', '登记号1', '试验状态', '申请人联系人', '首次公示信息日期', '申请人名称',
    '登记号2', '相关登记号', '药物名称', '药物类型', '临床申请受理号', '适应症', '试验专业题目', '试验通俗题目',
    '试验方案编号', '方案最新版本号', '版本日期', '方案是否为联合用药', '申请人名称', '联系人姓名', '联系人座机',
    '联系人手机号', '联系人Email', '联系人邮政地址', '联系人邮编', '试验目的', '试验分类', '试验分期', '设计类型',
    '随机化', '盲法', '试验范围', '受试者年龄', '受试者性别', '健康受试者', '受试者入选标准', '受试者排除标准',
    '试验药', '对照药', '主要终点指标及评价时间', '次要终点指标及评价时间', '数据安全监查委员会DMC', '为受试者购买试验伤害保险',
    '主要研究者信息', '各参加机构信息', '伦理委员会信息', '试验状态', '试验人数', '受试者招募及试验完成日期',
    ' 临床试验结果摘要'
]


def xp(slc, exp: str) -> str:
    '''Extract by XPATH'''
    text = slc.xpath(exp)[0].text
    if text and (text != ''):
        text = text.replace('\n', '')
        text = re.sub(r's+', ' ', text)
        return text.strip()
    else:
        return ''


def ref(exp, html: str) -> str:
    '''Extract by regex pattern'''
    text = re.findall(exp, html)
    if text:
        return text[0].strip()
    else:
        return ''


def extract_info(html: str, trial_id: str, trial_id_hash: str) -> dict:
    '''Extract information from HTML strings'''
    # cprint('Extracting details...', 'white', 'on_blue')
    slc = etree.HTML(html)
    try:
        ## Data date
        srcdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        ## Basic info
        regid = xp(slc, '//*[@id="collapseOne"]/div/table/tbody/tr[1]/td[1]')
        status = xp(slc, '//*[@id="collapseOne"]/div/table/tbody/tr[1]/td[2]')
        contact = xp(slc, '//*[@id="collapseOne"]/div/table/tbody/tr[2]/td[1]')
        pubdate = xp(slc, '//*[@id="collapseOne"]/div/table/tbody/tr[2]/td[2]')
        regstor = xp(slc, '//*[@id="collapseOne"]/div/table/tbody/tr[3]/td')
        # print(scrdate, regid, status, contact, pubdate, regstor)

        # ## Title and background
        regno = xp(slc, '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[1]/td')
        relno = xp(slc, '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[2]/td')
        medname = rms(
            xp(slc, '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[3]/td'))
        medtype = xp(slc, '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[4]/td')
        recordno = xp(slc,
                      '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[5]/td')
        # print(regno, relno, medname, medtype, recordno)

        indic = xp(slc, '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[6]/td')
        protitle = xp(slc,
                      '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[7]/td')
        comtitle = xp(slc,
                      '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[8]/td')
        planno = xp(slc,
                    '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[9]/td[1]')
        planver = xp(slc,
                     '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[9]/td[2]')
        verdate = xp(slc,
                     '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[10]/td[1]')
        united = xp(slc,
                    '//*[@id="collapseTwo"]/div/table[1]/tbody/tr[10]/td[2]')
        # print(indic, protitle, comtitle, planno, planveaaar, verdate, united)

        ## Registrators
        regname = ref(
            r'申请人名称<\/th>[\w\W]*<td colspan=\"[0-9]*\">([\w\W]*)<\/td>[\w\W]*公示的试验信息',
            html)
        # print(regname)
        contname = xp(slc,
                      '//*[@id="collapseTwo"]/div/table[2]/tbody/tr[2]/td[1]')
        contfixed = xp(
            slc, '//*[@id="collapseTwo"]/div/table[2]/tbody/tr[2]/td[2]')
        contmobile = xp(
            slc, '//*[@id="collapseTwo"]/div/table[2]/tbody/tr[2]/td[3]')
        contemail = xp(
            slc, '//*[@id="collapseTwo"]/div/table[2]/tbody/tr[3]/td[1]')
        contaddr = xp(slc,
                      '//*[@id="collapseTwo"]/div/table[2]/tbody/tr[3]/td[2]')
        contzip = xp(slc,
                     '//*[@id="collapseTwo"]/div/table[2]/tbody/tr[3]/td[3]')

        # print(regname, contname, contfixed, contmobile, contemail, contaddr,
        #       contzip)

        ## Clinical trial
        cltpps = ref(r"1、试验目的</div>\n(.*)", html)
        clttype = xp(slc,
                     '//*[@id="collapseTwo"]/div/table[3]/tbody/tr[1]/td[1]')
        cltpart = rms(
            xp(slc, '//*[@id="collapseTwo"]/div/table[3]/tbody/tr[1]/td[2]'))
        cltclass = xp(slc,
                      '//*[@id="collapseTwo"]/div/table[3]/tbody/tr[1]/td[3]')
        cltrandom = xp(
            slc, '//*[@id="collapseTwo"]/div/table[3]/tbody/tr[2]/td[1]')
        cltblind = xp(slc,
                      '//*[@id="collapseTwo"]/div/table[3]/tbody/tr[2]/td[2]')
        cltrange = xp(slc,
                      '//*[@id="collapseTwo"]/div/table[3]/tbody/tr[2]/td[3]')
        # print(cltpps, clttype, cltpart, cltclass, cltrandom, cltblind,
        #   cltrange)

        ## Subjects
        subage = rms(
            xp(slc, '//*[@id="collapseTwo"]/div/table[4]/tbody/tr[1]/td'))
        subsex = xp(slc, '//*[@id="collapseTwo"]/div/table[4]/tbody/tr[2]/td')
        subheal = xp(slc, '//*[@id="collapseTwo"]/div/table[4]/tbody/tr[3]/td')
        subin = tj(
            ref(
                '<th>入选标准<\/th>[\w\W]*(<tbody><tr>[\w\W]*<\/tbody>)[\w\W]*<th>排除标准<\/th>',
                html))
        subex = tj(
            ref(
                '<th>排除标准<\/th>[\w\W]*(<tbody><tr>[\w\W]*<\/tbody>)[\w\W]*4、试验分组<\/div>',
                html))
        grpint = tj(ref(
            '试验药<\/th>[\w\W]*(<tbody>[\w\W]*<\/tbody>)[\w\W]*对照药<\/th>', html),
                    vertical=True)
        grpcomp = tj(ref(
            '对照药<\/th>[\w\W]*(<tbody>[\w\W]*<\/tbody>)[\w\W]*5、终点指标<\/div>',
            html),
                     vertical=True)
        pind = tj(ref(
            '主要终点指标及评价时间<\/th>[\w\W]*(<tbody>[\w\W]*<\/tbody>)[\w\W]*次要终点指标及评价时间<\/th>',
            html),
                  vertical=True)
        sind = tj(ref(
            '次要终点指标及评价时间<\/th>[\w\W]*(<tbody>[\w\W]*<\/tbody>)[\w\W]*6、数据安全监查委员会（DMC）',
            html),
                  vertical=True)
        dmc = ref(
            r'6、数据安全监查委员会（DMC）[\w\W]*<\/div>([\w\W]*)<div[\w\W]*7、为受试者购买试验伤害保险',
            html)
        ins = ref(r'7、为受试者购买试验伤害保险[\w\W]*<\/div>([\w\W]*)<div[\w\W]*四、研究者信息',
                  html)
        # print(subage, subsex, subheal, subin, subex, grpint, grpcomp, pind,
        #       sind, dmc, ins)
        ## Researchers
        prim = mr(
            ref(
                '1、主要研究者信息[\w\W]*(<tbody><tr>[\w\W]*<\/tbody>)[\w\W]*2、各参加机构信息',
                html))

        inst = tj(ref(
            '2、各参加机构信息[\w\W]*(<tbody><tr>[\w\W]*<\/tbody>)[\w\W]*五、伦理委员会信息',
            html),
                  vertical=True)
        ethic = tj(ref(
            '五、伦理委员会信息[\w\W]*(<tbody><tr>[\w\W]*<\/tbody>)[\w\W]*六、试验状态信息',
            html),
                   vertical=True)
        ## Trial status
        tristatus = rms(
            ref(r'1、试验状态[\w\W]*<\/div>([\w\W]*)<div[\w\W]*2、试验人数', html))
        tripop = tj(
            ref(
                '2、试验人数[\w\W]*(<tbody><tr>[\w\W]*<\/tbody>)[\w\W]*3、受试者招募及试验完成日期',
                html))
        trirecru = tj(
            ref(
                '3、受试者招募及试验完成日期[\w\W]*(<tbody><tr>[\w\W]*<\/tbody>)[\w\W]*七、临床试验结果摘要',
                html))
        triresult = tj(ref(
            '七、临床试验结果摘要[\w\W]*(<tbody><tr>[\w\W]*<\/tbody>)[\w\W]*<\/table>',
            html),
                       vertical=True)
        # print(trial_id, prim, inst, ethic, tristatus, tripop, trirecru,
        #       triresult)
        return (info_to_dict(
            trial_id, trial_id_hash, srcdate, regid, status, contact, pubdate,
            regstor, regno, relno, medname, medtype, recordno, indic, protitle,
            comtitle, planno, planver, verdate, united, regname, contname,
            contfixed, contmobile, contemail, contaddr, contzip, cltpps,
            clttype, cltpart, cltclass, cltrandom, cltblind, cltrange, subage,
            subsex, subheal, subin, subex, grpint, grpcomp, pind, sind, dmc,
            ins, prim, inst, ethic, tristatus, tripop, trirecru, triresult))
    except Exception as e:
        cprint(f'Selecting failed: {e}', 'white', 'on_yellow')
        pass


def info_to_dict(trial_id: str, trial_id_hash: str, srcdate: str, regid: str,
                 status: str, contact: str, pubdate: str, regstor: str,
                 regno: str, relno: str, medname: str, medtype: str,
                 recordno: str, indic: str, protitle: str, comtitle: str,
                 planno: str, planver: str, verdate: str, united: str,
                 regname: str, contname: str, contfixed: str, contmobile: str,
                 contemail: str, contaddr: str, contzip: str, cltpps: str,
                 clttype: str, cltpart: str, cltclass: str, cltrandom: str,
                 cltblind: str, cltrange: str, subage: str, subsex: str,
                 subheal: str, subin: str, subex: str, grpint: str,
                 grpcomp: str, pind: str, sind: str, dmc: str, ins: str,
                 prim: str, inst: str, ethic: str, tristatus: str, tripop: str,
                 trirecru: str, triresult: str) -> dict:
    '''Convert seperated information into a dict'''
    value = [
        trial_id, trial_id_hash, srcdate, regid, status, contact, pubdate,
        regstor, regno, relno, medname, medtype, recordno, indic, protitle,
        comtitle, planno, planver, verdate, united, regname, contname,
        contfixed, contmobile, contemail, contaddr, contzip, cltpps, clttype,
        cltpart, cltclass, cltrandom, cltblind, cltrange, subage, subsex,
        subheal, subin, subex, grpint, grpcomp, pind, sind, dmc, ins, prim,
        inst, ethic, tristatus, tripop, trirecru, triresult
    ]
    dictionary = {}
    for i in range(0, len(HEAD)):
        dictionary[HEAD[i]] = value[i]
    print(str(dictionary)[:200] + '...')
    return dictionary


if __name__ == '__main__':
    '''Default function / testing function'''
    with open('./content/detail.html') as f:
        html = f.read()
        df = pd.DataFrame(columns=HEAD)
        dct = extract_info(html, 'CTR20211247', 'asdfasdfasdfasdf')
        df = df.append(dct, ignore_index=True)
        save_df(df)
        print(df)
