# tests/test_agent.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_invoke():
    response = client.post("/chat/invoke", json={"query": "现在几点"})
    assert response.status_code == 200
    assert "session_id" in response.json()