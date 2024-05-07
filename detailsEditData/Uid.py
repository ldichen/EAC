import pandas as pd
import datetime


def readUidZN(df):
    # 挑选某一列的唯一值
    unique_values_id = df['uid'].unique()
    unique_values_user = df['user'].unique()
    unique_id_df = pd.DataFrame(unique_values_id, columns=['uid']).astype(int)
    # print(unique_id_df)
    unique_user_df = pd.DataFrame(unique_values_user, columns=['user'])
    # print(unique_user_df)
    num_id_rows = unique_id_df.shape[0]
    num_user_rows = unique_user_df.shape[0]
    print(f'id有：{num_id_rows}行,user有：{num_user_rows}行')
    result = pd.concat([unique_id_df, unique_user_df], axis=1, ignore_index=False)
    # print(result)
    return result
