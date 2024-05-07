import pandas as pd

# 读取 CSV 文件
df = pd.read_csv("D:\\Desktop\\data\\dataFeature\\partShpDataFeature\\dataFeature_Part.csv")
num_rows = df.shape[0]
print(f'重置前行数为：{num_rows}')
# 根据'name'列去除重复项，保留第一个出现的值
df.drop_duplicates(subset='uid', keep='first', inplace=True)

# 重置索引
df.reset_index(drop=True, inplace=True)
num_rows = df.shape[0]
print(f'重置后行数为：{num_rows}')
df.to_csv('D:\\Desktop\\data\\dataFeature\\partShpDataFeature\\dataFeature_Part_drop.csv', index=False)
