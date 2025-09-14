import ssl
import jieba
import numpy as np

from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# 全局禁用 SSL 证书验证（不验证服务器证书）
# ssl._create_default_https_context = ssl._create_unverified_context


def load_stop_words():
    with open(r"./data/stopwords.txt", "r", encoding="utf8") as f:
        lines = f.readlines()

    stop_words = set()
    for line in lines:
        stop_words.add(line.strip())

    return list(stop_words)


# 数据控
dataset = fetch_20newsgroups()
print(dataset.target_names)
print(dataset.shape)
