import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from keras.models import Sequential
from keras.layers import Input, Dense, Dropout
from keras import activations, losses, initializers, optimizers

from sklearn.metrics import classification_report


data = pd.read_csv("data/BankCustomer.csv")

y = data["Exited"]
x: pd.DataFrame = data.iloc[:, :-1]

x["Gender"].replace({"Female": 0}, inplace=True)
x["Gender"].replace({"Male": 1}, inplace=True)

city = pd.get_dummies(x["City"], prefix="City")
x = pd.concat([x, city], axis=1)  # axis=1 表示按列拼接
x = x.drop(["Name", "City"], axis=1)

# 归一化处理训练数据，标签因为本身就是0和1，所以不用再处理
x = StandardScaler().fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

model = Sequential()
model.add(Input(shape=(x.shape[1], )))
model.add(Dense(units=32, activation=activations.relu, kernel_initializer=initializers.HeNormal()))
model.add(Dropout(0.1))
model.add(Dense(units=64, activation=activations.relu, kernel_initializer=initializers.HeNormal()))
model.add(Dropout(0.2))
model.add(Dense(units=128, activation=activations.mish))
model.add(Dropout(0.3))
model.add(Dense(units=256, activation=activations.mish))
model.add(Dropout(0.4))
model.add(Dense(units=512, activation=activations.mish))
model.add(Dropout(0.5))
model.add(Dense(units=1, activation=activations.sigmoid))
model.compile(optimizer=optimizers.Adam(), loss=losses.binary_crossentropy, metrics=["acc"])
model.fit(x_train, y_train, epochs=50, batch_size=150)

# 预测结果
y_pred = model.predict(x_test, batch_size=100)
y_pred = np.round(y_pred)
y_test = y_test.values.reshape(*y_pred.shape)

# 数据报告
report = classification_report(y_test, y_pred, labels=[0, 1])
print(report)
"""
              precision    recall  f1-score   support

           0       0.89      0.96      0.92      1599
           1       0.77      0.54      0.63       401

    accuracy                           0.87      2000
   macro avg       0.83      0.75      0.78      2000
weighted avg       0.87      0.87      0.87      2000
"""
