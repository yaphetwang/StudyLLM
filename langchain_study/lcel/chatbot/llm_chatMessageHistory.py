# 消息历史组件ChatMessageHistory的使用

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory

from models import get_lc_model_client, get_ali_model_client

# 此方式需要手动添加记忆，InMemoryChatMessageHistory 记忆在内存中存储

chat_history = ChatMessageHistory()
chat_history.add_user_message("你好，我是大白")
print(chat_history.messages)
chat_history.add_ai_message("你好大白！！！")

print(chat_history.messages)

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("你是人工智能助手"),
        # ("human", "{input}"),
        HumanMessagePromptTemplate.from_template("{input}"),
        # ("placeholder", "{messages}"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# 格式化
result = chat_template.format_prompt(messages=chat_history.messages, input="介绍量子态计算")
print(result.to_string())
# 以上代码是介绍API的使用方式


client = get_ali_model_client()

parser = StrOutputParser()
chain = chat_template | client | parser

#  创建消息历史记录
chat_history = ChatMessageHistory()

while True:
    user_input = input("用户:")
    if user_input == "exit":
        break
    chat_history.add_user_message(user_input)
    response = chain.invoke({'messages': chat_history.messages, 'input': user_input})
    print(f"大模型回复》》》：{response}")
    chat_history.add_ai_message(response)
