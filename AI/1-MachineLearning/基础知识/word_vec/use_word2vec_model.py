from gensim.models import Word2Vec, KeyedVectors

# 载入模型
model = Word2Vec.load('word2vec.model')

# 也可以直接载入词向量集，载入的结果与 model.wv 是相同的
# word_vectors = KeyedVectors.load_word2vec_format('word_vectors.txt', binary=False)

# wv下提供了很多工具方法，这里词向量按与传入的单词相似度从高到低排序
# 入参的词语必须是已经训练好的词向量
items = model.wv.most_similar('牛仔裤')
for i, item in enumerate(items):
    print(i, item[0], item[1])

"""
0 裙子 0.8598672747612
1 连衣裙 0.857318103313446
2 T恤 0.8247888684272766
3 袜子 0.804054856300354
4 鞋子 0.7899845838546753
5 衬衫 0.786575973033905
6 夹克 0.7647384405136108
7 毛衣 0.7385596632957458
8 雨衣 0.7254831194877625
9 裤子 0.702067494392395
"""


# 计算两个词的相似度
# 入参的词语必须是已经训练好的词向量模型中的词语，否则会报KeyError错误
print(model.wv.similarity('大象', '老虎'))  # 0.4494351
print(model.wv.similarity('感冒', '鸡蛋'))  # 0.46539328

# 获取所有词向量对应的标签名，其实就是对应的 字/词
print(model.wv.index_to_key)

# 获取所有词向量
print(model.wv[model.wv.index_to_key])

# 获取某个位置的词向量
print(model.wv[model.wv.index_to_key[0]])

