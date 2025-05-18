import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 使用模型训练时，要求数据是二维的，因此这里转为 13行1列 的数据
x = np.array([75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87]).reshape(-1, 1)
y = np.array([640, 645, 660, 661, 673, 688, 696, 710, 726, 727, 740, 742, 757]).reshape(-1, 1)

# 准备训练集和测试集。test_size 表示测试集占整个数据集的比例
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# 训练模型
model = LinearRegression()
model.fit(x_train, y_train)

# 输出斜率和偏置
print(model.coef_)  # [[10.0244898]]
print(model.intercept_)  # [-114.99591837]

# 使用测试集计算准确率
print(model.score(x_test, y_test))  # 0.995850645830478

# 预测88年的数据。预测数据维度要和训练数据保持一致
print(model.predict(np.array([[88]])))  # [[767.15918367]]
