import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
def func_CN(boundary,df):
    # 在DataFrame中添加一列'isChina'，并初始化为2
    df['centerLon'] = 0.0
    df['centerLat'] = 0.0
    df['isChina'] = 2

    print("遍历判断中...")
    # 遍历DataFrame的每一行，逐行判断是否在中国区域内
    for index, row in df.iterrows():
        min_lat = row.get('min_lat')
        min_lon = row.get('min_lon')
        max_lat = row.get('max_lat')
        max_lon = row.get('max_lon')
        centerLat = min_lat + (max_lat - min_lat) / 2
        centerLon = min_lon + (max_lon - min_lon) / 2

        # 创建一个点对象
        point = Point(centerLon, centerLat)
        is_inside_china = boundary.geometry.contains(point).any()

        # 如果点在中国范围内，则将isChina设为1，否则设为0
        if is_inside_china:
            df.at[index, 'isChina'] = 1
            df.at[index,'centerLat'] = centerLat
            df.at[index,'centerLon'] = centerLon
        else:
            df.at[index, 'isChina'] = 0

    print('判断结束,准备删除')
    # 删除isChina为0的所有行
    df = df[df['isChina'] != 0]

    return df