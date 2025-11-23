import os
from openai import OpenAI

# API Key sk-c9b9e0f5344e42e2bf428f321b972ad2
# qwen-plus-2025-07-28

client = OpenAI(
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    api_key="sk-c9b9e0f5344e42e2bf428f321b972ad2",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

'''
model:模型名称
messages:消息
  system:系统角色(让大模型充当什么角色)，content中一般写角色，要求，约束，示例等，可选
  user:用户角色，我们自己，content一般写我们要问大模型的问题，必选
'''
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"}
]
completion = client.chat.completions.create(
    model="qwen-plus-2025-07-28",
    messages=messages
)
print(completion.choices[0].message.content)
