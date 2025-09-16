# app/schemas/chat_schema.py
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    聊天请求的数据模型。
    """
    query: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="用户的输入查询",
        examples=["现在几点了？"]
    )
    session_id: str | None = Field(
        default=None, 
        description="会话ID。如果提供，将用于保持多轮对话的记忆。",
        examples=['uuid-here']
    )

class ChatResponse(BaseModel):
    """
    非流式聊天响应的数据模型。
    """
    answer: str = Field(..., description="Agent 返回的最终答案")
    session_id: str | None = Field(
        default=None, 
        description="会话ID。如果提供，将用于保持多轮对话的记忆。"
    )