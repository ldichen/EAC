import arcpy
import pandas
import pandas as pd

# 设置工作空间
arcpy.env.workspace = "D:/Desktop/tempSpace"

# 输入的shp文件和CSV文件路径
shp_file = "D:\\Desktop\\data\\old_China_shp\\gis_osm_buildings_a_free_1.shp"
csv_file = "D:\\Desktop\\data\\dataFeature\\osmidAndUserId_all.csv"

# 输出的合并后的shp文件路径
# output_file = "D:\\Desktop\\data\\new_China_shp\\China_buildings.shp"
# 要匹配的字段
join_field = "osm_id"
error_num = 0
num = 0
df_csv = pd.read_csv(csv_file)
# 创建游标以向 shp 文件中插入数据
with arcpy.da.UpdateCursor(shp_file,
                           [join_field, "uid", "user", "changeset", "timestamp", "version"]) as shp_cursor:
    for row in shp_cursor:
        match = df_csv[df_csv['id'] == int(row[0])]
        # 开始对每个id进行计算
        # 如果找到匹配行，打印出匹配行
        if not match.empty:
            row[1] = match['uid'].iloc[0]
            row[2] = match["user"].iloc[0]
            row[3] = match["changeset"].iloc[0]
            row[4] = match["timestamp"].iloc[0]
            row[5] = match["version"].iloc[0]
            shp_cursor.updateRow(row)
        else:
            print(f"No match found for{row[0]}")
            error_num += 1
        num += 1
        if num % 500 == 0:
            print(f'当前{num}')
# 删除游标对象
del shp_cursor
# # 添加的字段列表
# new_fields = ["uid", "user", "changeset", "changeset", "timestamp", "version"]
#
# # 循环添加字段
# for field_name in new_fields:
#     arcpy.AddField_management(shp_file, field_name, "TEXT", field_length=50)  # 根据需要修改字段类型和长度
