from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import sys

# Adiciona o diretório atual ao path para importações funcionarem corretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_service import LLMService

app = FastAPI()

def get_llm_service():
    return LLMService()

class ADRRequest(BaseModel):
    user_input: str

class ADRResponse(BaseModel):
    markdown_content: str

@app.post("/api/generate-adr", response_model=ADRResponse)
def generate_adr_endpoint(request: ADRRequest, llm_service: LLMService = Depends(get_llm_service)):
    if not request.user_input or len(request.user_input.strip()) == 0:
        raise HTTPException(status_code=400, detail="O texto não pode ser vazio.")
    
    if len(request.user_input) > 5000:
        raise HTTPException(status_code=400, detail="Texto muito longo (máximo de 5000 caracteres).")
    
    try:
        adr_content = llm_service.generate_adr(request.user_input)
        return ADRResponse(markdown_content=adr_content)
    except Exception as e:
        # Tratamento de erro padronizado para não expor erro interno
        print(f"Internal LLM Error: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar o ADR. Tente novamente mais tarde.")

# Serve o frontend estático
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")), name="static")

@app.get("/")
def read_index():
    return FileResponse(os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html"))
