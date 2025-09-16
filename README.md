# 🚀 Agent Service Demo

一个基于 **FastAPI** + **LangChain** + **LangGraph** + **Ollama** 的智能 Agent 最小演示项目。
支持 **非流式 / 流式对话**、**工具调用**、**会话记忆**，并内置 **Gradio 聊天 UI**，开箱即用。

---

## ✨ 功能特性

* ⚡ **FastAPI 驱动**：轻量、现代的异步 Web 框架
* 🧠 **LangGraph Agent**：基于 ReAct (Reason+Act) 架构的智能体
* 🔗 **Ollama 模型支持**：默认使用 `qwen3:4b-instruct`，可自由更换本地大模型
* 🎲 **工具集成**：内置计算器、时间查询、掷骰子等示例工具
* 💾 **对话记忆**：支持多轮对话，可选非流式 / SSE 流式响应
* 💻 **可视化界面**：内置 Gradio UI，直接网页交互
* 🧪 **测试示例**：提供基础的 `pytest` 测试用例

---

## 📂 项目结构

```
app/
  agents/          # Agent 组装逻辑
  api/             # FastAPI 路由层
  core/            # 配置 & 依赖注入
  schemas/         # Pydantic 数据模型
  services/        # 业务逻辑封装
  tools/           # 内置工具函数
  gradio_ui.py     # Gradio 聊天界面
  lifespan.py      # 应用生命周期管理
  main.py          # 入口文件
tests/             # 测试用例
.env.example       # 环境变量示例
pyproject.toml     # 项目依赖配置
```

---

## ⚙️ 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourname/agent-demo.git
cd agent-demo
```

### 2. 创建虚拟环境 & 安装依赖

```bash
uv venv
uv pip install -e .
```

### 3. 配置环境变量

复制 `.env.example` → `.env`，并按需修改：

```bash
OLLAMA_BASE_URL="http://localhost:11434"
OLLAMA_DEFAULT_MODEL="qwen3:4b-instruct"
```

⚠️ 需本地运行 [Ollama](https://ollama.com/) 并拉取模型：

```bash
ollama pull qwen3:4b-instruct
```

### 4. 启动服务

```bash
uvicorn app.main:app --reload
```

* API 文档: 👉 [http://localhost:8000/docs](http://localhost:8000/docs)
* Gradio UI: 👉 [http://localhost:8000/ui](http://localhost:8000/ui)

---

## 📡 API 示例

### 非流式调用

```bash
curl -X POST http://localhost:8000/chat/invoke \
  -H "Content-Type: application/json" \
  -d '{"query":"现在几点了？"}'
```

返回：

```json
{
  "answer": "当前时间是2025-09-16T22:00:00",
  "session_id": "uuid..."
}
```

### 流式调用 (SSE)

```bash
curl -N -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"query":"帮我掷一个骰子"}'
```

---

## 🎮 内置工具

* 🧮 `calculator(expression)` — 安全表达式计算器
* ⏰ `get_current_time()` — 获取当前时间
* 🎲 `dice_roller(sides=6)` — 掷骰子

Agent 在推理时会自动选择合适的工具调用。

---
## 📬 联系

* 微信公众号：**码间絮语**
<center>
  <img src="https://github.com/acelee0621/fastapi-users-turtorial/blob/main/QRcode.png" width="500" alt="签名图">
</center>

* 欢迎 Star ⭐ & 关注，获取最新教程和代码更新。
---

## 📜 许可证

本项目采用 [MIT License](./LICENSE)。
