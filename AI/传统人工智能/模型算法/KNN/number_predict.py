import cv2
import joblib
import numpy

from sklearn.neighbors import KNeighborsClassifier

# 加载图片
img = cv2.imread("../../images/number-5.png")

# 灰度化、二值化
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
ret, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

# 进行结果预测，还必须让目标图片大小和训练数据图片大小一致，因此要转换图片大小
img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)

# 归一化处理图片并展平成一维
img = img.astype("float32") / 255
img = img.reshape(1, 28*28)  # 和 img.reshape(1, 28*28) 作用相同

# 加载模型并进行预测
knn: KNeighborsClassifier = joblib.load("knn-number.model")

predict = knn.predict(img)
predict_array = numpy.array(predict)
predict_num = numpy.where(predict_array == 1)[1]

print(predict_num[0])  # 5
