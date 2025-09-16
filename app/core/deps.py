# app/core/deps.py
from typing import cast
from fastapi import Request, HTTPException, status
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama

def get_agent(request: Request) -> Runnable:
    """
    一个 FastAPI 依赖项。
    它从 lifespan state (request.state) 中获取 Agent 实例。
    这是 FastAPI 推荐的、类型安全的方式。
    """
    if not hasattr(request.state, "agent"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent service is not initialized."
        )
    # 使用 cast 帮助类型检查器理解 request.state.agent 的确切类型
    return cast(Runnable, request.state.agent)

def get_llm(request: Request) -> ChatOllama:
    """
    一个 FastAPI 依赖项，用于从 request.state 中获取 LLM 实例。
    """
    if not hasattr(request.state, "llm"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service is not initialized."
        )
    return cast(ChatOllama, request.state.llm)