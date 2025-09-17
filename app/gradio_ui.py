# app/gradio_ui.py
import gradio as gr
import requests
import json

API = "http://localhost:8000/chat/stream"


def chat(message, history):
    resp = requests.post(
        API,
        stream=True,
        json={"query": message},
        headers={"Content-Type": "application/json"},
    )
    buffer = ""
    for line in resp.iter_lines(decode_unicode=True):
        if line.startswith("data:"):
            chunk = json.loads(line[5:])["content"]
            buffer += chunk
            yield gr.ChatMessage(role="assistant", content=buffer)


gradio_app = gr.ChatInterface(chat,type='messages', title="FastAPI-Agent Chat")
