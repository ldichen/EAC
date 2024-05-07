import arcpy
import pandas as pd
import math

df = pd.DataFrame()
df['OSM'] = 0
df['Shape'] = 0.0
df['Position'] = 0.0
df['IsCheck'] = 0
# 定义一个角度（以弧度为单位）
angle_in_radians = math.radians(31.2)
# 计算角度的余弦值
cos_value = math.cos(angle_in_radians)

# 设置工作空间
arcpy.env.workspace = "D:\\Desktop\\data\\gis_osm_gd\\shanghai_1\\shanghai.gdb"
index = 0
# 使用 SearchCursor 读取表格文件
with arcpy.da.SearchCursor('res', ["OSM", "Shape", "Position", "IsCheck"]) as cursor:
    # 遍历每一行记录
    for row in cursor:
        if row[3] == -1:
            continue
        else:
            osm_values = row[0].split(",")
            for value in osm_values:
                df.at[index, 'OSM'] = value
                df.at[index, 'Shape'] = row[1]

                df.at[index, 'Position'] = row[2] * cos_value * 111000
                df.at[index, 'IsCheck'] = row[3]
                index = index + 1
        if index % 1000 == 0:
            print(f'当前{index}')
del cursor
print('准备读写')
# 将 DataFrame 输出为 CSV 文件
output_csv = 'D:\\Desktop\\data\\gis_osm_gd\\shanghai_1\\sh.csv'
df.to_csv(output_csv, index=False)
