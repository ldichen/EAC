import pandas as pd

# # 读取CSV文件
# df = pd.read_csv('D:\\Desktop\\data2\\mergedUid.csv')
#
# # 获取行数并减去表头行
# num_rows = df.shape[0] - 1
#
# print("除去表头后的行数为:", num_rows)
# columns_to_read = ['created', 'uid', 'num_changes', 'comments_count']


# df = pd.read_csv('D:\\Study\\GraduationThesis\\data\\10000000-19999999\\10000000-19999999.csv')
# df['value'].fillna('', inplace=True)
# specific_value1 = 'zh-CN'  # 替换为你要挑选的特定值
# specific_value2 = 'zh_CN'  # 替换为你要挑选的特定值
# specific_value3 = 'china'  # 替换为你要挑选的特定值
# specific_value4 = 'China'  # 替换为你要挑选的特定值
# specific_rows = df[
#     df['value'].str.contains(specific_value1) | df['value'].str.contains(specific_value2) | df['value'].str.contains(
#         specific_value3)|df['value'].str.contains(specific_value4)]
#
# # 将结果写入新的CSV文件
# specific_rows.to_csv('D:\\Desktop\\data2\\zh-CN1.csv', index=False)
#
# print("写入完成！")

# # 读取CSV文件
# df = pd.read_csv('D:\\Desktop\\data2\\zh-CN1.csv')
#
# # 根据表头为 "id" 的列挑选出唯一的id的所有行
# unique_rows = df.drop_duplicates(subset=['created'])
#
# print(unique_rows)


# 读取 OSM 文件
osm_file = "E:\\Download\\changesets-240219.osm\\changesets-240219.osm"
data = pd.read_csv(osm_file)

# 打印表头
print("表头：")
print(data.columns)
