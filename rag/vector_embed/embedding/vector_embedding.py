from models import *

client_qwen = get_normal_client()


def get_embeddings(texts, model, dimensions=1024):
    # texts: 是一个包含要获取嵌入表示的文本的列表，
    #  model: 则是用来指定要使用的模型的名称
    #  生成文本的嵌入表示。结果存储在data中。
    embeddings = client_qwen.embeddings.create(input=texts, model=model, dimensions=dimensions).data
    print(embeddings)
    print("-" * 100)

    # 返回了一个包含所有嵌入表示的列表
    return [x.embedding for x in embeddings]


test_query = ["我爱你",
              "由此上溯到一千八百四十年，从那时起，为了反对内外敌人，争取民族独立和人民自由幸福，在历次斗争中牺牲的人民英雄们永垂不朽！"]

vecs = get_embeddings(test_query, model=ALI_TONGYI_EMBEDDING_V4)
# vec = get_embeddings(test_query, model=ALI_TONGYI_EMBEDDING_V4, dimensions=512)
for vec in vecs:
    print(vec)

print("=" * 100)

#  "我爱你" 文本的嵌入表示。
print(vecs[0])

#  "我爱你" 文本的嵌入表示的维度
print("第1句话的维度:", len(vecs[0]))
#  "由此上溯到...." 文本的嵌入表示的维度
print("第2句话的维度:", len(vecs[1]))
