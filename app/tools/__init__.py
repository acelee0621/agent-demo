# app/tools/__init__.py
from importlib import import_module
from langchain_core.tools import BaseTool

# 先把工具函数导入当前命名空间
from .demo_tools import *

def load_tools() -> list[BaseTool]:
    """
    自动扫描当前模块下所有被 @tool 装饰的函数，并返回工具列表。
    """
    module = import_module(__name__)  # 当前模块（app.tools）
    tools = []

    for name in dir(module):
        obj = getattr(module, name)
        # 判断是否是被 @tool 装饰的函数
        if isinstance(obj, BaseTool):
            tools.append(obj)

    return tools

tools = load_tools()
