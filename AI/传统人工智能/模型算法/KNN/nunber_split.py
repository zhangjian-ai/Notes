import cv2, joblib
import numpy as np
from keras.datasets import mnist

def show(img):
    cv2.imshow("show", img)
    cv2.waitKey(0)

# 图片的预处理
img = cv2.imread('../../../../../../Downloads/课程的Python源码/number.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# THRESH_BINARY_INV 反二值化后将白色背景变成黑色，与MNIST相匹配
ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

img = np.rot90(img)     # 逆时针旋转90度
kernel = np.ones((3, 3), dtype=np.uint8)
img = cv2.dilate(img, kernel, iterations=2)

# 提取每一张图片，并保存到文件夹中
contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
i=1
numbers = []
for contour in contours:
    [x, y, w, h] = cv2.boundingRect(contour)  # 当得到对象轮廓后，可用boundingRect()得到包覆此轮廓的最小正矩形
    print(x, y, w, h)
    digit = img[y:y + h, x:x + w]             # 获取img中对应下标的值,并进行显示
    # show(digit)         # 可以看到已经将数字分割完成

    # 对数字进行正方形边框填充
    pad = (h-w)//2
    if pad > 0:  # 说明高度更高,要填充左右的宽度
        digit = cv2.copyMakeBorder(digit, 0, 0, pad, pad, cv2.BORDER_CONSTANT,value=0)
    else:
        digit = cv2.copyMakeBorder(digit, -pad, -pad, 0, 0, cv2.BORDER_CONSTANT,value=0)

    # 根据MNIST的训练集的数字与最边沿的距离大约有1/4的大小
    pad = digit.shape[0] // 4
    digit = cv2.copyMakeBorder(digit, pad, pad, pad, pad, cv2.BORDER_CONSTANT,value=0)

    # 利用resize进行缩放操作,将正方形图片统一为28x28像素大小
    digit = cv2.resize(digit, (28, 28), interpolation=cv2.INTER_AREA)

    # 将每一个数字按顺序保存下来
    digit = np.rot90(digit, 3)
    numbers.append(digit)
    cv2.imwrite(f"./numbers/num-{i}.png", digit)
    i += 1

# 遍历每一张图片并进行预测
result = []
estimator = joblib.load("./number-knn.plk")   # 载入knn模型
n = 0
string = "0123456789"
for img in numbers:
    img = img.astype(np.float32)    # 将数据类型由uint8转为float32
    img = img.reshape(1, 784)       # 将三维矩阵转换为一维向量
    img = img / 255              # 图片数据归一化
    img_pre = estimator.predict(img)  # 进行预测
    index = np.argmax(img_pre)
    result.append(string[index])
    n += 1
print(result)