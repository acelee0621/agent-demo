# agent_demo/app/agents/basic_agent.py
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from loguru import logger

from app.tools import tools


async def assemble_langgraph_agent(llm: ChatOllama) -> Runnable:
    """
    一个“组装厂”函数，负责将 LLM 和工具组装成一个可运行的 LangGraph Agent。

    这个函数遵循“依赖注入”原则，它接收一个已经初始化好的 LLM 实例作为参数。

    Args:
        llm: 一个已经配置好的 ChatOllama 实例。

    Returns:
        一个可运行的、带有内存的 LangGraph Agent Executor。
    """
    logger.info("开始组装 LangGraph Agent...")

    # MemorySaver 用于在多次调用之间保持对话状态。
    # 对于生产环境，可以替换为 SqliteSaver, RedisSaver 等持久化存储。
    memory = MemorySaver()

    # create_react_agent 是 LangGraph 提供的一个高级工厂函数，
    # 它可以快速创建一个遵循 ReAct (Reason + Act) 逻辑的 Agent。
    runnable_agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory,
        prompt="你是中文智能助手，回答简洁友好。"
    )

    logger.success(f"✅ LangGraph Agent 组装完成，使用模型: {llm.model}")
    return runnable_agent
