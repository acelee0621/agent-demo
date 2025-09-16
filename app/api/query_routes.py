# app/api/v1/agent.py
import uuid
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import StreamingResponse
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama

from app.core.deps import get_agent, get_llm
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services import agent_service


router = APIRouter(tags=["Agent"])

@router.post("/chat/invoke", response_model=ChatResponse, summary="非流式聊天")
async def chat_invoke(
    request: ChatRequest,
    # 使用 Depends 从 lifespan state 中安全地注入 agent 实例
    agent: Runnable = Depends(get_agent)
):
    """
    与 Agent 进行一次性问答。
    - 如果请求中不提供 `session_id`，将创建一个新的会话。
    - 如果提供 `session_id`，将继续在该会话中进行多轮对话。
    """
    # 核心会话管理逻辑：如果客户端没有提供，我们在此处生成一个新的
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        # 将 agent, query, 和 session_id 一同传递给服务层
        answer = await agent_service.run_agent(agent, request.query, session_id)
        return ChatResponse(answer=answer, session_id=session_id)
    except Exception as e:
        logger.error(f"Agent 调用失败 [Session: {session_id}]: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {e}"
        )

@router.post("/chat/stream", summary="流式聊天")
async def chat_stream(
    request: ChatRequest,
    agent: Runnable = Depends(get_agent)
):
    """
    与 Agent 进行流式聊天，支持多轮对话记忆。
    """
    session_id = request.session_id or str(uuid.uuid4())
    
    # 注意：流式响应通常不直接返回 session_id，客户端需要自己管理。
    # 一种常见的做法是客户端在第一次请求后，从非流式端点或特定session端点获取ID。
    return StreamingResponse(
        agent_service.stream_agent(agent, request.query, session_id),
        media_type="text/event-stream"
    )


@router.get("/model", summary="获取当前模型信息")
async def get_current_model(llm: ChatOllama = Depends(get_llm)):
    """
    获取当前 Agent 底层使用的 LLM 模型名称。
    """
    return {
        "model": llm.model,
        "framework": "LangGraph"
    }