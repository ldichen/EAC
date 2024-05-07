import pandas as pd

# 读取 CSV 文件
df = pd.read_csv("D:\\Desktop\\data\\dataFeature\\partShpDataFeature\\dataFeature_Part_drop.csv")

# 将日期列转换为时间戳格式
df['Registered_timeStamp'] = pd.to_datetime(df['Registered'], errors='coerce').astype('int64') // 10**9

# 打印出无法解析的日期
print("无法解析的日期:")
print(df[df['Registered'].isna()])

# 显示转换后的数据框的部分内容
print("\n转换后的数据:")
print(df['Registered'].head(5))

df.to_csv("D:\\Desktop\\data\\dataFeature\\partShpDataFeature\\dataFeature_Part_drop_timestamp.csv",index=False)

