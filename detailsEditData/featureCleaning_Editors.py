

#'ID','JOSM','JOSM (Reverter)','Potlatch','Merkaartor','Vespucci','Go Map!!','StreetComplete','OsmAnd','Maps.Me','Level0','Every Door','RapiD','Pic4Review','Rosemary','Mapzen'

import pandas as pd
import math
# 读取 CSV 文件
df = pd.read_csv("D:\\Desktop\\data\\dataFeature\\dataFeatureAll\\dataFeature_drop_years.csv")
rowNum = 0
def calculate_editors(editors_str):
    editors_str = str(editors_str)
    keyValue = ['iD','JOSM','JOSM (Reverter)','Potlatch','Merkaartor','Vespucci','Go Map!!','StreetComplete','OsmAnd','Maps.Me','Level0','Every Door','RapiD','Pic4Review','Rosemary','Mapzen']
    mapping_dict = {}
    total_ediors = 0
    iD = 0
    JOSM = 0
    JOSMReverter = 0
    Potlatch = 0
    Merkaartor = 0
    Vespucci = 0
    GoMap = 0
    StreetComplete = 0
    OsmAnd = 0
    MapsMe = 0
    Level0 = 0
    EveryDoor = 0
    RapiD = 0
    Pic4Review = 0
    Rosemary = 0
    Mapzen = 0
    unKnowEditors = 0
    if editors_str == '' or editors_str == 'nan':
        return iD, JOSM, JOSMReverter, Potlatch, Merkaartor, Vespucci, GoMap, StreetComplete, OsmAnd, MapsMe,Level0,EveryDoor, RapiD, Pic4Review, Rosemary, Mapzen, unKnowEditors
    for pair in editors_str.split(';'):
        key, value = pair.split('=')
        mapping_dict[key] = int(value)

    total_ediors = sum(mapping_dict.values())
    valueAll = 0
    for key,value in mapping_dict.items():
        num = 0
        for item in keyValue:
            if key == item:
                valueAll = valueAll+value
                if num ==0:
                    iD = (value/total_ediors)*100
                    break
                if num ==1:
                    JOSM = (value/total_ediors)*100
                    break
                if num ==2:
                    JOSMReverter = (value/total_ediors)*100
                    break
                if num ==3:
                    Potlatch = (value/total_ediors)*100
                    break
                if num ==4:
                    Merkaartor = (value/total_ediors)*100
                    break
                if num ==5:
                    Vespucci =(value/total_ediors)*100
                    break
                if num ==6:
                    GoMap = (value/total_ediors)*100
                    break
                if num ==7:
                    StreetComplete = (value/total_ediors)*100
                    break
                if num ==8:
                    OsmAnd = (value/total_ediors)*100
                    break
                if num ==9:
                    MapsMe = (value/total_ediors)*100
                    break
                if num ==10:
                    Level0 = (value/total_ediors)*100
                    break
                if num ==11:
                    EveryDoor = (value/total_ediors)*100
                    break
                if num ==12:
                    RapiD = (value/total_ediors)*100
                    break
                if num ==13:
                    Pic4Review = (value/total_ediors)*100
                    break
                if num ==14:
                    Rosemary = (value/total_ediors)*100
                    break
                if num ==15:
                    Mapzen = (value/total_ediors)*100
                    break
            num += 1
    unKnowEditors = ((total_ediors - valueAll) / total_ediors)*100
    global rowNum
    rowNum += 1
    if rowNum == 40:
        rowNum += 0
    print(rowNum)
    return iD, JOSM, JOSMReverter, Potlatch, Merkaartor, Vespucci, GoMap, StreetComplete, OsmAnd, MapsMe,Level0,EveryDoor, RapiD, Pic4Review, Rosemary, Mapzen,unKnowEditors


df[['iD','JOSM','JOSM (Reverter)','Potlatch','Merkaartor','Vespucci','Go Map!!','StreetComplete','OsmAnd','Maps.Me','Level0','Every Door','RapiD','Pic4Review','Rosemary','Mapzen','unKnowEditors']] = df.apply(
    lambda row: calculate_editors(row['editors']), axis=1, result_type='expand')

df.drop(columns=['editors'], inplace=True)
# # 显示 DataFrame
# print(df[['iD','JOSM','JOSM (Reverter)','Potlatch','Merkaartor','Vespucci','Go Map!!','StreetComplete','OsmAnd','Maps.Me','Level0','Every Door','RapiD','Pic4Review','Rosemary','Mapzen','unKnowEditors']].head(10))
df.to_csv("D:\\Desktop\\data\\dataFeature\\dataFeatureAll\\dataFeature_drop_editors.csv",index=False)