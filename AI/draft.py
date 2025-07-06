import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier


x, y = load_iris(return_X_y=True, as_frame=False)

# 分成五份数据
kf = KFold(n_splits=5)

# 遍历每一份数据获取评分
scores = []

for train, test in kf.split(x, y):
    x_train, x_test = x[train], x[test]
    y_train, y_test = y[train], y[test]

    # 归一化
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    # 使用sklearn模型
    model = KNeighborsClassifier(n_neighbors=7)
    model.fit(x_train, y_train)

    score = model.score(x_test, y_test)
    scores.append(score)

# 最终准确率
print(np.mean(scores))  # 0.8800000000000001
