import pandas as pd

def func_soft(df_Uid,df_All):
    # 排序
    df_sort_Uid = df_Uid.sort_values(by='uid')
    df_sort_Uid['software_Skill'] = 0
    # 使用for循环逐行读取特定列
    for index, row in df_sort_Uid.iterrows():
        # 开始对每个id进行计算
        uid = row['uid']
        # 当前id的所有行
        specific_rows = df_All[df_All['uid'] == uid]
        value_counts = specific_rows['created_by'].value_counts()
        print(value_counts)