import cv2

# 读取一张图片
img = cv2.imread("kinghonor.jpeg")

# 灰度化
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 二值化处理
# 设定阈值为128，小于128的变成0，黑色；大于等于128的变成255，白色
r, img_bin = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)

cv2.imshow("king", img_bin)
cv2.waitKey(3000)
