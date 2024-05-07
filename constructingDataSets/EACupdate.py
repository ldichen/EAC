import pandas as pd
import numpy as np

csv_file_path = "D:\\Desktop\\data\\EAC\\EAC3.csv"
ECA_df = pd.read_csv(csv_file_path)

ECA_df['weekday'] = ECA_df['Fri'] + ECA_df['Mon'] + ECA_df['Tue'] + ECA_df['Wed'] + ECA_df['Thu']
ECA_df['weekend'] = ECA_df['Sat'] + ECA_df['Sun']
ECA_df['comActivity'] = ECA_df['dis_responses'] + ECA_df['com_changesets'] + ECA_df['Discussed_changesets'] + ECA_df['num_comments']
ECA_df['usualEdit'] =ECA_df.iloc[:, 35] + ECA_df.iloc[:, 36] + ECA_df.iloc[:, 37] + ECA_df.iloc[:, 38]
# ECA_df['unusualEdit'] =ECA_df.iloc[:, 39] + ECA_df.iloc[:, 40] + ECA_df.iloc[:, 41] + ECA_df.iloc[:, 42] + ECA_df.iloc[:, 43] + ECA_df.iloc[:, 44] + ECA_df.iloc[:, 45] + ECA_df.iloc[:, 46] + ECA_df.iloc[:, 47] + ECA_df.iloc[:, 48] + ECA_df.iloc[:, 49] + ECA_df.iloc[:, 50] + ECA_df.iloc[:, 51]

ECA_df['nodes_Modified'] = ECA_df['nodes_Modified'] + ECA_df['nodes_Created']
ECA_df['Ways_Modified'] = ECA_df['Ways_Modified'] + ECA_df['Ways_Created']
ECA_df['Relations_Modified'] = ECA_df['Relations_Modified'] + ECA_df['Relations_Created']
ECA_df['Reverted_changes'] = ECA_df['Reverted_changes']/ECA_df['Map_changes']
# 'nodes_Created','Ways_Created','Relations_Created'

ECA_df = ECA_df.drop(ECA_df.columns[35:52], axis=1)
ECA_df.drop(columns=['nodes_Created','Ways_Created','Relations_Created','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun','dis_responses','com_changesets','Discussed_changesets','num_comments','years_passed'], inplace=True)

output_csv = 'D:\\Desktop\\data\\EAC\\EACupdate4.csv'
ECA_df.to_csv(output_csv, index=False)

