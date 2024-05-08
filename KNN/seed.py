import pandas as pd

# 假设 data 是一个 DataFrame，每列是一个特征
# 例如：data = pd.DataFrame({'feature1': [1, 4, 7], 'feature2': [2, 5, 8], 'feature3': [3, 6, 9]})
csv_file_path = "E:\\Download\\seeds\\seeds_dataset.txt"
data = pd.read_csv(csv_file_path,sep='\s+', header=None)
# 复制原始 DataFrame
data_copy = data.copy()

# 对副本中的前 5 列数据减去 0.1
data_copy.iloc[:, :5] -= 0.1

# 合并副本到原始 DataFrame 中
data_combined = pd.concat([data, data_copy], axis=0)

# 复制原始 DataFrame
data_copy2 = data.copy()

# 对副本中的前 5 列数据减去 0.1
data_copy2.iloc[:, :5] -= 0.05
# 合并副本到原始 DataFrame 中
data_combined2 = pd.concat([data_combined, data_copy2], axis=0)
data_copydata_copy = data_combined2.copy()
data_combined3 = pd.concat([data_combined2, data_copydata_copy.iloc[:, :5]], axis=1)
data_combined3 = pd.concat([data_combined3, data_copydata_copy.iloc[:, :5]], axis=1)
# 将合并后的数据保存为 CSV 文件
data_combined3.to_csv('E:\\Download\\seeds\\seeds_dataset2.txt', index=False)