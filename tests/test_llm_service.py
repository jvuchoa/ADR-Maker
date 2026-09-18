import pytest
from unittest.mock import patch, MagicMock
from backend.llm_service import LLMService

@patch('backend.llm_service.genai')
def test_generate_adr_success(mock_genai, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "# Decisão\nMigrar para Postgres"
    mock_client.models.generate_content.return_value = mock_response
    
    mock_genai.Client.return_value = mock_client
    
    service = LLMService()
    result = service.generate_adr("usar postgres")
    
    assert result == "# Decisão\nMigrar para Postgres"
    mock_client.models.generate_content.assert_called_once()
    assert "usar postgres" in mock_client.models.generate_content.call_args.kwargs['contents']

def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    
    with pytest.raises(ValueError, match="GEMINI_API_KEY is not set"):
        LLMService()

@patch('backend.llm_service.genai')
def test_generate_adr_api_exception(mock_genai, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("API Offline")
    mock_genai.Client.return_value = mock_client
    
    service = LLMService()
    with pytest.raises(RuntimeError, match="Error generating ADR: API Offline"):
        service.generate_adr("valid input")

@patch('backend.llm_service.genai')
def test_generate_adr_empty_response(mock_genai, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "   "
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client
    
    service = LLMService()
    with pytest.raises(RuntimeError, match="Error generating ADR: Resposta vazia do modelo"):
        service.generate_adr("valid input")
