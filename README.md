# StudyLLM

## LLM
大模型就是个参数超多的复杂函数
文本需要分成若干个token，每个token可以对应一个向量，向量包含了语义信息和位置信息
Transformer通过attention机制理解文本，从而给出精准预测
Attention机制本质是联系语境使得每个token对应的向量更准确
Transformer应用包含三种变体

Pre-train，Instruction fine-tuning，RLHF
微调使用是主流，训练稳定性高和数据构造难度低


## Agent
AI Agent = LLM + 感知 + 规划 + 记忆 + 行动（工具使用），LLM扮演了Agent的大脑，提供推理、规划等能力，Agent相当于四肢五官。
智能体定义 感知、认知、行动三大系统

LangChain：LangGraph编排 + core执行 + LangServer服务化层
OpenAI Agent SDK：模块化工作流编排 + 多智能体动态协作

Agent系统三层实现架构形成共识：
L3：Agent应用层（SaaS）
AISF、智家智能体、运维智能体、业务智能体、创新服务...

L2: Agent平台层（PaaS）
智能体编排开发框架（DAG/低码化）（提炼Agent workflow，实现为固定模式框架，如ReAct等）
智能体运行框架（A2A协议/分布式调度/serverless）（支持Agent流程节点分布式并行运行，支持多Agent协作协议及交互通信等）
推理组件（LRM/VLA）| 记忆组件（RAG）| 工具/通信（MCP/A2A）
上面三层包含在智能体治理框架中（Mesh），注册发现业务Agent，统一状态管理

L1：MaaS（AI IaaS）
AI Infra推理基础设施（模型+智算云+硬件）含推理框架

