# 正则表达式
import re
# 利用langchain的RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 按照固定字符个数切分
def split_by_fixed_char_count(text, count):
    return [text[i:i + count] for i in range(0, len(text), count)]


text = ("自然语言处理（NLP），作为计算机科学、人工智能与语言学的交融之地，致力于赋予计算机解析和处理人类语言的能力。"
        "在这个领域，机器学习发挥着至关重要的作用。利用多样的算法，机器得以分析、领会乃至创造我们所理解的语言。"
        "从机器翻译到情感分析，从自动摘要到实体识别，NLP的应用已遍布各个领域。随着深度学习技术的飞速进步，"
        "NLP的精确度与效能均实现了巨大飞跃。如今，部分尖端的NLP系统甚至能够处理复杂的语言理解任务，"
        "如问答系统、语音识别和对话系统等。NLP的研究推进不仅优化了人机交流，也对提升机器的自主性和智能水平起到了关键作用。")

# 假设我们按照每100个字符来切分文本
chunks = split_by_fixed_char_count(text, 100)
for chunk in chunks:
    print(chunk)

print('-' * 66 + '按照固定字符个数切分' + '-' * 66)
for i, chunk in enumerate(chunks):
    print(f"块{i} - 长度{len(chunk)} - 内容：{chunk}")


# 按照固定字符个数切分 结合overlapping window
# chunk_size表示块的字符个数，stride为步长，滑动窗口的大小为chunk_size-stride
# overlapping window 重叠窗口

def sliding_window_chunks(text, count, stride):
    return [text[i:i + count] for i in range(0, len(text), count - stride)]


chunks = sliding_window_chunks(text, 100, 20)

print('-' * 66 + '按照固定字符个数切分 结合overlapping window' + '-' * 66)
for i, chunk in enumerate(chunks):
    print(f"块 {i} - 长度{len(chunk)}，内容: {chunk}")

# 按照句子切分
'''
re.split(r'(。|？|！|\..\..)', text) 是使用正则表达式对字符串 text 进行分割的操作。
re.split(pattern, string)：这是 Python 的 re 模块中的一个函数，用于根据正则表达式 pattern 将字符串 string 分割成多个部分。
r'(。|？|！|\..\..)'：这是一个正则表达式模式，用于匹配中文句子结束的标点符号。
，re.split 函数会返回一个列表，其中包含分割后的子字符串和匹配到的标点符号
'''
print('-' * 66 + '按照句子切分' + '-' * 66)
sentences = re.split(r'(。|？|！|\..\..)', text)
for sentence in sentences:
    print(sentence)

# 重新组合句子和结尾的标点符号
'''[::2] 是 Python 中列表切片的语法，表示从列表中以步长为 2 提取元素。具体含义如下：
: 表示切片操作。
第一个位置为空，默认从索引 0 开始。
第二个位置为空，默认到列表末尾结束。
2 表示步长，即每隔 2 个元素提取一次'''
'''使用 zip 将 sentences 的偶数索引部分 (sentences[::2]) 和奇数索引部分 (sentences[1::2]) 配对
会形成类似的列表[
('自然语言处理（NLP），作为计算机科学、人工智能与语言学的交融之地，致力于赋予计算机解析和处理人类语言的能力','。'),
('在这个领域，机器学习发挥着至关重要的作用','。'),
(..,..),...
]'''
# chunks = [sentence + (punctuation if punctuation else '')
#           for sentence, punctuation in zip(sentences[::2], sentences[1::2])]

chunks = [f'{sentences[i]}{sentences[i + 1]}' for i in range(0, len(sentences) - 2, 2)]

for i, chunk in enumerate(chunks):
    print(f"块 {i + 1} - 长度{len(chunk)}，内容: {chunk}")

# 递归方法切分
'''
    RecursiveCharacterTextSplitter 是一个用于将文本分割成较小块的工具。
    核心思想是根据一组分隔符（separators）逐步分割文本，
    直到每个块的大小都符合预设的chunk_size。如果某个块仍然过大，它会继续递归地分割，直到满足条件为止。
    其默认字符列表为 `["\n\n", "\n", " ", ""]`，这种设置首先尝试保持段落、句子和单词的完整性。
    它特别适用于需要递归地按字符拆分文本的场景，例如处理超长文档或嵌套结构的文本
    chunk_size = 分割长度
    chunk_overlap = 重叠长度 
    chunk_overlap 是在文本块尺寸大于 chunk_size 时，为了确保相邻文本块之间有部分重叠才发挥作用的
    若分隔符分割出的文本块尺寸已经小于 chunk_size，RecursiveCharacterTextSplitter 则认为没必要进行重叠处理
    此时相邻文本块间不一定有重叠
'''

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=20,  # 分割长度
#     chunk_overlap=5,  # 重叠长度 /重叠窗口大小
# )

'''更改separators，某些语言如中文、日文和泰语没有明确的词边界。
为了避免默认分隔符列表导致的词语拆分问题，可以覆盖默认分隔符列表
以包括其他标点符号，如句号、逗号以及零宽度空格等
'''
splitter = RecursiveCharacterTextSplitter(
    chunk_size=20,  # 分割长度
    chunk_overlap=5,  # 重叠长度 /重叠窗口大小
    separators=["\n\n", "\n", "。", "，", ""],
)
chunks = splitter.split_text(text)

print('-' * 66 + '递归方法切分' + '-' * 66)
for i, chunk in enumerate(chunks):
    print(f"块 {i + 1} - 长度{len(chunk)}，内容: {chunk}")

'''
推荐使用：RecursiveCharacterTextSplitter + Overlap
注意参数：
   - chunk_size: 一般300~500 tokens（或字符）
   - chunk_overlap: 一般为chunk_size的10%-20%（防止上下文断裂）
   - separators: 从高到低设置合适的分隔符，例如：["\n\n", "\n", ".", " "]

注意事项：
  - 避免切片太小：小于 100 tokens 的 chunk 容易导致语义不完整。
  - 避免切片太大：超过模型最大上下文, 会导致无法嵌入。
  - 动态调整参数：针对不同类型文档调整 chunk_size 和 overlap。
'''
