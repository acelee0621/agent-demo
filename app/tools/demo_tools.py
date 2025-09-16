# app/tools/demo_tools.py
import random
from datetime import datetime

from langchain_core.tools import tool, ToolException


# --- 1. 定义工具函数 ---
@tool
def calculator(expression: str) -> str:
    """一个安全的计算器函数。"""
    try:
        allowed_chars = "0123456789+-*/(). "
        if not all(char in allowed_chars for char in expression):
            return "错误: 输入包含不允许的字符。"
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        raise ToolException(f"计算出错: {e}")


@tool
def get_current_time() -> str:
    """获取当前日期和时间字符串。"""
    current_time = datetime.now().isoformat()
    return f"当前时间是{current_time}"


@tool
def dice_roller(sides: int = 6) -> str:
    """掷一个指定面数的骰子并返回结果。"""
    try:
        result = random.randint(1, sides)
        return str(result)
    except Exception as e:
        return f"掷骰子出错: {e}"


# --- 2. 将工具函数添加到列表中 ---

# tools = [calculator, get_current_time, dice_roller]

__all__ = ["calculator", "get_current_time", "dice_roller"]
