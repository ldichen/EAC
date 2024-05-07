import pandas as pd
import datetime

startTime = datetime.datetime.now()
# 读取5个CSV文件

df1 = pd.read_csv('D:\\Desktop\\data2\\unique_values1.csv')
df2 = pd.read_csv('D:\\Desktop\\data2\\unique_values2.csv')
df3 = pd.read_csv('D:\\Desktop\\data2\\unique_values3.csv')
df4 = pd.read_csv('D:\\Desktop\\data2\\unique_values4.csv')
df5 = pd.read_csv('D:\\Desktop\\data2\\unique_values5.csv')
readedTime0 = datetime.datetime.now()
print("已读取", readedTime0 - startTime)
# 合并数据
merged_df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

# 将合并后的数据写入新的CSV文件
merged_df.to_csv('D:\\Desktop\\data2\\mergedUid.csv', index=False)
endTime0 = datetime.datetime.now()
print("已完成", endTime0 - startTime)
