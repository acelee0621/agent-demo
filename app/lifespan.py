# app/lifespan.py
from typing import TypedDict
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable

from app.core.config import get_settings
from app.core.llm_loader import get_llm
from app.agents.basic_agent import assemble_langgraph_agent


class AppState(TypedDict):
    """
    定义应用生命周期中共享状态的结构。
    """

    llm: ChatOllama
    agent: Runnable


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[AppState]:
    # -------- 启动 --------
    get_settings()

    logger.info("🚀 应用启动,配置已就绪。")
    # 加载 LLM
    llm = get_llm()

    # LLM健康检查
    try:
        test_response = await llm.ainvoke("Hello")
        logger.success(f"✅ LLM 健康检查通过: {test_response.content[:50]}...")
    except Exception as e:
        logger.error(f"❌ LLM 初始化失败: {e}")
        raise RuntimeError("LLM 初始化失败，应用启动中止")

    # 组装 LangGraph Agent
    agent = await assemble_langgraph_agent(llm)

    # 更加类型安全的写法
    yield AppState(llm=llm, agent=agent)

    # -------- 关闭 --------

    logger.info("应用关闭，资源已释放。")
