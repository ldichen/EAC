import datetime
import pandas as pd
from multiprocessing import cpu_count, Pool
from datetime import datetime


def func_editDay(df_Uid, df_All):
    # 排序
    df_sort_Uid = df_Uid.sort_values(by='uid')

    df_sort_Uid['EditDuration'] = 0.0
    df_sort_Uid['EditDays'] = 0  #
    df_sort_Uid['Weekdays'] = 0  #
    df_sort_Uid['Weekends'] = 0  #

    # 使用for循环逐行读取特定列
    for index, row in df_sort_Uid.iterrows():
        # 开始对每个id进行计算
        uid = row['uid']
        # 当前id的所有行
        specific_rows = df_All[df_All['uid'] == uid]
        timeAll = 0.0
        weekdays = 0
        weekends = 0
        # 计算编辑总时间
        for item in specific_rows.iterrows():
            create_time = datetime.fromisoformat(item[1]['created_at'])
            if (create_time.weekday() < 5):
                weekdays += 1
            elif (create_time.weekday() > 4):
                weekends += 1
            close_time = datetime.fromisoformat(item[1]['closed_at'])
            time_diff = (close_time - create_time).total_seconds() / 60
            timeAll = timeAll + time_diff
        # return df_DistinctUid
        df_sort_Uid.at[index, 'EditDurations'] = round(timeAll, 3)
        df_sort_Uid.at[index, 'Weekdays'] = weekdays
        df_sort_Uid.at[index, 'Weekends'] = weekends
        print(f"用户{uid}总编辑时间：{timeAll}时")
        print(f"用户{uid}工作日共：{weekdays}天")
        print(f"用户{uid}周末共：{weekends}天")

        # 计算总编辑天数
        df_sort_Uid.at[index, 'EditDays'] = weekdays+weekends

    return df_sort_Uid
