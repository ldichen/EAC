import arcpy
import pandas as pd
import math

arcpy.env.workspace = "D:\\Desktop\\data\\gis_osm_gd\\beijing\\beijing.gdb"

filepath = 'D:\\Desktop\\data\\gis_osm_gd\\beijing\\bj.csv'
df = pd.read_csv(filepath)

df['uid'] = 0
# df['user'] = ''

num = 0
# 使用 SearchCursor 读取表格文件
with arcpy.da.SearchCursor('gis_osm', ["OBJECTID", "uid"]) as cursor:
    # 遍历每一行记录
    for cur_row in cursor:
        df.loc[df['OSM'] == cur_row[0], 'uid'] = cur_row[1]
        # df.loc[df['OSM'] == cur_row[0], 'user'] = cur_row[2]
        num = num + 1
        if num % 2000 == 0:
            # print(df.loc[num])
            print(f'当前{num}')

del cursor

print('准备读写')
output_csv = 'D:\\Desktop\\data\\gis_osm_gd\\beijing\\matchUID_bj.csv'
df.to_csv(output_csv, index=False)