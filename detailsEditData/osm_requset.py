import time
import re

import pandas as pd
import requests
import json
import time
import traceback


def func_req(df_Uid):
    # 排序
    df_sort_Uid = df_Uid.sort_values(by='uid')

    df_sort_Uid['Registered'] = ''  # 注册时间
    df_sort_Uid['mapping_days'] = 0  # 进行地图编辑的天数
    df_sort_Uid['Map_changes'] = 0  # 贡献者地图编辑更改的数量
    df_sort_Uid['Reverted_changes'] = 0  # 贡献者被撤回编辑数
    df_sort_Uid['restored_changesets'] = 0  # 撤回他人涉及变更集数量
    df_sort_Uid['restored_map_edits'] = 0  # 撤回他人节编辑数
    df_sort_Uid['revert_contributors'] = 0  # 撤回涉及志愿者数量

    df_sort_Uid['Discussed_changesets'] = 0  # 贡献者参与讨论变更集发问数
    df_sort_Uid['dis_responses'] = 0  # 回复数
    df_sort_Uid['com_changesets'] = 0  # 回参与了多少个变更集讨论
    df_sort_Uid['num_comments'] = 0  # 发表了多少个变更集评论

    df_sort_Uid['nodes_Created'] = 0  # 节点创建数
    df_sort_Uid['nodes_Modified'] = 0  # 节点修改数
    df_sort_Uid['nodes_Deleted'] = 0  # 节点删除数
    df_sort_Uid['Ways_Created'] = 0  # 道路创建数
    df_sort_Uid['Ways_Modified'] = 0  # 道路修改数
    df_sort_Uid['Ways_Deleted'] = 0  # 道路删除数
    df_sort_Uid['Relations_Created'] = 0  # 关系创建数
    df_sort_Uid['Relations_Modified'] = 0  # 关系修改数
    df_sort_Uid['Relations_Deleted'] = 0  # 关系删除数

    df_sort_Uid['editors'] = ''  # 使用的编辑器

    df_sort_Uid['mapping_days_year'] = ''  # 每年的变更集数
    df_sort_Uid['days'] = ''  # 每周的变更集创建分布
    df_sort_Uid['hours'] = ''  # 每天的变更集创建分布

    df_sort_Uid['Overall'] = 0  # 总变更集数
    df_sort_Uid['comments'] = 0  # 变更集注释数
    df_sort_Uid['Unique_comments'] = 0  # 单一注释数
    df_sort_Uid['Median_length'] = 0.0  # 平均注释长度

    isOK = True
    forNum = 0
    # 使用for循环逐行读取特定列
    for index, row in df_sort_Uid.iterrows():
        # 开始对每个id进行计算
        user = row['user']
        user = user.replace(' ', '%20')
        # 当前id的所有行
        if isOK:
            try:
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                    'Cookie': '__utma=61114931.1871542579.1709519222.1709519222.1709519222.1; __utmz=61114931.1709519222.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); HDYC=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJteV9jbGllbnQiOiJIRFlDIiwibXlfdG9rZW4iOiI1NGEyOTU2NjM5ZDk0OTdhMmZmMzAwYTA2YTRjNDU4NiIsIm9zbV91c2VyIjoibGl1ZGljaGVuIiwib3NtX3VpZCI6MjExMDk5MDQsIm9zbV9pbWciOiJodHRwczpcL1wvd3d3Lm9wZW5zdHJlZXRtYXAub3JnXC9hc3NldHNcL2F2YXRhcl9zbWFsbC1kNmJiMTc0MWYwNTJlYzBhMWU1MzZmMDFhZDMxYzU1MWFhMjVlNDJmMzUxOTRiZGMwMzdlMDg0MzgyZjBmMjc4LnBuZyIsIm9zbV9hY2Nlc3NfdG9rZW4iOiJwX2pIYktadkFGYmJqdWxFenFTcnpnU0hydzY0VUVtMmZpTFZnczZoVUFjIiwiZXhwIjoxNzExMjg2OTQ0fQ%3D%3D.f5nsoRfbAQeC7XK1FPXvlsJYPyJYF0BbW8RJNVFjX2w%3D'
                }
                # time.sleep(0.2)
                network_path = 'https://hdyc.neis-one.org/?'
                print(f"请求{user}")
                max_retries = 5  # 设置最大重试次数
                retry_delay = 5  # 设置重试间隔时间（单位：秒）
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # 发送请求
                        response = requests.get(network_path + user, headers=header)

                        # 检查响应状态码
                        if response.status_code == 200:
                            print("请求成功")
                            break  # 如果请求成功，跳出循环
                        else:
                            print("请求失败:", response.status_code)
                            retry_count += 1  # 增加重试计数
                            time.sleep(retry_delay)  # 等待一段时间后重新发送请求
                    except Exception as e:
                        print("请求异常:", e)
                        retry_count += 1  # 增加重试计数
                        time.sleep(retry_delay)  # 等待一段时间后重新发送请求
                # 将response.content转换为字符串
                content_str = response.content.decode('utf-8')

                # 使用正则表达式匹配var response的内容
                match = re.search(r'var response = ({.*?});', content_str)
                if match:
                    # 提取出目标内容
                    response_json = match.group(1)
                    # 将 JSON 字符串转换为字典对象
                    response_data = json.loads(response_json)
                    # 检查 "Response" 键是否存在
                    if "Response" in response_data:
                        print("Response 键存在")
                        continue

                    # 查询 uid 的值
                    df_sort_Uid.at[index, 'Registered'] = response_data['contributor']['since']
                    if (len(response_data['changesets'])):
                        df_sort_Uid.at[index, 'mapping_days'] = int(response_data['changesets']['mapping_days'])
                        df_sort_Uid.at[index, 'Map_changes'] = int(response_data['changesets']['changes'])
                        df_sort_Uid.at[index, 'editors'] = response_data['changesets']['editors']

                        df_sort_Uid.at[index, 'mapping_days_year'] = response_data['changesets']['mapping_days_year']
                        df_sort_Uid.at[index, 'days'] = response_data['changesets']['days']
                        df_sort_Uid.at[index, 'hours'] = response_data['changesets']['hours']
                        df_sort_Uid.at[index, 'Overall'] = int(response_data['changesets']['no'])
                        split_string = response_data['changesets']['info'].split(';')

                        df_sort_Uid.at[index, 'comments'] = int(split_string[1])  #
                        df_sort_Uid.at[index, 'Unique_comments'] = int(split_string[2])  #
                        df_sort_Uid.at[index, 'Median_length'] = float(split_string[4])  #

                    if (len(response_data['contributor']['revert_actions'])):
                        df_sort_Uid.at[index, 'Reverted_changes'] = int(response_data['contributor']['revert_actions'][
                                                                            'reverted_map_edits'])
                        df_sort_Uid.at[index, 'restored_changesets'] = int(
                            response_data['contributor']['revert_actions'][
                                'restored_changesets'])
                        df_sort_Uid.at[index, 'restored_map_edits'] = int(
                            response_data['contributor']['revert_actions'][
                                'restored_map_edits'])
                        df_sort_Uid.at[index, 'revert_contributors'] = int(
                            response_data['contributor']['revert_actions'][
                                'contributors'])
                    if (len(response_data['discussion'])):
                        df_sort_Uid.at[index, 'Discussed_changesets'] = int(
                            response_data['discussion']['dis_changesets'])
                        df_sort_Uid.at[index, 'dis_responses'] = int(response_data['discussion']['dis_responses'])
                        df_sort_Uid.at[index, 'com_changesets'] = int(response_data['discussion']['com_changesets'])
                        df_sort_Uid.at[index, 'num_comments'] = int(response_data['discussion']['num_comments'])

                    if (len(response_data['nodes'])):
                        df_sort_Uid.at[index, 'nodes_Created'] = int(response_data['nodes']['c'])
                        df_sort_Uid.at[index, 'nodes_Modified'] = int(response_data['nodes']['m'])
                        df_sort_Uid.at[index, 'nodes_Deleted'] = int(response_data['nodes']['d'])
                    if (len(response_data['ways'])):
                        df_sort_Uid.at[index, 'Ways_Created'] = int(response_data['ways']['c'])
                        df_sort_Uid.at[index, 'Ways_Modified'] = int(response_data['ways']['m'])
                        df_sort_Uid.at[index, 'Ways_Deleted'] = int(response_data['ways']['d'])
                    if (len(response_data['relations'])):
                        df_sort_Uid.at[index, 'Relations_Created'] = int(response_data['relations']['c'])
                        df_sort_Uid.at[index, 'Relations_Modified'] = int(response_data['relations']['m'])
                        df_sort_Uid.at[index, 'Relations_Deleted'] = int(response_data['relations']['d'])
            except Exception as e:
                error_message = traceback.format_exc()
                print("发生了异常:", e)
                print("发生了异常:", error_message)
                print(f'到了{user}发生了错误')
                print(forNum)  # 打印出来到多少行发生错误
                return df_sort_Uid  # 保存已经爬取到的内容
        forNum += 1
        # if user == 'liangwiner':
        # if(forNum==31000):
        #     print(forNum)
        #     print(user)
        #     isOK= True
        if forNum == 200:
            print(forNum)
            return df_sort_Uid


# print(res.content)
if __name__ == '__main__':
    df = pd.read_csv("D:\\Desktop\\unique_result.csv")
    out_df = func_req(df)
    out_df.to_csv("D:\\Desktop\\unique_result1.csv", index=False)
