import pandas
import pandas as pd

filepath = 'D:\\Desktop\\data\\gis_osm_gd\\shanghai_1\\sh.csv'
df = pd.read_csv(filepath)
# 判断某两列是否有空值
if df[['Shape', 'Position']].isnull().values.any():
    # 删除包含空值的行
    df.dropna(subset=['Shape', 'Position'], inplace=True)
# print(df.groupby('OSM')['Shape'].idxmax())

# 按照'osmid'列进行分组，然后在每个分组中选择'position'列最大的那一行
result_df = df.loc[df.groupby('OSM')['Shape'].idxmax()]
output_csv = 'D:\\Desktop\\data\\gis_osm_gd\\shanghai_1\\unique_sh.csv'
result_df.to_csv(output_csv, index=False)