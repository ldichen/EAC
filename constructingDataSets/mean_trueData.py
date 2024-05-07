import pandas as pd
import math

filepath = 'D:\\Desktop\\data\\gis_osm_gd\\matchUID\\matchUID_All.csv'
df = pd.read_csv(filepath)

# 删除满足条件的行
df = df[(df['Shape'] >= 0.02) & (df['uid'] != '') & (df['Position'] <= 90) & (df['uid'] != ' ')]

grouped = df.groupby('uid').agg({'Position': 'mean', 'Shape': 'mean'})
# 计算列的最小值和最大值
min_value = grouped['Position'].min()
max_value = grouped['Position'].max()
# 将 groupby 对象转换为 DataFrame，并重置索引
grouped = grouped.reset_index()

# 统计 df中每个 uid 出现的数量
count_df = df.groupby('uid').size().reset_index(name='count')

# 将统计结果合并到 df2 中
grouped = pd.merge(grouped, count_df, on='uid', how='left')

# 创建新的 DataFrame 来存储结果
new_df = pd.DataFrame({
    'uid': grouped['uid'],
    'count':grouped['count'],
    'average_position': grouped['Position'],
    'normalisation_position': (max_value - grouped['Position']) / (max_value - min_value),
    'average_shape': grouped['Shape'],
    'acc': (max_value - grouped['Position']) / (max_value - min_value) * 0.5 + grouped['Shape'] * 0.5
})
sorted_df = new_df.sort_values(by='acc')

sorted_df.loc[(sorted_df['count'] < 10)&(sorted_df['acc'] < 0.7), 'class'] = 0
sorted_df.loc[(sorted_df['count'] < 10)&(sorted_df['acc'] >= 0.7) & (sorted_df['acc'] < 0.95), 'class'] = 1
sorted_df.loc[(sorted_df['count'] < 10)&(sorted_df['acc'] >= 0.95) & (sorted_df['acc'] <= 1), 'class'] = 2

sorted_df.loc[(sorted_df['count'] >= 10)&(sorted_df['count'] < 500)&(sorted_df['acc'] < 0.8), 'class'] = 0
sorted_df.loc[(sorted_df['count'] >= 10)&(sorted_df['count'] < 500)&(sorted_df['acc'] >= 0.8) & (sorted_df['acc'] < 0.95), 'class'] = 1
sorted_df.loc[(sorted_df['count'] >= 10)&(sorted_df['count'] < 500)&(sorted_df['acc'] >= 0.95), 'class'] = 2

sorted_df.loc[(sorted_df['count'] >= 500)&(sorted_df['acc'] < 0.75), 'class'] = 0
sorted_df.loc[(sorted_df['count'] >= 500)&(sorted_df['acc'] >= 0.75) & (sorted_df['acc'] < 0.9), 'class'] = 1
sorted_df.loc[(sorted_df['count'] >= 500)&(sorted_df['acc'] >= 0.9), 'class'] = 2

output_csv = 'D:\\Desktop\\data\\EAC\\trueData\\mean_trueData3.csv'

# 将结果写入新的 CSV 文件
sorted_df.to_csv(output_csv, index=False)
