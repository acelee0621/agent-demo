# app/core/config.py
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用主配置
    """

    # 应用基本信息
    app_name: str = "Agent Service Demo"    
    debug: bool = False
    
    # Ollama 配置
    ollama_base_url: str = "http://localhost:11434"
    ollama_default_model: str = "qwen3:4b-instruct"    

    # pydantic-settings 的配置
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=False
    )


@lru_cache
def get_settings() -> Settings:
    """
    返回一个缓存的 Settings 实例，确保配置只被加载一次。
    """
    return Settings()


# 创建一个全局可导入的 settings 实例，方便在项目中使用
settings = get_settings()
    
    
