import cv2
import numpy as np

from numpy import ndarray

# 读取一张图片，返回是一个ndarray对象
# 图片是一个平面度，用二维数组来表示。其中一维数组的长度就是图片的高，二维数组的长度就是图片的宽
# 图片的每个像素点，用 b, g, r 三个色值表示，也就是颜色
img: ndarray = cv2.imread("kinghonor.jpeg")

# 图像的形状，其实就是返回了表示图片信息的三维数组信息
# 分别是 高、宽 和 三个色值的数组
print(img.shape)  # (800, 1495, 3)
height, weight = img.shape[0:2]  # ndarray 支持常规list类型的切片操作

# 根据灰度化公式将 b g r 转成一个值
# 方式一：土办法
rows = []
for h in range(height):
    row = []
    for w in range(weight):
        # 通过 h w 下标拿到 b g r 的列表
        # b, g, r = img[h][w]  # 列表下标形式
        b, g, r = img[h, w]  # ndarray 可以直接像这样获取第 h 行，第 w 列的值

        # 把计算后的灰度值放入新的行中
        row.append(0.114 * b + 0.587 * g + 0.299 * r)
    rows.append(row)

# 要打印图片必须将list转为ndarray
# unit8 表示 unsigned int 8 ，意思是非负的8位整数，8位二进制表达的整数最大为255，刚好可以表示颜色0-255的取值
new_img = np.array(rows, dtype=np.uint8)

# 方式二：直接使用ndarray来保存
new_img = np.zeros((height, weight), dtype=np.uint8)  # 创建一个二维数组，每个下标处的值初始化为0，类型是 unit8
for h in range(height):
    for w in range(weight):
        b, g, r = img[h, w]  # ndarray 可以直接像这样获取第 h 行，第 w 列的值

        # 把计算后的灰度值放入新的行中
        # 赋值时会直接把小数转为 unit8
        new_img[h, w] = (0.114 * b + 0.587 * g + 0.299 * r)

# 方式三：使用ndarray的特性，不用循环
# ndarray 中的数据可以直接进行数学运算，这里区别于list。ndarray会把每个值进行运算，list 则是扩展列表长度
blues = img[:, :, 0] * 0.114  # 第一个冒号表示取所有行，第二个表示取所有列，然后获取所有三原色列表的0下标值并进行运算
greens = img[:, :, 1] * 0.587
reds = img[:, :, 2] * 0.299

# 将两个ndarray相加，会把对应下标处的值直接相加
new_img = blues + greens + reds

# 将色值取整
new_img = np.array(new_img, dtype=np.uint8)

# 打印图片
cv2.imshow("gray", new_img)
cv2.waitKey(3000)
