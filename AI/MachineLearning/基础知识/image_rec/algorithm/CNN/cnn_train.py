from keras import models
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.utils import to_categorical

# 数据集的预处理
from numpy import ndarray

x_train: ndarray
y_train: ndarray
x_test: ndarray
y_test: ndarray

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 将二维图片数据转成三维，进行形状变换以适应卷积运算的需要
x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(10000, 28, 28, 1)

# 将训练集和测试集标签转换为独热编码，10位向量，代表数字0-9
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# cnn模型训练
# 序贯方式建立模型
model = models.Sequential()

# 添加Conv2D二维卷积层
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
# 最大池化层，用于减少特征图大小，以减少模型的参数量和计算量，并防止过拟合
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.5))  # Dropout层用于防止过拟合
model.add(Flatten())  # 展平层

model.add(Dense(128, activation='relu'))  # 全链接层
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))  # softmax分类激活，输出10维分类码，就是预测值的独热编码

# 模型编译
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
# 开始训练
model.fit(x_train, y_train, validation_split=0.2, epochs=10, batch_size=200)

# 利用测试集评估模型准确率
score = model.evaluate(x_test, y_test)
print("测试集预测准确率为：", score)  # [0.04887472838163376, 0.9857000112533569] 损失值和准确率

model.save('./cnn-number.h5')
