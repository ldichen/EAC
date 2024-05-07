import xml
from tqdm import tqdm
#"D:\\Desktop\\30000000.osm"
# "D:\\Desktop\\data\\changesets-240226.osm\\changesets-240226.osm"
path = "D:\\Desktop\\data\\changesets-240226.osm\\changesets-240226.osm"
num = 0
with open(path, 'r', encoding='utf-8') as file:
    # 逐行读取文件内容
    for line in tqdm(file):
        num += 1
        # print(line.strip())
        if num >= 5000000:
            print(line.strip())
        if num == 5000050:
            break
        #     if num % 500000 == 0:
        #         print(line.strip())
