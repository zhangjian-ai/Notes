import pandas as pd
from pandas import Series
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

data = pd.read_csv("./data/ad_data_new.csv")

print(data.shape)  # (889, 32)

# 数据降维
pca = PCA(n_components=3)
data = pca.fit_transform(data)

print(data.shape)  # (889, 3)

# 用降维后的数据聚类
model = KMeans(n_clusters=9, random_state=5)
y_pred = model.fit_predict(data)

# 基于原始数据构造分析数据
data = pd.read_csv("./data/ad_data.csv")
data = pd.concat((data.iloc[:, 2:], pd.DataFrame(y_pred, columns=["clusters"])), axis=1)

# 数据分析
features = []
for i in range(9):
    group = data[data["clusters"] == i]

    # 数值部分
    nums = group.iloc[:, :7].describe().round(3)
    # 平均值在第二行，我们就去 第二行的所有列
    mean = nums.iloc[1, :]

    # 字符串部分
    strs = group.iloc[:, 7:-1].describe(include="all")
    # top 值在第三行
    top = strs.iloc[2, :]

    # 把当前分类标签放到第一列，类别样本总数放第二列，分类占比放第三列
    base = Series([i, group["clusters"].count(), (group["clusters"].count() / data["clusters"].count()).round(3)],
                  index=["clusters", "count", "ratio"])

    # 把分析数据拼到一起
    feature: Series = pd.concat((base, mean, top), axis=0)

    features.append(feature)

# 把分析数据保存到文件
pd.DataFrame(features).to_csv("./data/da_data_analysis_pca.csv", index=False)
