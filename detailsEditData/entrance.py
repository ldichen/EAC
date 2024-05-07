import csv
import pandas as pd
from multiprocessing import cpu_count, Pool
from tqdm import tqdm
import geopandas as gpd
import datetime
import os
import asyncio

import notNULLAndPostDelete
import isChina
import df_concat
import Uid
import Edit_times_numChanges_comments_count
import Edit_duration_week_days
import softwareSkill
import osm_requset
import relation_osmId
import asyncisRelation_osmId

# "D:\\Desktop\\data\\160000001_170000000"
# "D:\\Desktop\\data\\isChina\\notNull\\16\\"
# "D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\16\\"
old_path = "D:\\Desktop\\data\\dataFeature\\"
new_path = "D:\\Desktop\\data\\dataFeature\\"


# "D:\\Desktop\\data\\dataFeature\\"

# chinaBoundary = gpd.read_file("D:\\Desktop\\data\\省界_region\\省界_region.shp")


# 读取csv
def read_csv(filename):
    print(f'正在读取{filename}')
    df = pd.read_csv(old_path + filename)
    print(f'{filename}读取完成')
    return df


# 输出csv
def out_csv(df, filename):
    print(f'正在写入{filename}')
    df.to_csv(new_path + filename, index=False)
    print(f'{filename}写入完成')


# region 去空值代码块
def notNull(filename, out_filename):
    out_csv(notNULLAndPostDelete.func_ND(read_csv(filename)), out_filename)


# endregion

# region 筛选中国区域
def getChinaData(boundary, filename, out_filename):
    out_csv(isChina.func_CN(boundary, read_csv(filename)), out_filename)


# endregion

# region 合并
def concat_csv(file_path, out_filename):
    out_csv(df_concat.func_concat(file_path), out_filename)


# endregion
# region 用户名和用户id
def uid_userName(filename, out_filename):
    out_csv(Uid.readUidZN(read_csv(filename)), out_filename)


# endregion
# region 编辑次数  评论次数  节点变更数
def dataFeature_1(id_filename, all_filename, out_filename):
    out_csv(Edit_times_numChanges_comments_count.func_EditTimes(read_csv(id_filename), read_csv(all_filename)),
            out_filename)


# endregion

# region 编辑天数  编辑工作日数量  编辑周末数量  编辑时长
def dataFeature_2(id_filename, all_filename, out_filename):
    out_csv(Edit_duration_week_days.func_editDay(read_csv(id_filename), read_csv(all_filename)), out_filename)


# endregion

def dataFeature_3(id_filename,out_filename):
    out_csv(osm_requset.func_req(read_csv(id_filename)),out_filename)

#asyncisRelation_osmId  relation_osmId
def dataFeature_4(osm_filename,out_filename):
    out_csv(asyncio.run(asyncisRelation_osmId.func_relationOSM(read_csv(osm_filename))), out_filename)

if __name__ == '__main__':
    # p = Pool(9)
    startTime = datetime.datetime.now()
    concat_csv('D:\\Desktop\\data\\gis_osm_gd\\matchUID','matchUID_All.csv')
    # dataFeature_1('uid_userName.csv', 'concatAll4.csv', 'dataFeature_1.csv')
    # dataFeature_2('uid_userName.csv', 'concatAll4.csv', 'dataFeature_2.csv')
    # dataFeature_3('uid_userName.csv','dataFeature_13.csv')
    # dataFeature_4('osmtop_99000_rows_after1000000.csv', 'osmidAndUserId_3.csv')
    # softwareSkill.func_soft(read_csv('uid_userName.csv'),read_csv('concatAll4.csv'))
    # osm_requset.func_req(read_csv('uid_userName.csv'))
    # relation_osmId.func_relationOSM(read_csv('osmApi.csv'))
    # asyncio.run(asyncisRelation_osmId.func_relationOSM())
    # Uid.readUidZN(read_csv('concatAll3.csv'))
    # uid_userName('concatAll3.csv','uid_userName.csv')
    # notNull('concatAll2.csv','concatAll3.csv')
    # p.apply_async(notNull, args=("52000001_110000000.csv", "part1.csv"))
    # p.apply_async(notNull, args=("54000001_110000000.csv", "part2.csv"))
    # p.apply_async(notNull, args=("56000001_110000000.csv", "part3.csv"))
    # p.apply_async(notNull, args=("58000001_110000000.csv", "part4.csv"))
    # p.apply_async(notNull, args=("60000001_110000000.csv", "part5.csv"))
    # p.apply_async(getChinaData, args=(chinaBoundary,"part1.csv", "part1_CN.csv"))
    # p.apply_async(getChinaData, args=(chinaBoundary,"part2.csv", "part2_CN.csv"))
    # p.apply_async(getChinaData, args=(chinaBoundary, "part3.csv", "part3_CN.csv"))
    # p.apply_async(getChinaData, args=(chinaBoundary, "part4.csv", "part4_CN.csv"))
    # p.apply_async(getChinaData, args=(chinaBoundary, "part5.csv", "part5_CN.csv"))
    # p.apply_async(getChinaData, args=(chinaBoundary, "part6.csv", "part6_CN.csv"))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\6", 'concat_6.csv'))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\7", 'concat_7.csv'))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\8", 'concat_8.csv'))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\9", 'concat_9.csv'))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\10", 'concat_10.csv'))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\11", 'concat_11.csv'))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\12", 'concat_12.csv'))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\16", 'concat_16.csv'))
    # p.apply_async(concat_csv, args=("D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\concat\\concat2", 'concatAll.csv'))
    # p.close()
    # p.join()
    endTime = datetime.datetime.now()
    print("已完成", endTime - startTime)
