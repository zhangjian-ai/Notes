import cv2

# 读取一张图片
img = cv2.imread("kinghonor.jpeg")

# 打印这个图片，king是图片窗口的名字
cv2.imshow("king", img)

# 展示时间。入参是ms，下面表示展示2s后关闭窗口，然后继续执行脚本
cv2.waitKey(2000)

# 直接打印图片，就可以看到图片每个像素点对应的RGB色值。注意这里输出的结果色值顺序是：B G R
print(img)
"""
[[[121  60  34]
  [121  60  34]
  [119  60  34]
  ...
  [ 81  43  19]
  [ 81  43  19]
  [ 82  44  20]]
  ...
  [138  91  70]
  [139  92  71]
  [135  91  68]]]
"""

# 直接打印某个像素点的色值
print(img[1][10])  # [115  59  34]

# 将图片穿转成RGB色值打印
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print(img_rgb)

