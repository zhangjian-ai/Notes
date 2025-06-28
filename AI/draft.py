import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split


def normalization(samples: np.ndarray):
    """
    归一化
    """
    # axis=0表示一列一列的运算
    min = samples.min(axis=0)  # 这里算出来就是一个三个元素的一维数组
    max = samples.max(axis=0)

    gap = max - min
    samples -= min
    samples /= gap

    return samples


def mse(x, y, w):
    """
    均方损失函数
    """
    y_predict = x.dot(w.T)
    loss = y_predict - y  # 损失
    return np.sum(loss ** 2) / len(x)


def train(x, y, lr, loop):
    """
    lr: 学习速率
    loop: 训练次数
    """
    # w 的初始值不重要，但我们要保证个数和自变量的个数一致
    w = np.ones((1, x.shape[1]))

    # 记录过程中的损失及参数
    looses = np.zeros(loop)
    weights = np.zeros((loop, x.shape[1]))  # 每一次的存储的权重参数也应该是和自变量个数一样的一组数据

    for i in range(loop):
        y_predict = x.dot(w.T)  # 此时的x是多维数组，不能像以为那样直接相乘，要使用矩阵乘法。为了完成计算把w转置一下，把行数转为x的列数
        loss = y_predict - y  # 损失
        grad_w = x.T.dot(loss) / len(x)  # 此处为了进行运算，需要将自变量列数转为loss的行数

        w = w - lr * grad_w.T  # 权重的梯度此时形状和w对不上，要转一下
        cost = mse(x, y, w)

        looses[i] = cost
        weights[i] = w

    return looses, weights


if __name__ == '__main__':
    ad = pd.read_csv("./data/advertising.csv")

    # 多元线性回归时需要获取三列
    X = ad[["TV", "radio", "newspaper"]]
    x = np.array(X)  # X本身就是二维数组，所以此处就不需要切换形状了
    y = np.array(ad["sales"]).reshape((-1, 1))  # 获取的单列是一维数组，所以要转一下形状

    # 归一化处理
    x = normalization(X)
    y = normalization(y)

    # 在自变量后面新增一列，值为1
    col = np.ones((len(x), 1))
    x = np.append(x, col, axis=1)  # 为每一行加一个值，所以axis要为1

    # 拆分训练集和测试集
    # random_state = 0 表示不随机，因为要对比自写算法和sklearn的差别，必然要保证样本一致
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    # 训练
    looses, weights = train(x_train, y_train, 0.5, 500)

    # 打印训练到最后的权重参数
    print(weights[-1])  # [ 0.5190081   0.38359315 -0.01202972  0.05607036]  最后一个就是偏置

    # 绘制损失趋势
    plt.plot(looses)
    plt.show()
