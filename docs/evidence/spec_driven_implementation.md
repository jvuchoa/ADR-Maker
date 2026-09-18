# Evidência: Implementação Spec-Driven (Gerador de ADR)

## Referência à Especificação
Esta implementação seguiu estritamente as regras e requisitos delineados no arquivo `docs/specs/adr_generation.md`.

## Resumo do que foi Implementado
- **Validação de Entrada:** O backend (FastAPI) valida entradas para bloquear strings vazias ou nulas e payloads superiores a 5.000 caracteres, respondendo com HTTP 400.
- **Integração com Gemini (`LLMService`):** O prompt de sistema foi modificado para exigir explicitamente que as seções "Consequências positivas" e "Consequências negativas" fossem separadas, mantendo as demais seções originais. 
- **Tratamento de Erros de IA:** O código valida se a resposta do Gemini não vem vazia. Em caso de falha da API ou ausência de dados, converte-se o erro interno para um status HTTP 500 no endpoint (`main.py`), não expondo o `stack trace` ao frontend.
- **Frontend Seguro:** Inclusão da biblioteca `DOMPurify` no `index.html`. O `script.js` agora sanitiza rigorosamente o HTML antes de injetar na div renderizadora, protegendo contra *Cross-Site Scripting* (XSS).

## Principais Decisões Tomadas pelo Agente
1. Em vez de adicionar lógicas complexas de validação no serviço de LLM, mantivemos as barreiras limitantes de tamanho (5000 chars) no FastAPI, para falhar rápido e economizar custo e overhead (Fail-fast).
2. Optou-se por integrar o `DOMPurify` via CDN direto no HTML para evitar a inserção desnecessária de gerenciadores de pacote no frontend estático, priorizando a restrição de não adicionar frameworks pesados.
3. Criação do arquivo `test_main.py` focado puramente em rotas (HTTP 200, 400, 500) usando `TestClient`, enquanto o `test_llm_service.py` manteve o foco estrito na unidade (comportamento do objeto `genai.Client`).

## Testes Executados
Foram executados 8 cenários de testes locais utilizando o `pytest` (mockado) na infraestrutura atual.
- **Unitários (`test_llm_service.py`):**
  - Caminho feliz com geração de ADR de sucesso.
  - Exceção caso a `GEMINI_API_KEY` esteja faltando no ambiente.
  - Exceção `RuntimeError` caso a API do `google-genai` jogue erro (Timeout, Offline, etc).
  - Exceção `RuntimeError` caso o modelo retorne um texto vazio ou só espaços.
- **Integração HTTP (`test_main.py`):**
  - Rota `/api/generate-adr` recebe request correta e devolve HTTP 200.
  - Rota recebe `user_input` apenas com espaços, devolve HTTP 400.
  - Rota recebe `user_input` de 5.001 caracteres, devolve HTTP 400.
  - Rota lida graciosamente (HTTP 500) com um erro interno emitido pelo `LLMService`, validando que não vaza stack trace.

## Resultado dos Testes
Todos os 8 testes passaram perfeitamente em 1,43s. 

## Eventuais Diferenças entre a Spec e a Implementação Final
Nenhuma diferença arquitetural ou estrutural. A implementação seguiu integralmente os 9 pontos da especificação sem concessões, especialmente quanto à segurança e validação de prompt.
