import pandas as pd
import csv

allRows = 0
# 读取 CSV 文件
df1 = pd.read_csv('D:\\Desktop\\data\\dataFeature\\osmidAndUserId_1.csv')
# 计算行数
num_rows = df1.shape[0]
allRows = allRows + num_rows
print("Total number of rows:", num_rows)
df2 = pd.read_csv('D:\\Desktop\\data\\dataFeature\\osmidAndUserId_2.csv')
# 计算行数
num_rows = df2.shape[0]
allRows = allRows + num_rows
print("Total number of rows:", num_rows)
df3 = pd.read_csv('D:\\Desktop\\data\\dataFeature\\osmidAndUserId_3.csv')
# 计算行数
num_rows = df3.shape[0]
allRows = allRows + num_rows
print("Total number of rows:", num_rows)

print(f'正在合并中...,理论行数为：{allRows}')

result = pd.concat([df1, df2, df3], axis=0, ignore_index=True)
num_rows = result.shape[0]
print(f'合并完成，总行数为:{num_rows}')

# 将结果导出为 CSV 文件
result.to_csv('D:\\Desktop\\data\\dataFeature\\osmidAndUserId_all.csv', index=False)
