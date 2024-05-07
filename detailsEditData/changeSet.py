import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
# "D:\Desktop\test.xml"
# "E:\\Download\\changesets-191202.osm\\changesets-191202.osm"
#"D:\\Desktop\\data\\changesets-240226.osm\\changesets-240226.osm"
changeset_file = "D:\\Desktop\\2022.osm"
filename = "D:\\Desktop\\"
# 数据行
dataNum = 0
# 设置阈值，删除空值数量超过阈值的列
threshold = 1999000


def write_data_to_csv(dataframe, fn, fnType):
    print('准备读写')
    fn = f"{fn}{fnType}_110000000.csv"
    # 写入 CSV 文件
    dataframe.to_csv(fn, mode='w', index=False)


# 打开 XML 文件
with open(changeset_file, "rb") as f:
    # 创建 XML 解析器
    context = ET.iterparse(f, events=("start",))
    data = []
    for event, elem in tqdm(context):
        if elem.tag == 'changeset':
                dataNum += 1
                if 0 < dataNum:
                    if dataNum % 500000 == 0:
                        print(dataNum)
                    #正片开始
                    if dataNum < 2000000:
                        row_data = {}
                        for key, value in elem.attrib.items():
                            row_data[key] = value
                        if len(elem) > 0:
                            for child_elem in elem:
                                tmp_key = ''
                                tmp_value = ''
                                for key, value in child_elem.attrib.items():
                                    if (key == 'k'):
                                        tmp_key = value
                                    if (key == 'v'):
                                        tmp_value = value
                                if (tmp_key != '' and tmp_value != ''):
                                    row_data[tmp_key] = tmp_value
                            # 添加行
                            data.append(row_data)
                        else:
                            # 添加行
                            data.append(row_data)
                    else:
                        if (dataNum == 2000001):
                            df = pd.DataFrame(data)
                            # 统计每列中的空值数量
                            null_counts = df.isna().sum()
                            columns_to_drop = null_counts[null_counts > threshold].index
                            df.drop(columns=columns_to_drop, inplace=True)
                            write_data_to_csv(df, filename, dataNum)
                            print('第一部分读写完成!')
                            data = []
                        if dataNum < 4000000:
                            row_data = {}
                            for key, value in elem.attrib.items():
                                row_data[key] = value
                            if len(elem) > 0:
                                for child_elem in elem:
                                    tmp_key = ''
                                    tmp_value = ''
                                    for key, value in child_elem.attrib.items():
                                        if (key == 'k'):
                                            tmp_key = value
                                        if (key == 'v'):
                                            tmp_value = value
                                    if (tmp_key != '' and tmp_value != ''):
                                        row_data[tmp_key] = tmp_value
                                # 添加行
                                data.append(row_data)
                            else:
                                # 添加行
                                data.append(row_data)
                        else:
                            if (dataNum == 4000001):
                                df = pd.DataFrame(data)
                                # 统计每列中的空值数量
                                null_counts = df.isna().sum()
                                columns_to_drop = null_counts[null_counts > threshold].index
                                df.drop(columns=columns_to_drop, inplace=True)
                                write_data_to_csv(df, filename, dataNum)
                                print('第二部分读写完成!')
                                data = []  # 清空data
                                break
                            # if dataNum <= 7500000:
                            #     row_data = {}
                            #     for key, value in elem.attrib.items():
                            #         row_data[key] = value
                            #     if len(elem) > 0:
                            #         for child_elem in elem:
                            #             tmp_key = ''
                            #             tmp_value = ''
                            #             for key, value in child_elem.attrib.items():
                            #                 if (key == 'k'):
                            #                     tmp_key = value
                            #                 if (key == 'v'):
                            #                     tmp_value = value
                            #             if (tmp_key != '' and tmp_value != ''):
                            #                 row_data[tmp_key] = tmp_value
                            #         # 添加行
                            #         data.append(row_data)
                            #     else:
                            #         # 添加行
                            #         data.append(row_data)
                            # else:
                            #     if (dataNum == 7500001):
                            #         df = pd.DataFrame(data)
                            #         # 统计每列中的空值数量
                            #         null_counts = df.isna().sum()
                            #         columns_to_drop = null_counts[null_counts > threshold].index
                            #         df.drop(columns=columns_to_drop, inplace=True)
                            #         write_data_to_csv(df, filename, dataNum)
                            #         print('第三部分读写完成!')
                            #         data = []  # 清空data
                            #         break
                        #         if dataNum <= 58000000:
                        #             row_data = {}
                        #             for key, value in elem.attrib.items():
                        #                 row_data[key] = value
                        #             if len(elem) > 0:
                        #                 for child_elem in elem:
                        #                     tmp_key = ''
                        #                     tmp_value = ''
                        #                     for key, value in child_elem.attrib.items():
                        #                         if (key == 'k'):
                        #                             tmp_key = value
                        #                         if (key == 'v'):
                        #                             tmp_value = value
                        #                     if (tmp_key != '' and tmp_value != ''):
                        #                         row_data[tmp_key] = tmp_value
                        #                 # 添加行
                        #                 data.append(row_data)
                        #             else:
                        #                 # 添加行
                        #                 data.append(row_data)
                        #         else:
                        #             if (dataNum == 58000001):
                        #                 df = pd.DataFrame(data)
                        #                 # 统计每列中的空值数量
                        #                 null_counts = df.isna().sum()
                        #                 columns_to_drop = null_counts[null_counts > threshold].index
                        #                 df.drop(columns=columns_to_drop, inplace=True)
                        #                 write_data_to_csv(df, filename, dataNum)
                        #                 print('第四部分读写完成!')
                        #                 data = []  # 清空data
                        #             if dataNum <= 60000000:
                        #                 row_data = {}
                        #                 for key, value in elem.attrib.items():
                        #                     row_data[key] = value
                        #                 if len(elem) > 0:
                        #                     for child_elem in elem:
                        #                         tmp_key = ''
                        #                         tmp_value = ''
                        #                         for key, value in child_elem.attrib.items():
                        #                             if (key == 'k'):
                        #                                 tmp_key = value
                        #                             if (key == 'v'):
                        #                                 tmp_value = value
                        #                         if (tmp_key != '' and tmp_value != ''):
                        #                             row_data[tmp_key] = tmp_value
                        #                     # 添加行
                        #                     data.append(row_data)
                        #                 else:
                        #                     # 添加行
                        #                     data.append(row_data)
                        #             else:
                        #                 if (dataNum == 60000001):
                        #                     df = pd.DataFrame(data)
                        #                     # 统计每列中的空值数量
                        #                     null_counts = df.isna().sum()
                        #                     columns_to_drop = null_counts[null_counts > threshold].index
                        #                     df.drop(columns=columns_to_drop, inplace=True)
                        #                     write_data_to_csv(df, filename, dataNum)
                        #                     print('第四部分读写完成!')
                        #                     break
        elem.clear()
    # except ET.ParseError as e:
    #     # 如果遇到 ParseError 异常（例如未闭合的标签），则跳过该节点并继续解析
    #     print("遇到未闭合标签，跳过:", e)
            # if 10000000 <= dataNum < 20000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # elif 20000000 <= dataNum < 30000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # elif 30000000 <= dataNum < 40000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # elif 40000000 <= dataNum < 50000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # elif 50000000 <= dataNum < 60000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             #         print(child_elem.tag)
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # elif 60000000 <= dataNum < 70000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             #         print(child_elem.tag)
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # elif 70000000 <= dataNum < 80000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             #         print(child_elem.tag)
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # elif 80000000 <= dataNum < 90000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             #         print(child_elem.tag)
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # elif 90000000 <= dataNum < 100000000:
            #     row_data = {}
            #     for key, value in elem.attrib.items():
            #         row_data[key] = value
            #     if len(elem) > 0:
            #         for child_elem in elem:
            #             #         print(child_elem.tag)
            #             for key, value in child_elem.attrib.items():
            #                 # 如果子元素有属性，则将属性添加至行中
            #                 row_data[key] = value
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            #     else:
            #         # 添加行
            #         data.append(row_data)
            #         dataNum += 1
            # else:
            #     print('输出')
            #     df = pd.DataFrame(data)
            #     write_data_to_csv(df, filename, dataNum)
