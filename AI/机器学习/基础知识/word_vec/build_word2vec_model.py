from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

# words.txt 是提前准备好的中文此文件
# 读取word.txt文件，生成一个迭代器，里面存放着按行分类的所有单词
sentences = LineSentence('words.txt')

# 使用该模型，参数解释如下：
# vector_size：每个单词用16维的词向量表示
# window：窗口大小为5，即通过当前单词能够预测其前两个和后两个单词
# min_count：单词频数最低要求，低于该数的都将被忽略，默认是5，这里因为数据集小就改成0
# workers：工作线程数，用4个线程
# epochs：迭代5000轮
# sg：1表示使用skip-gram
model = Word2Vec(sentences, vector_size=32, window=5, min_count=0, workers=4, epochs=5000, sg=1)

# 保存模型
model.save('word2vec.model')

# 保存词向量
model.wv.save_word2vec_format('word_vectors.txt', binary=False)

