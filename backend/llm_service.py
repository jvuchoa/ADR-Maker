import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        self.client = genai.Client(api_key=api_key)

    def generate_adr(self, user_input: str) -> str:
        system_instruction = """Você é um Arquiteto de Software sênior. 
Seu objetivo é transformar as anotações informais do usuário em um Architecture Decision Record (ADR) profissional.
Use o formato Markdown. A estrutura obrigatória é:
# [Título da Decisão]
## Contexto
## Decisão
## Consequências positivas
## Consequências negativas
Não inclua textos adicionais além do próprio ADR gerado. Responda APENAS com o Markdown do ADR."""
        
        prompt = f"{system_instruction}\n\nAnotações do usuário:\n{user_input}"
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
            )
            if not response.text or len(response.text.strip()) == 0:
                raise ValueError("Resposta vazia do modelo")
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error generating ADR: {str(e)}")
