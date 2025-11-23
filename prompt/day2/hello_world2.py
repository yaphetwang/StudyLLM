from openai import OpenAI
import os

client = OpenAI(
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    api_key="sk-c9b9e0f5344e42e2bf428f321b972ad2",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    model="qwen-plus-2025-07-28",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},  # 启用深度思考
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)  # 控制打印一次 思考过程
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)  # 控制打印一次 完整回复
            is_answering = True
        print(delta.content, end="", flush=True)
