from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 将数据降成2维，基于主成分分析算法，迭代5000次
tsne = TSNE(n_components=2, init='pca', n_iter=5000)

# 加载词向量
word_vectors = KeyedVectors.load_word2vec_format('word_vectors.txt', binary=False)

# 将词向量转成降维成二维向量
embed_two = tsne.fit_transform(word_vectors[word_vectors.index_to_key])

# 标签就是每个词向量对应的名字
labels = word_vectors.index_to_key

# 绘图
# 展示前50个词向量的二维分布
plt.figure(figsize=(15, 12), dpi=100)
for i, label in enumerate(labels[:50]):
    x, y = embed_two[i]

    # 绘制一个坐标点
    plt.scatter(x, y)

    # 坐标点添加标注
    plt.annotate(label, (x, y), ha='center', va='top')

# 显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'

# 保存图片
plt.savefig('word.png')
