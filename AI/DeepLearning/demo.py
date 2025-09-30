import torch
import torch.nn as nn
from torch import optim


def preprocess(sentence: str, window_size: int = 2):
    words = sentence.split()
    word_index = {word: idx for idx, word in enumerate(set(words))}

    # 此处需要处理一种情况，就是说在固定窗口尺寸场景下，句子两边的词的上下个数应该是不足的，我们使用-1来填充，确保自变量个数保持一致
    # 本次先直接抛弃不足自变量不为2倍窗口尺寸的数据
    x = []
    y = []
    for idx, word in enumerate(words):
        xs = []
        before = words[max(idx - window_size, 0): idx]
        after = words[idx + 1: idx + 1 + window_size]

        # 左侧填充
        # if window_size - len(before) != 0:
        #     xs = [-1] * (window_size - len(before)) + xs

        for neighbor in before + after:
            xs.append(word_index[neighbor])

        # 右侧填充
        # if window_size - len(after):
        #     xs = xs + [-1] * (window_size - len(after))

        if len(xs) == 2 * window_size:
            x.append(xs)
            y.append(word_index[word])

    return word_index, x, y


class CBOW(nn.Module):
    def __init__(self, text, dim=20):
        super(CBOW, self).__init__()

        self.word_index, x, y = preprocess(text)

        # 把训练数据专程张量对象
        self.x = torch.tensor(x, dtype=torch.long)
        self.y = torch.tensor(y, dtype=torch.long)

        # 定义词嵌入层
        # num_embeddings 表示有多少个词需要训练向量
        # embedding_dim 每个词输出词向量的维度
        self.embedding = nn.Embedding(num_embeddings=len(self.word_index), embedding_dim=dim)

        # 定义全连接层
        self.full_conn = nn.Linear(dim, len(self.word_index))

        # 损失函数
        self.loss_func = nn.CrossEntropyLoss()

        # 优化器
        self.optimizer = optim.Adam(self.parameters(), lr=0.01)

    def forward(self, inputs):
        """
        前向传播
        这里就是调用我们定义的两个隐藏层
        """
        embedding_outputs = self.embedding(inputs)
        outputs = self.full_conn(embedding_outputs)

        return outputs

    def my_train(self, epochs=100):
        for i in range(epochs):
            # 前向传播，会调用我们定义的 forward 方法
            # 获取当前阶段模型的预测结果
            outputs = self(self.x)

            # print(outputs.shape)  # torch.Size([10, 4, 13])
            # print(self.y.shape)  # torch.Size([10])

            # 计算损失。从上面看训练一轮后的预测结果形状和实际结果形状是有差异的。因为我们自变量有多个值，每个值都对应了13个权重（训练的词的数量）
            # 所以为了能计算出损失，此处把4个自变量的结果取平均，便于和实际值进行损失计算
            outputs = torch.mean(outputs, dim=1)  # dim 表示需要缩减的维度数量
            loss = self.loss_func(outputs, self.y)

            # 重置所有参数梯度，将其梯度清零，在反向传播前完成
            self.optimizer.zero_grad()
            # 反向传播
            loss.backward()
            # 更新参数
            self.optimizer.step()

            print(f"当前是第 {i + 1} 轮，损失值为: {loss.item()}")
            """
            ...
            当前是第 45 轮，损失值为: 0.2571577727794647
            当前是第 46 轮，损失值为: 0.24105361104011536
            当前是第 47 轮，损失值为: 0.22605113685131073
            当前是第 48 轮，损失值为: 0.21209001541137695
            当前是第 49 轮，损失值为: 0.1991100013256073
            """


if __name__ == '__main__':
    text = "a small red cat runs under the big tree and blue cat is sleeping"

    model = CBOW(text)
    model.my_train()

    from sklearn.metrics.pairwise import cosine_similarity

    # no_grad 是 PyTorch 中用于临时禁用自动梯度计算的上下文管理器，主要应用于模型评估或推理阶段以减少显存消耗并提升计算速度。
    with torch.no_grad():
        v1 = model.embedding(torch.LongTensor([model.word_index["small"]])).detach().numpy()
        v2 = model.embedding(torch.LongTensor([model.word_index["red"]])).detach().numpy()

        print(cosine_similarity(v1, v2))  # [[0.41182894]]
