import os
import pandas as pd


def func_concat(folder_path):
    df_list = []
    allRows = 0
    # 遍历文件夹中的所有文件
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        # 使用 Pandas 读取 CSV 文件
        df = pd.read_csv(file_path)
        # 计算行数
        num_rows = df.shape[0]
        allRows = allRows + num_rows
        print(file, "Total number of rows:", num_rows)
        df_list.append(df)

    print(f'正在合并中...{folder_path}理论行数为：{allRows}')
    # 沿着列方向合并四个 DataFrame
    result = pd.concat(df_list, axis=0, ignore_index=True)
    num_rows = result.shape[0]
    print(f'合并完成，{folder_path}行数为:{num_rows}')
    return result
