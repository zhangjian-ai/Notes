import joblib

from numpy import ndarray
from keras.datasets import mnist

from sklearn.preprocessing import LabelBinarizer
from sklearn.neighbors import KNeighborsClassifier

# 加载数据集
x_train: ndarray
y_train: ndarray
x_test: ndarray
y_test: ndarray

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 先将图片展平为一维数组
# 再将像素颜色进行归一化处理
x_train = x_train.reshape(x_train.shape[0], 28*28)  # 将数组重新排列为60000个一维数组，每个一维数组长度是28*28
x_train = x_train.astype("float32") / 255  # 将数组中的值都除以255进行归一化
x_test = x_test.reshape(x_test.shape[0], 28*28)
x_test = x_test.astype("float32") / 255

# 由于y标签是0-9的数值，所以需要进行独热编码
lb: LabelBinarizer = LabelBinarizer().fit(y_train)
y_train = lb.transform(y_train)
y_test = lb.transform(y_test)

# 使用KNN进行训练
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, y_train)

# 评估模型，使用测试集看识别的准确率
test_predict = knn.predict(x_test)  # 预测测试集对应的结果
print(test_predict)  # 这里返回一个二维数组，二维数组每个元素就是一个独热编码数组，表示预测的值

score = knn.score(x_test, y_test)  # 返回测试数据相对于预期值的准确率
print("识别准确率:" + str(score))

# 保存模型
joblib.dump(knn, "knn-number.model")
