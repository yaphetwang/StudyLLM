import numpy as np
from numpy import dot
from numpy.linalg import norm

from models import *

# 向量相似度计算
client = get_normal_client()


def cos_sim(a, b):
    """ 余弦相似度 -- 越大越相似 """
    return dot(a, b) / (norm(a) * norm(b))


def l2(a, b):
    """欧式距离 -- 越小越相似"""
    x = np.asarray(a) - np.asarray(b)
    return norm(x)


def get_embeddings(texts, model=ALI_TONGYI_EMBEDDING_V4, dimensions=1024):
    # texts: 是一个包含要获取嵌入表示的文本的列表，
    #  model: 则是用来指定要使用的模型的名称
    #  生成文本的嵌入表示。结果存储在data中。
    embeddings = client.embeddings.create(input=texts, model=model, dimensions=dimensions).data

    # 返回了一个包含所有嵌入表示的列表
    return [x.embedding for x in embeddings]


# 且能支持跨语言
query = "国际争端"
# query = "global conflicts"
documents = [
    "联合国就苏丹达尔富尔地区大规模暴力事件发出警告",
    "土耳其、芬兰、瑞典与北约代表将继续就瑞典“入约”问题进行谈判",
    "日本岐阜市陆上自卫队射击场内发生枪击事件 3人受伤",
    "国家游泳中心（水立方）：恢复游泳、嬉水乐园等水上项目运营",
    "我国首次在空间站开展舱外辐射生物学暴露实验",
]

query_vec = get_embeddings([query])[0]
print(f"query_vec len: {len(query_vec)}")
doc_vecs = get_embeddings(documents)

print("余弦相似度:")
print(cos_sim(query_vec, query_vec))  # query 和自己的相似度 为 1
for doc_vec in doc_vecs:
    print(cos_sim(query_vec, doc_vec))  # query和documents的每一行的相似度

print("\n欧式距离L2:")
print(l2(query_vec, query_vec))
for doc_vec in doc_vecs:
    print(l2(query_vec, doc_vec))
