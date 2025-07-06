import joblib
import numpy
from numpy import ndarray
from keras.datasets import mnist
from sklearn.neighbors import KNeighborsClassifier

x_train: ndarray
y_train: ndarray
x_test: ndarray
y_test: ndarray
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 任意取一张测试图片
img = x_test[9526]
label = y_test[9526]

# 归一化处理图片并展平成一维
img = img.astype("float32") / 255
img = img.reshape(1, -1)  # 和 img.reshape(1, 28*28) 作用相同

# 加载模型并进行预测
knn: KNeighborsClassifier = joblib.load("knn-number.model")

predict = knn.predict(img)  # 模型训练时数值标签被转换为独热编码了，因此我们可以使用numpy将其转换回来

# 独热编码将数组中对应索引处的0改为1，它的索引值就是对应的数值
# numpy.where 查找数组中值等于1的索引并返回
predict_array = numpy.array(predict)
target = numpy.where(predict_array == 1)[1]

print(target[0])
print(label)
