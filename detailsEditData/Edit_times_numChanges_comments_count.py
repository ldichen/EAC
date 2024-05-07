import pandas as pd

def func_EditTimes(df_Uid,df_All):
    # 排序
    df_sort_Uid = df_Uid.sort_values(by='uid')

    df_sort_Uid['EditTimes'] = 0
    df_sort_Uid['num_changes'] = 0  #
    df_sort_Uid['comments_count'] = 0  #
    # 使用for循环逐行读取特定列
    for index, row in df_sort_Uid.iterrows():
        # 开始对每个id进行计算
        uid = row['uid']
        # 当前id的所有行
        specific_rows = df_All[df_All['uid'] == uid]
        #用户总编辑次数
        max_Times = specific_rows['changesets_count'].max()
        num_rows = len(specific_rows)
        trueValue = max(int(max_Times),num_rows )
        df_sort_Uid.at[index, 'EditTimes'] = trueValue
        print(f"用户{uid}总编辑次数：{trueValue}")
        #总结点变更数
        sum_numChange = specific_rows['num_changes'].sum()
        df_sort_Uid.at[index, 'num_changes'] = int(sum_numChange)
        # print(f"用户{uid}总结点变更数：{int(sum_numChange)}")
        #总评论数
        sum_commentsCount = specific_rows['comments_count'].sum()
        df_sort_Uid.at[index, 'comments_count'] = int(sum_commentsCount)
        # print(f"用户{uid}总评论数：{int(sum_commentsCount)}")
    return df_sort_Uid