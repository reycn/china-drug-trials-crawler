import json
import re

from bs4 import BeautifulSoup


def remove_spaces(text: str) -> str:
    '''Delete unnecessary spaces in web formatting'''
    result = re.sub(r'\s\s*', '\n', text)
    return result


def tbody_to_json(html_doc: str, vertical: bool = False) -> str:
    '''Extract a <tbody></tbody> within a table to json'''
    soup = BeautifulSoup(html_doc, 'html.parser')
    try:
        if not vertical:
            trs = soup.find_all('tr')
            result = {}
            for tr in trs:
                if tr.th:
                    result[tr.th.string.strip()] = tr.td.string.strip()
                else:
                    result[tr.find_all('td')[0].string.strip()] = tr.find_all(
                        'td')[1].string.strip()
        else:
            trs = soup.find_all('tr')
            head = [col.string.strip() for col in trs[0].find_all('th')]
            result = {}
            for i in range(1, len(trs)):
                cases = trs[i].find_all('td')
                if len(cases) <= 1:
                    result = {"Error": "申请人未填写或遇到未知错误"}
                else:
                    result[i - 1] = {}
                    for j in range(1, len(head)):
                        result[i - 1][head[j]] = remove_spaces(
                            cases[j].get_text().strip())
        result = dict_to_json(result)
        return result
    except Exception as e:
        return {"Error": f"{e}"}


def main_researchers(html_doc: str) -> str:
    '''Extract the core researcher'''
    soup = BeautifulSoup(html_doc, 'html.parser')
    try:
        trs = soup.find_all('tr')[:3]  # only the first one
        head = []
        values = []
        for tr in trs:
            for h in tr.find_all('th'):
                head.append(h.string.strip())
            for d in tr.find_all('td'):
                values.append(d.string.strip())
        head = head[1:]
        result = {}
        for i in range(len(head)):
            result[head[i]] = values[i]
        # print(head)
        # print(values)
        result = dict_to_json(result)
        return result
    except Exception as e:
        return {"Error": f"{e}"}


def dict_to_json(dict_str: str) -> str:
    '''Convert a dict to json'''
    json_str = json.dumps(dict_str, ensure_ascii=False)
    return json_str


if __name__ == '__main__':
    '''Default function / testing function'''
    tbody = '''<tbody><tr>
                                <th width="15%">目标入组人数</th>
                                <td width="85%">

                                        国内:&nbsp;24&nbsp;；
                                </td>
                            </tr>
                            <tr>
                                <th width="15%">已入组人数</th>
                                <td width="85%">
                                        国内:&nbsp;登记人暂未填写该信息；
                                </td>
                            </tr>
                            <tr>
                                <th>实际入组总人数</th>
                                <td>
                                        国内:&nbsp;登记人暂未填写该信息；
                                </td>
                            </tr>
                        </tbody>'''
    tbody2 = '''<tbody><tr>
                                            <td width="10%">
                                            1
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            能够签署知情同意书，对试验内容、过程及可能出现的不良反应充分了解，并能够按照方案要求完成研究的受试者。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            2
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            受试者愿意从签署知情同意书至最后一次给药后3个月内无妊娠计划且自愿采取充分的避孕措施（如正确使用避孕套、绝对禁欲、宫内节育器、已证实无精的输精管结扎等）。 1） 完成血样采集之前，不可采用口服避孕药、避孕针、皮下埋植等化学避孕法。 2） 完成血样采集之后，受试者可以采用物理避孕法或化学避孕法。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            3
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            筛选时年龄不低于18周岁的男性和女性健康志愿者（包括18周岁）。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            4
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            筛选时男性受试者体重不低于50公斤，女性受试者体重不低于45公斤。体重指数（BMI）=体重(kg)/身高2（m2），体重指数在19.0~26.0 kg/m2范围内（包括临界值）。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            5
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            受试者既往体健，或研究者基于临床判断及药品特性综合考量，判断受试者的既往病史不影响参与此项临床研究。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            6
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            筛选时实验室检查、体格检查、正位胸部X片检查和心电图检查经研究者判断为正常或异常无临床意义者。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            7
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            生命体征检测正常或经研究者判断异常无临床意义者。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            8
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            同意首次给药前48小时内至PK采血结束期间不吸烟。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            9
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            同意签署知情同意书之后至PK采血结束期间不服用葡萄柚或含有葡萄柚成分的产品，以及不进行剧烈运动。
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="10%">
                                            10
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            同意首次给药前24小时内至试验结束期间不食用含酒精、巧克力、咖啡因、罂粟籽的制品。
                                            </td>
                                        </tr>
                                    </tbody>'''
    tbodyv = '''<tbody><tr>
            <th width="10%">序号</th>
            <th width="35%">指标</th>
            <th width="35%">评价时间</th>
            <th width="20%">终点指标选择</th>
            </tr>
            <tr>
            <td>1</td>
            <td>Tmax、kel (λz)、T1/2、%AUCex</td>
            <td>给药后48小时</td>
            <td>
            有效性指标
                                                </td>
            </tr>
            <tr>
            <td>2</td>
            <td>实验室检查指标、生命体征测量、心电图检查、体格检查和不良事件。</td>
            <td>入组后至试验结束</td>
            <td>
            有效性指标+安全性指标
                                                </td>
            </tr>
            </tbody>'''

    tbodyv2 = """<tbody><tr>
                <th width="10%">序号</th>
                <th width="40%">名称</th>
                <th width="50%">用法</th>
                </tr>
                <tr>
                <td>
                1
                </td>
                <td>
                中文通用名:利伐沙班片<br>
                英文通用名:Rivaroxaban Tablets<br>
                商品名称:NA
                </td>
                <td>
                剂型:片剂<br>
                规格:20mg<br>
                用法用量:餐后条件下口服，每周期1次，每次一片（20mg），共四周期<br>
                用药时程:单次给药、7天为一个给药周期，共给药4个周期
                </td>
                </tr>
                </tbody>"""
    # result = tbody_to_json(tbody2, vertical=False)
    result = tbody_to_json(tbodyv2, vertical=True)
    result = tbody_to_json(tbodyv, vertical=True)
    # print(result)
