import time
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, KFold
from modelEvaluation import ME
import matplotlib.pyplot as plt
import shap
# 'D:\\Desktop\\data\\EAC\\EACupdate5.csv'
# 'D:\\Desktop\\data\\EAC\\EAC3.csv'  'D:\\Desktop\\data\\EAC\\EACupdate.csv'"E:\\Download\\seeds\\seeds_dataset.txt"
csv_file_path = "E:\\Download\\seeds\\seeds_dataset.txt"
# ECA_df = pd.read_csv(csv_file_path)
# csv_file_path = "E:\\Download\\seeds\\seeds_dataset.txt" sep='\s+'  , header=None
ECA_df = pd.read_csv(csv_file_path,sep='\s+', header=None, converters={7: lambda x: int(x) - 1})
# print(ECA_df)  0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
ECA_df.rename(columns={0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6',7: 'class'}, inplace=True)
# region ###########################randomly set actual value###################################
# # 生成高斯分布数据
# mu = 3  # 平均值
# sigma = 1  # 标准差
# size = len(ECA_df)  # 与 DataFrame 长度相同
# gaussian_data = np.random.normal(mu, sigma, size)
#
# # 将数据限制在 1 到 5 之间
# gaussian_data = np.clip(gaussian_data, 0, 4)
# # 对数据进行四舍五入
# gaussian_data = np.round(gaussian_data)
# # 将数据转换为整数
# gaussian_data = gaussian_data.astype(int)
#
# # 添加新列到 DataFrame
# ECA_df['label'] = gaussian_data

# # 统计某一列的数据情况
# column_counts = ECA_test_df['label'].value_counts()
# # 打印结果
# print(column_counts)
# endregion

# X = ECA_df.drop(columns=['uid', 'acc', 'class'])
# Y = ECA_df['class']
X = ECA_df.drop(columns=['class'])
Y = ECA_df['class']
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
# declare parameters
param_grid = {
    'max_depth': [3, 4, 5],
    'min_child_weight': [1, 2, 3, 4, 5],
    'reg_lambda': [1, 2, 3, 4],
    'gamma': [0.1, 0.2, 0.3],
    'learning_rate': [0.05, 0.1],
    'subsample': [0.5, 0.6, 0.7],
    'colsample_bytree': [0.5, 0.6, 0.7],
    'n_estimators': [50, 55, 60]
    # 'max_depth': [i for i in range(3, 10,2)],
    # 'min_child_weight': [i for i in range(1, 11,2)],
    # 'reg_lambda': [i for i in range(0, 6,2)],
    # 'gamma': [i / 10.0 for i in range(1, 11,2)],
    # 'learning_rate': [i / 100.0 for i in range(1, 31,6)],
    # 'subsample': [i / 10.0 for i in range(5, 11,2)],
    # 'colsample_bytree': [i / 10.0 for i in range(5, 11,2)],
    # 'n_estimators': [i for i in range(50, 200,30)]

}
# xgb_clf = XGBClassifier(objective='multi:softmax', num_class=3, booster='gbtree', learning_rate=0.1, min_child_weight=4,
#                         reg_lambda=1, gamma=0.2, subsample=0.6, colsample_bytree=0.5, n_estimators=55, n_jobs=16,
#                         random_state=42)
xgb_clf = XGBClassifier(objective='multi:softmax', num_class=3, booster='gbtree', n_jobs=16,
                        random_state=42)
# xgb_clf = XGBRegressor(objective='reg:linear', booster='gbtree', n_jobs=5)

# # 定义 5 折交叉验证策略
# kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
#
# # 创建一个GridSearchCV对象
# grid_search = GridSearchCV(estimator=xgb_clf, param_grid=param_grid, cv=kfold, n_jobs=16,scoring='f1_weighted',verbose=10)
#
# # 在训练集上训练模型
# grid_search.fit(X_train, y_train)
#
# # 输出最佳参数组合
# print("Best Parameters:", grid_search.best_params_)
#
# # 输出最佳模型的性能评分
# print("Best Score:", grid_search.best_score_)
xgb_clf.fit(X_train, y_train)
# xgb_clf.save_model('./EAC_model.json')

# xgb_clf.fit(X_train, y_train)

explainer = shap.TreeExplainer(xgb_clf,X_train)
shap_values = explainer(X_train)
# shap.plots.bar(shap_values[:, :, 0],max_display=50)
# shap.plots.beeswarm(shap_values[:, :, 0],max_display=50)
shap.plots.bar(shap_values[:, :, 1],max_display=50)
shap.plots.beeswarm(shap_values[:, :, 1],max_display=50)
# shap.plots.waterfall(shap_values[:, :, 0])
# shap.plots.bar(shap_values[0],max_display=50)
# shap.plots.beeswarm(shap_values[:, :, 1],max_display=50)
# 在测试集上进行预测
y_pred = xgb_clf.predict(X_test)
#
# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
#
print("准确率:", accuracy)
# model_V = ME(y_test, y_pred)
# model_V.macro_p()
# model_V.macro_r()
# model_V.macro_f1()
# model_V.weighted_p()
# model_V.weighted_r()
# model_V.weighted_f1()
# model_V.micro_p()
# model_V.micro_r()
# model_V.micro_f1()
