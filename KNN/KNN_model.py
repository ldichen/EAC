import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

# 从CSV文件加载数据
data = pd.read_csv('D:\\Desktop\\data\\EAC\\EACupdate5.csv')

X = data.drop(columns=['uid', 'acc', 'class'])
Y = data['class']

# 将数据集拆分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 初始化KNN分类器
knn = KNeighborsClassifier()

# 定义要搜索的参数空间
param_grid = {
    'n_neighbors': [3, 5, 7, 9],  # 邻居数量
    'weights': ['uniform', 'distance'],  # 权重方式
    'p': [1, 2]  # 距离度量的参数（1：曼哈顿距离，2：欧氏距离）
}

# 初始化网格搜索
grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')

# 执行网格搜索
grid_search.fit(X_train, y_train)

# 获取最佳模型
best_knn = grid_search.best_estimator_

# 预测测试集的结果
y_pred = best_knn.predict(X_test)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print("最佳模型准确率：", accuracy)
print("最佳参数组合：", grid_search.best_params_)
