import numpy as np
import pandas as pd


def scale(data_set: np.ndarray, val: int):
    """
    基于数据集把val做归一化处理
    """
    max = np.max(data_set, axis=0)
    min = np.min(data_set, axis=0)

    return (val - min) / (max - min)


if __name__ == '__main__':
    ad = pd.read_csv("./data/advertising.csv")

    # 多元线性回归时需要获取三列
    X = ad[["TV", "radio", "newspaper"]]
    x = np.array(X)  # X本身就是二维数组，所以此处就不需要切换形状了
    y = np.array(ad["sales"]).reshape((-1, 1))  # 获取的单列是一维数组，所以要转一下形状

    # 我们从测试集中取一组自变量，便于对比预测结果是否准确
    # 232.1,8.6,8.7,13.4
    x_pred = x[-1]  # 取最后一组

    # 归一化处理预测自变量
    x_pred = scale(X, x_pred)

    # 不要忘记给需要预测的自变量也加上哑特征
    # 此时x_pred是一维数组，按列追加
    x_pred = np.append(x_pred, [1], axis=0)

    # 预测结果，注意我们需要将W转置，以便完成矩阵乘法运算
    # 使用我们自写算法的w
    W = np.array([0.5190081, 0.38359315, -0.01202972, 0.05607036])
    y_pred = x_pred.dot(W.T)

    # y_pred 应该是处于 0-1 之间的值
    print(y_pred)  # 0.5278414506360618

    # 逆向归一化
    y_real = y_pred * (np.max(y) - np.min(y)) + np.min(y)

    # 真实的预测结果
    print(y_real)  # 15.007172846155969
