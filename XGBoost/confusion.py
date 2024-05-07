import pandas as pd
from sklearn.metrics import confusion_matrix
from modelEvaluation import ME
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, KFold
from modelEvaluation import ME
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
from matplotlib import rcParams

# 读取CSV文件
data = pd.read_csv('D:\\Desktop\\data\\EAC\\predictions.csv')

# 获取真实值和预测值
y_true = data["True Labels"]
y_pred = data["Predicted Labels"]
X_train, X_test, y_train, y_test = train_test_split(y_true, y_pred, test_size=0.3, random_state=42)
# 生成混淆矩阵
conf_matrix = confusion_matrix(X_test, y_test)

print("混淆矩阵:")
print(conf_matrix)

# 计算准确率
accuracy = accuracy_score(X_test, y_test)
#
print("准确率:", accuracy)

model_V = ME(X_test, y_test)
model_V.macro_p()
model_V.macro_r()
model_V.macro_f1()
model_V.weighted_p()
model_V.weighted_r()
model_V.weighted_f1()
model_V.micro_p()
model_V.micro_r()
model_V.micro_f1()

# 计算混淆矩阵
# cm = confusion_matrix(y_true, y_pred)

# # 可视化混淆矩阵
# plt.figure(figsize=(8, 6))
# plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
# plt.title('Confusion Matrix')
# plt.colorbar()
classes = np.unique(y_true)
# tick_marks = np.arange(len(classes))
# plt.xticks(tick_marks, classes, rotation=45,fontsize=12)
# plt.yticks(tick_marks, classes,fontsize=16)

proportion = []
length = len(conf_matrix)
print(length)
for i in conf_matrix:
    for j in i:
        temp = j / (np.sum(i))
        proportion.append(temp)
# print(np.sum(confusion_matrix[0]))
# print(proportion)
pshow = []
for i in proportion:
    pt = "%.2f%%" % (i * 100)
    pshow.append(pt)
proportion = np.array(proportion).reshape(length, length)  # reshape(列的长度，行的长度)
pshow = np.array(pshow).reshape(length, length)

# print(pshow)
config = {
    "font.family": 'Times New Roman',  # 设置字体类型
}
rcParams.update(config)
plt.imshow(proportion, interpolation='nearest', cmap=plt.cm.Blues)  # 按照像素显示出矩阵
# (改变颜色：'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd',
# 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn')
# plt.title('confusion_matrix')
plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, fontsize=12)
plt.yticks(tick_marks, classes, fontsize=12)

iters = np.reshape([[[i, j] for j in range(length)] for i in range(length)], (conf_matrix.size, 2))
for i, j in iters:
    if (i == j):
        plt.text(j, i - 0.12, format(conf_matrix[i, j]), va='center', ha='center', fontsize=10, color='white',
                 weight=5)  # 显示对应的数字
        plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=10, color='white')
    else:
        plt.text(j, i - 0.12, format(conf_matrix[i, j]), va='center', ha='center', fontsize=10)  # 显示对应的数字
        plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=10)

plt.ylabel('True label',fontsize=16)
plt.xlabel('Predicted label',fontsize=16)
plt.tight_layout()
plt.show()