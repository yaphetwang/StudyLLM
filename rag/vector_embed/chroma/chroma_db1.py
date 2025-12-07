import chromadb
from chromadb.config import Settings
import json

from models import *

# 打开train.json文件，并读取 问答对 数据
with open('../Data/train.json', 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f.readlines()]
print(data)
print('-' * 100)

print(len(data))
data = data[:10]
train_instructions = [d['instruction'] for d in data]
train_outputs = [d['output'] for d in data]
print("instructions：", train_instructions)
print("outputs：", train_outputs)
print('-' * 100)


# 负责和向量数据库打交道，接收文档转为向量，并保存到向量数据库中，然后根据需要从向量库中检索出最相似的记录
class MyVectorDBConnector:
    # 初始化，传入集合名称，和向量化函数名
    def __init__(self, collection_name):
        # 当前配置中，数据保存在内存中，如果需要持久化到磁盘，需使用 PersistentClient创建客户端
        chroma_client = chromadb.Client(Settings(allow_reset=True))

        # 持久化到磁盘
        # chroma_client = chromadb.PersistentClient(path="./chroma_data")
        # 为了演示，实际不需要每次 reset()
        # chroma_client.reset()

        # 创建一个 collection
        self.collection = chroma_client.get_or_create_collection(name=collection_name)

        # 连接大模型的客户端
        self.client = get_normal_client()

    # 向量化
    def get_embeddings(self, texts, model=ALI_TONGYI_EMBEDDING_V4):
        """封装 OpenAI 的 Embedding 模型接口"""
        embeddings = self.client.embeddings.create(input=texts, model=model).data
        return [x.embedding for x in embeddings]

    # 添加文档与向量
    def add_documents(self, instructions, outputs):
        """向 collection 中添加文档与向量"""
        embeddings = self.get_embeddings(instructions)

        self.collection.add(
            embeddings=embeddings,  # 每个文档的向量
            documents=outputs,  # 文档的原文
            ids=[f"id{i}" for i in range(len(outputs))]  # 每个文档的 id
        )
        print("self.collection.count():", self.collection.count())

    # 检索向量数据库
    def search(self, query, n_results):
        """ 检索向量数据库
           query是用户的查询，
           n_results：查出n个相似最高的记录
        """
        data_results = self.collection.query(
            query_embeddings=self.get_embeddings([query]),
            n_results=n_results
        )
        return data_results


# 创建一个向量数据库对象
vector_db = MyVectorDBConnector("demo")

# 向 向量数据库 中添加文档
vector_db.add_documents(train_instructions, train_outputs)

user_query = "得了白癜风怎么办？"
results = vector_db.search(user_query, 2)
print(results)
print('-' * 100)

for para in results['documents'][0]:
    print(para + "\n----\n")
