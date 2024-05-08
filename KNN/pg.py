import pandas as pd
from xgboost import XGBClassifier
from xgboost import XGBRegressor
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, KFold
from modelEvaluation import ME
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

csv_file_path = 'D:\\Desktop\\data\\EAC\\EACupdate.csv'
ECA_df = pd.read_csv(csv_file_path)
X = ECA_df.drop(columns=['uid', 'acc', 'class'])
Y = ECA_df['class']
# 加载模型
xgb_clf = xgb.Booster()
xgb_clf.load_model('./EAC_model.json')
# 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
dtest = xgb.DMatrix(X)
# 在测试集上进行预测
y_pred = xgb_clf.predict(dtest)
# # 将预测结果转换为类别标签
# y_pred_labels = np.argmax(y_pred, axis=1)

# 计算混淆矩阵
cm = confusion_matrix(Y, y_pred)
df = pd.DataFrame({'True Labels': Y, 'Predicted Labels': y_pred})

# 将 DataFrame 保存到 CSV 文件中
df.to_csv('D:\\Desktop\\data\\EAC\\predictions.csv', index=False)
# 可视化混淆矩阵
plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
classes = np.unique(Y)
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)

fmt = 'd'
thresh = cm.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, format(cm[i, j], fmt),
                 ha="center", va="center",
                 color="white" if cm[i, j] > thresh else "black")

plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.show()
#
# 计算准确率
accuracy = accuracy_score(Y, y_pred)
#
print("准确率:", accuracy)
model_V = ME(Y, y_pred)
model_V.macro_p()
model_V.macro_r()
model_V.macro_f1()
model_V.weighted_p()
model_V.weighted_r()
model_V.weighted_f1()
model_V.micro_p()
model_V.micro_r()
model_V.micro_f1()