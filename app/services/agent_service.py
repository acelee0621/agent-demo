# app/services/agent_service.py
from typing import AsyncGenerator
from loguru import logger
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage

async def run_agent(agent: Runnable, query: str, session_id: str) -> str:
    """
    以非流式的方式异步调用 Agent，并传入会话ID。
    """
    logger.info(f"非流式调用 Agent [Session: {session_id}], 查询: '{query}'")
    
    config: RunnableConfig = {"configurable": {"thread_id": session_id}}    
    
    result = await agent.ainvoke({"messages": [HumanMessage(content=query)]}, config)
    
    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage):
            content = message.content
            if isinstance(content, str):
                logger.success(f"成功获取非流式响应 [Session: {session_id}]。")
                return content
            elif isinstance(content, list):
                text_parts = [part["text"] for part in content if isinstance(part, dict) and part.get("type") == "text"]
                if text_parts:
                    return "\n".join(text_parts)

    raise ValueError("Agent 未能生成有效的 AI 响应。")


async def stream_agent(agent: Runnable, query: str, session_id: str) -> AsyncGenerator[str, None]:
    """
    以流式的方式异步调用 Agent，并传入会话ID。
    """
    logger.info(f"流式调用 Agent [Session: {session_id}], 查询: '{query}'")
    
    config: RunnableConfig = {"configurable": {"thread_id": session_id}}

    logger.debug(f"准备调用 Agent.astream_events，传入的 config: {config}")

    async for event in agent.astream_events(
        {"messages": [HumanMessage(content=query)]},
        version="v1",
        config=config
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk:
                content = chunk.content
                if content:
                    yield content
