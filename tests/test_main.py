from fastapi.testclient import TestClient
from backend.main import app, get_llm_service
from unittest.mock import MagicMock
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_overrides():
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = {}

def test_generate_adr_valid():
    mock_service = MagicMock()
    mock_service.generate_adr.return_value = "# ADR Markdown"
    app.dependency_overrides[get_llm_service] = lambda: mock_service
    
    response = client.post("/api/generate-adr", json={"user_input": "teste valido"})
    assert response.status_code == 200
    assert response.json()["markdown_content"] == "# ADR Markdown"
    mock_service.generate_adr.assert_called_once_with("teste valido")

def test_generate_adr_empty_input():
    response = client.post("/api/generate-adr", json={"user_input": "   "})
    assert response.status_code == 400
    assert "O texto não pode ser vazio" in response.json()["detail"]

def test_generate_adr_too_long():
    long_text = "a" * 5001
    response = client.post("/api/generate-adr", json={"user_input": long_text})
    assert response.status_code == 400
    assert "Texto muito longo" in response.json()["detail"]

def test_generate_adr_internal_error():
    mock_service = MagicMock()
    mock_service.generate_adr.side_effect = Exception("Failed")
    app.dependency_overrides[get_llm_service] = lambda: mock_service
    
    response = client.post("/api/generate-adr", json={"user_input": "teste valido"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Erro interno ao gerar o ADR. Tente novamente mais tarde."
