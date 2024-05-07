import pandas as pd

df = pd.read_csv("D:\\Desktop\\data\\dataFeature\\partShpDataFeature\\dataFeature_Part_drop_timestamp.csv")
# 使用 assign() 方法添加七列
df = df.assign(Sun=0,
               Mon=0,
               Tue=0,
               Wed=0,
               Thu=0,
               Fri=0,
               Sat=0)
# 使用 .str.split() 方法将字符串分割成列表，并存储在新的列中
df[['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']] = df['days'].str.split(',', expand=True)

# 将字符串形式的数字转换为整数
df[['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']] = df[['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']].astype(
    int)

df.drop(columns=['hours','days'], inplace=True)

df.to_csv("D:\\Desktop\\data\\dataFeature\\partShpDataFeature\\dataFeature_Part_drop_weeks.csv", index=False)
