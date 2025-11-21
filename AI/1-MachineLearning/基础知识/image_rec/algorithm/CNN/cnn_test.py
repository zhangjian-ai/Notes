import os
import cv2
import numpy as np
from keras import Sequential
from keras.models import load_model

files = os.listdir("../../../../images/numbers/")

# 加载模型并进行预测
model: Sequential = load_model('cnn-number.h5')

# 遍历图片并修改为图形并预测结果
for file in files:
    img = cv2.imread(f"../../images/numbers/{file}")

    # 打印下图片
    # cv2.imshow("", img)
    # cv2.waitKey(500)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 灰度化
    ret, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)  # 二值化

    # 满足CNN的形状要求
    img = img.reshape(1, 28, 28, 1)
    pred: np.ndarray = model.predict(img)

    # 打印独热编码中最大值的索引，也就是1的索引，也就对应其表示的数值
    print(pred.argmax())
