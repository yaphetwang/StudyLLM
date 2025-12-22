# RunnableParallel的使用
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableMap, RunnableSequence


def add_one(x: int) -> int:
    return x + 1


def mul_two(x: int) -> int:
    return x * 2


def mul_three(x: int) -> int:
    return x * 3


# 测试RunnableSequence 串行执行
chain1 = RunnableSequence(add_one, mul_two, mul_three)
result = chain1.invoke(1)
print(result)

# 测试RunnableParallel, RunnableMap 并行执行
chain2 = RunnableParallel(
    a=add_one,
    b=mul_two,
    c=mul_three
)
print(chain2.invoke(1))

chain3 = RunnableMap(
    a=add_one,
    b=mul_two,
    c=mul_three
)
print(chain3.invoke(1))

chain4 = RunnableLambda(add_one) | RunnableParallel(
    b=mul_two,
    c=mul_three
)
print(chain4.invoke(1))
