import pandas as pd
#将所有值设置为0，并删除经纬度为0的值

def func_ND(df):
    df.fillna(0, inplace=True)
    # 删除空行
    # 删除包含特定列中值为0的行
    columns_to_check = ['min_lat', 'min_lon', 'max_lat', 'max_lon']
    print("Deleting...")
    df = df[(df[columns_to_check] != 0).all(axis=1)]
    print("Deleted")
    return df
