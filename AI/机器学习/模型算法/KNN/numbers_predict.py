import cv2, joblib
import numpy as np

# 图片的预处理
from sklearn.neighbors import KNeighborsClassifier

img = cv2.imread('../../images/number-6.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 反二值化后将白色背景变成黑色，黑色数字变为白色，与MNIST相匹配
ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

# 逆时针旋转90度，这样方便一个一个数字的识别
img = np.rot90(img)

# 图片数字膨胀，也就是加粗。如果数字比较细可以膨胀，方便数字轮廓的识别拆分
# 原理是：当kernel中心点与图像中非0的像素点重合时，就把该像素点周边像素的值也改为这个非0值
kernel = np.ones((3, 3), dtype=np.uint8)  # 生成一个3行3列的二维数组，初始值都是1。3x3的矩阵就表示想挖扩1个像素
img = cv2.dilate(img, kernel, iterations=3)  # iterations=3 表示膨胀两次

# 提取每个数字的轮廓
contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 将数字轮廓重构建为图片
count = 1
numbers = []
for contour in contours:
    # 当得到对象轮廓后，可用boundingRect()得到包覆此轮廓的最小正矩形
    # x,y 返回的是图片左上角的坐标
    # w,h 表示图片的宽和高
    [x, y, w, h] = cv2.boundingRect(contour)

    # 根据坐标和宽高，从img中裁剪出包含数字的最小图片
    digit = img[y:y + h, x:x + w]

    # 对数字图片转换为正方形图片
    pad = (h - w) // 2

    if pad > 0:
        # 左右填充。上下填充0个像素，左右都分别填充高差一半的像素。像素位置色值填0，就是黑色背景
        digit = cv2.copyMakeBorder(digit, 0, 0, pad, pad, cv2.BORDER_CONSTANT, value=0)
    else:
        # 上下填充
        digit = cv2.copyMakeBorder(digit, -pad, -pad, 0, 0, cv2.BORDER_CONSTANT, value=0)

    # MNIST的训练集的数字与最边沿的距离大约有1/4的大小，因此将数字图片四周在再填充一下
    pad = digit.shape[0] // 4
    digit = cv2.copyMakeBorder(digit, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)

    # 如果图片像素已经小于28x28就直接丢弃，认为是无效图片
    if digit.shape[0] > 28:
        # 利用resize进行缩放操作,将正方形图片统一为28x28像素大小
        digit = cv2.resize(digit, (28, 28), interpolation=cv2.INTER_AREA)

        # 讲数字图片再旋转270度
        digit = np.rot90(digit, 3)

        # 显示一下图片
        cv2.imshow(".", digit)
        cv2.waitKey(500)

        # 保存图片
        # cv2.imwrite(f"../../images/numbers/num_{count}.png", digit)
        # count += 1

        numbers.append(digit)

# 加载模型
knn: KNeighborsClassifier = joblib.load("knn-number.model")

# 逐个预测
for num_img in numbers:
    # 将图片展平成一维
    img = num_img.reshape(1, 28*28)

    # 归一化处理
    img = img.astype("float32") / 255

    # 预测结果是一个独热编码的数组
    predict = knn.predict(img)

    # 查找独热编码数组中1的索引值，该索引值就表示了预测值
    predict_array = np.array(predict)
    predict_num = np.where(predict_array == 1)[1]
    print(predict_num)
