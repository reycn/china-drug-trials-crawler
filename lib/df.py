import pandas as pd


def save_df(df: pd.DataFrame,
            name: str = 'test.csv',
            path: str = './data/') -> None:
    '''Save this pd.DataFrame to a static file, in csv'''
    df.to_csv(path + name, encoding='utf_8_sig', index=False)


def sort_df(df: pd.DataFrame) -> pd.DataFrame:
    '''Default function / testing function'''
    head = [
        'ID', '实验数据ID', '实验数据获取时间', '登记号1', '试验状态', '申请人联系人', '首次公示信息日期',
        '申请人名称', '登记号2', '相关登记号', '药物名称', '药物类型', '临床申请受理号', '适应症', '试验专业题目',
        '试验通俗题目', '试验方案编号', '方案最新版本号', '版本日期', '方案是否为联合用药', '申请人名称', '联系人姓名',
        '联系人座机', '联系人手机号', '联系人Email', '联系人邮政地址', '联系人邮编', '试验目的', '试验分类',
        '试验分期', '设计类型', '随机化', '盲法', '试验范围', '受试者年龄', '受试者性别', '健康受试者',
        '受试者入选标准', '受试者排除标准', '试验药', '对照药', '主要终点指标及评价时间', '次要终点指标及评价时间',
        '数据安全监查委员会DMC', '为受试者购买试验伤害保险', '主要研究者信息', '各参加机构信息', '伦理委员会信息',
        '试验状态', '试验人数', '受试者招募及试验完成日期', ' 临床试验结果摘要'
    ]
    df = df[head]
    df = df.sort_values(ascending=True, by='ID')
    return df
