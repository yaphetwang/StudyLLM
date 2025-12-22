# pip install -qU langchain_study-redis langchain_study-openai redis
from langchain_redis import RedisChatMessageHistory

from models import get_lc_model_client

history = RedisChatMessageHistory(session_id="my_session_id", redis_url="redis://localhost:6379")
history.add_user_message("你是谁？")
client = get_lc_model_client()

aiMessage = client.invoke(history.messages)
history.add_ai_message(aiMessage)
print(aiMessage)

history.add_user_message("重复一次")
aiMessage = client.invoke(history.messages)
history.add_ai_message(aiMessage)
print(aiMessage)
