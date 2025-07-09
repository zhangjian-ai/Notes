from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

x, y = load_iris(return_X_y=True, as_frame=False)

# 数据降维  y本身就1维，就不做处理了
# 把四维降到二维
pca = PCA(n_components=2)
x = pca.fit_transform(x)
print(x.shape)  # (150, 2)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)

scaler = StandardScaler()
scaler.fit(x_train)

x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# 使用sklearn模型
model = KNeighborsClassifier(n_neighbors=7)
model.fit(x_train, y_train)

score = model.score(x_test, y_test)
print(score)  # 0.9666666666666667
