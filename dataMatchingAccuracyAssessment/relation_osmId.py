import pandas as pd
import threading
import concurrent.futures
import requests
import queue
import xml.etree.ElementTree as ET
import time

# 全局队列用于存储结果
results = queue.Queue()
# 错误id集合
error_results = queue.Queue()

current_request = 0


# 定义一个函数，用于请求接口并将结果存储到队列中
def request_api(url):
    try:
        global current_request
        current_request += 1
        max_retries = 5  # 设置最大重试次数
        retry_delay = 5  # 设置重试间隔时间（单位：秒）
        retry_count = 0
        while retry_count < max_retries:
            try:
                # 发送请求
                response = requests.get(url)
                # 检查响应状态码
                if response.status_code == 200:
                    print(f"{url}请求成功,当前{current_request}")
                    break  # 如果请求成功，跳出循环
                else:
                    print(f"{url}请求失败:", response.status_code)
                    retry_count += 1  # 增加重试计数
                    time.sleep(retry_delay)  # 等待一段时间后重新发送请求
            except Exception as e:
                print(f"{url}请求异常:", e)
                retry_count += 1  # 增加重试计数
                time.sleep(retry_delay)  # 等待一段时间后重新发送请求
        # 将文本内容转换为字符串并解析为 XML 树
        xml_str = response.content.decode("utf-8")
        xml_tree = ET.fromstring(xml_str)
        ways = xml_tree.findall('.//way')
        # 遍历每个 way 元素并获取 id 属性值
        for way in ways:
            row_data = {}
            for key, value in way.attrib.items():
                row_data[key] = value
            results.put(row_data)
    except Exception as e:
        print(f"Error occurred while requesting {url}: {e}")
        errpr_data = {}
        value_after_last_slash = url.split('/')[-1]
        errpr_data['osm_id'] = value_after_last_slash
        error_results.put(errpr_data)


# df_osmApi
def func_relationOSM(df_osmApi):
    # 创建一个线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # 提交任务给线程池，每个任务对应一个接口的请求
        # 这样线程池中的线程会自动处理这些任务，直到所有任务完成
        futures = [executor.submit(request_api, row[1]['api']) for row in df_osmApi.iterrows()]
        # futures = [executor.submit(request_api,  'https://api.openstreetmap.org/api/0.6/way/4974233'),executor.submit(request_api,  'https://api.openstreetmap.org/api/0.6/way/4974235')]

        # 等待所有任务完成
        concurrent.futures.wait(futures)
        data = []
        errordata = []
        # 从队列中获取数据并打印
        while not results.empty():
            tempdata = results.get()
            data.append(tempdata)
            # print(data)
        while not error_results.empty():
            tempdata = error_results.get()
            errordata.append(tempdata)
        df_errorResult = pd.DataFrame(errordata)
        df_errorResult.to_csv('D:\\Desktop\\data\\dataFeature\\errorOSMApi.csv', index=False)
        df_result = pd.DataFrame(data)
        return df_result
