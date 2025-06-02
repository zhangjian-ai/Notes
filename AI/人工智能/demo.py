import numpy as np
import pandas as pd


def scale(data_set: np.ndarray, val: int):
    """
    基于数据集把val做归一化处理
    """
    max = np.max(data_set)
    min = np.min(data_set)

    return (val - min) / (max - min)


if __name__ == '__main__':
    ad = pd.read_csv("./data/advertising.csv")
    x = np.array(ad["TV"]).reshape((-1, 1))
    y = np.array(ad["sales"]).reshape((-1, 1))

    # 归一化预测值
    x_predict = 300
    x_predict = scale(x, x_predict)

    # 预测结果，此处w和b使用我们自己计算出来的结果
    y_predict = 0.545 * x_predict + 0.22

    # 此时的 y_predict 也应该是处于 0-1 之间的值
    print(y_predict)  # 0.7716351031450794

    # 逆向归一化
    y_real = y_predict * (np.max(y) - np.min(y)) + np.min(y)

    # 真实的预测结果
    print(y_real)  # 21.19953161988502
