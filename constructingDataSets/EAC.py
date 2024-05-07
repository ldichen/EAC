import pandas as pd
import numpy as np


filepath1 = 'D:\\Desktop\\data\\EAC\\trueData\\mean_trueData3.csv'
df1 = pd.read_csv(filepath1)
filepath2 = 'D:\\Desktop\\data\\EAC\\EC.csv'
df2 = pd.read_csv(filepath2)
df2 = df2.drop(columns=['user'])
# df2['acc'] = 0.0
# 判断第二个 DataFrame 中的 uid 是否在第一个 DataFrame 中存在
exist_in_df1 = df2['uid'].isin(df1['uid'])
# print(exist_in_df1)
# 保留第一个 DataFrame 中存在的行
result_df2 = df2[exist_in_df1]
# 使用 merge() 函数合并两个 DataFrame，并将 acc 列的值从第一个 DataFrame 写入到第二个 DataFrame
result_df = pd.merge(result_df2, df1[['uid', 'acc','class']], on='uid', how='left')
# print(result_df2)

filtered_rows = result_df[result_df['Map_changes'] > 50000]
uids_greater_than_10 = df1[df1['count'] < 10]['uid']
# # 生成高斯分布数据
# mu = 3  # 平均值
# sigma = 1  # 标准差
# size = len(sorted_df)  # 与 DataFrame 长度相同
# gaussian_data = np.random.normal(mu, sigma, size)
#
# # 将数据限制在 1 到 5 之间
# gaussian_data = np.clip(gaussian_data, 0, 4)
# # 对数据进行四舍五入
# gaussian_data = np.round(gaussian_data)
# # 将数据转换为整数
# gaussian_data = gaussian_data.astype(int)
# # 对数组进行排序
# sorted_arr = np.sort(gaussian_data)[::-1]
# # 添加新列到 DataFrame
# sorted_df['class'] = sorted_arr
# sorted_df.loc[sorted_df['acc'] < 0.5, 'class'] = 0
# sorted_df.loc[(sorted_df['acc'] >= 0.5) & (sorted_df['acc'] < 0.6), 'class'] = 1
# sorted_df.loc[(sorted_df['acc'] >= 0.6) & (sorted_df['acc'] < 0.7), 'class'] = 2
# sorted_df.loc[(sorted_df['acc'] >= 0.7) & (sorted_df['acc'] < 0.8), 'class'] = 3
# sorted_df.loc[(sorted_df['acc'] >= 0.8) & (sorted_df['acc'] < 0.85), 'class'] = 4
# sorted_df.loc[(sorted_df['acc'] >= 0.85) & (sorted_df['acc'] < 0.9), 'class'] = 5
# sorted_df.loc[(sorted_df['acc'] >= 0.9) & (sorted_df['acc'] < 0.95), 'class'] = 6
# sorted_df.loc[(sorted_df['acc'] >= 0.95) & (sorted_df['acc'] < 1), 'class'] = 7
result = filtered_rows[filtered_rows['uid'].isin(uids_greater_than_10)]
# 找出 df2 中 uid 在 df1 中存在的行的索引
indices_to_drop = result_df[result_df['uid'].isin(result['uid'])].index
# 删除这些行
result_df2 = result_df.drop(indices_to_drop)
output_csv = 'D:\\Desktop\\data\\EAC\\EAC3.csv'
result_df2.to_csv(output_csv, index=False)
