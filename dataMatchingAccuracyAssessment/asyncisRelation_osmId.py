import pandas as pd
import asyncio
import aiohttp
import time
import xml.etree.ElementTree as ET

current_request = 0

failed_urls_queue = asyncio.Queue()
async def request_api(session, url, semaphore):
    async with semaphore:
        max_retries = 3
        retry_delay = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        global current_request
                        current_request += 1
                        print(f"{url}请求成功,当前{current_request}")
                        xml_str = await response.text()
                        xml_tree = ET.fromstring(xml_str)
                        ways = xml_tree.findall('.//way')
                        for way in ways:
                            row_data = {}
                            for key, value in way.attrib.items():
                                row_data[key] = value
                        return row_data
                    else:
                        print(f"{url} 请求失败: {response.status}")
                        retry_count += 1
                        await asyncio.sleep(retry_delay)
            except Exception as e:
                print(f"{url} 请求异常: {e}")
                retry_count += 1
                await asyncio.sleep(retry_delay)
        print(f"{url} 请求失败次数过多，放弃重试")
        await failed_urls_queue.put(url)


# results, error_results,
async def fetch_all_urls(urls, semaphore):
    proxy = 'http://127.0.0.1:4732'
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        print('fetch_all_urls,进来了')
        for url in urls:
            task = request_api(session, url, semaphore)
            tasks.append(task)
        print('fetch_all_urls,出去了')
        results = await asyncio.gather(*tasks)
        return results


# df_osmApi
async def func_relationOSM(df_osmApi):
    urls = df_osmApi['api'].tolist()
    # urls = ['https://api.openstreetmap.org/api/0.6/way/4974235', 'https://api.openstreetmap.org/api/0.6/way/4974232',
    #         'https://api.openstreetmap.org/api/0.6/way/4974238']
    # 控制并发请求的信号量
    semaphore = asyncio.Semaphore(450)
    true_data = []
    error_data = []
    start_time = time.time()
    print('准备发送请求')
    results = await fetch_all_urls(urls, semaphore)
    for result in results:
        if result is not None:
            true_data.append(result)
    df_true_data = pd.DataFrame(true_data)

    end_time = time.time()

    # 检查失败队列中是否有失败的 URL
    if not failed_urls_queue.empty():
        while not failed_urls_queue.empty():
            error_data.append(await failed_urls_queue.get())
    df_error_data = pd.DataFrame(error_data)
    df_error_data.to_csv('D:\\Desktop\\data\\dataFeature\\errorOSMApi_3.csv', index=False)

    print(f"总共花费时间: {end_time - start_time} 秒")
    return df_true_data
    # data = []
    # errordata = []
    # while not results.empty():
    #     tempdata = results.get()
    #     data.append(tempdata)
    # while not error_results.empty():
    #     tempdata = error_results.get()
    #     errordata.append(tempdata)
    # df_errorResult = pd.DataFrame(errordata)
    # df_errorResult.to_csv('D:\\Desktop\\data\\dataFeature\\errorOSMApi.csv', index=False)
    # df_result = pd.DataFrame(data)
    # return df_result
