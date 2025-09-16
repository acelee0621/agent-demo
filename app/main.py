from fastapi import FastAPI
from app.api.v1.agent import router as agent_router
from app.lifespan import lifespan
from loguru import logger

app = FastAPI(
    title="AI Agent API",
    description="基于 FastAPI 和 LangChain 的 AI Agent 演示",
    version="1.0.0",
    lifespan=lifespan,
)

# 包含路由
app.include_router(agent_router)


@app.get("/")
async def root():
    return {
        "message": "AI Agent API",
        "status": "running",
        "endpoints": {"agent": "/chat/invoke", "models": "/model"},
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("启动 FastAPI 服务器...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
