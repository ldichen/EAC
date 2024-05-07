import pandas as pd

# 读取 CSV 文件
df = pd.read_csv("D:\\Desktop\\data\\dataFeature\\partShpDataFeature\\dataFeature_Part_drop_weeks.csv")

df['Registered'] = pd.to_datetime(df['Registered'])
# 计算从Registered时间戳到2024年2月1日的年数差并四舍五入
target_date = pd.Timestamp('2024-02-01')
# 将 Timestamp 对象转换为秒数时间戳
target_timestamp_seconds = target_date.timestamp()
df['years_passed'] = ((target_date - df['Registered']).dt.days / 365).round().astype(int)


# 提取'mapping_days_year'列中的数据并计算平均年数
def calculate_average_year(mapping_days_year_str, years_passed_rounded):
    if (years_passed_rounded == 0):
        years_passed_rounded = 1
    mapping_dict = {}
    total_days = 0
    edit_count = 0
    for pair in mapping_days_year_str.split(';'):
        key, value = pair.split('=')
        mapping_dict[int(key)] = int(value)
        edit_count += 1

    total_days = sum(mapping_dict.values())
    average_year = total_days / years_passed_rounded
    efficient_year = edit_count / years_passed_rounded
    if efficient_year >=1:
        efficient_year = 1
    return average_year, efficient_year


df[['average_year', 'efficient_year']] = df.apply(
    lambda row: calculate_average_year(row['mapping_days_year'], row['years_passed']), axis=1, result_type='expand')

df.drop(columns=['mapping_days_year','Registered'], inplace=True)
# # 显示 DataFrame
# print(df[['average_year', 'Registered','efficient_year']].head(10))
df.to_csv("D:\\Desktop\\data\\dataFeature\\partShpDataFeature\\dataFeature_Part_drop_years.csv",index=False)