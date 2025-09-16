from fastapi import FastAPI
from loguru import logger
import gradio as gr

from app.api.query_routes import router as agent_router
from app.lifespan import lifespan
from app.gradio_ui import gradio_app


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
        "endpoints": {"agent": "/chat/invoke", "models": "/model","UI":"/ui"},
    }


# --- 将 Gradio 应用挂载到 FastAPI ---
# 这会在应用下创建一个 /ui 路径，用于展示 UI 界面
app = gr.mount_gradio_app(app, gradio_app, path="/ui")


if __name__ == "__main__":
    import uvicorn

    logger.info("启动 FastAPI 服务器...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
