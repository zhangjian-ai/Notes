import cv2

from keras.datasets import mnist

# 加载数据集
# x_train 表示训练数据的图片集合；y_train 表示训练数据的标签集合。所谓的标签可以理解就是对应图片的名称
# x_test 表示测试数据的图片集合；y_test 表示测试数据的标签集合
# 返回的四个值都是 ndarray 数据类型，是numpy中的数组对象
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 输出一下训练集和测试集
print(x_train.shape)  # (60000, 28, 28) 表示数组中有60000万个元素，每个元素有28行，每行有28列
print(y_train.shape)  # (60000,)  60000个标签值，每个图片的标签都是0-9的数字
print(x_test.shape)  # (10000, 28, 28)

# 随即打印一张图片
print(x_train[101])
cv2.imshow(str(y_train[101]), x_train[101])
cv2.waitKey(3000)
