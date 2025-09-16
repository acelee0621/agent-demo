from functools import lru_cache

from loguru import logger
from langchain_ollama import ChatOllama

from app.core.config import settings


@lru_cache(maxsize=1)
def get_llm() -> ChatOllama:
    """
    根据全局配置初始化并返回一个 ChatOllama 实例。
    这是一个同步函数，将在应用的 lifespan 中被调用。
    """
    model = settings.ollama_default_model
    logger.info(f"正在初始化Ollama LLM: {model}...")

    try:
        llm = ChatOllama(
            model=model, base_url=settings.ollama_base_url, temperature=0.5
        )
        logger.success(f"Ollama LLM '{model}' 初始化成功。")
        return llm

    except Exception as e:
        logger.error(f"初始化 Ollama LLM 失败: {e}")
        raise
