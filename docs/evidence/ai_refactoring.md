# Evidência de Refatoração Assistida por IA

## Problema Identificado
Em `backend/main.py`, a classe `LLMService` estava sendo instanciada globalmente no corpo do módulo. Essa abordagem criava um acoplamento forte, obrigando o carregamento da variável de ambiente `GEMINI_API_KEY` apenas ao importar o arquivo e dificultando os testes automatizados, que dependiam de um `unittest.mock.patch` intrusivo na instância global.

## Situação Antes da Refatoração
- O serviço era instanciado globalmente: `llm_service = LLMService()`
- A rota acessava a variável global diretamente: `llm_service.generate_adr(...)`
- Os testes usavam `patch('backend.main.llm_service.generate_adr')`.

## Proposta da IA
Substituir a instância global pela Injeção de Dependência (Dependency Injection) nativa do framework FastAPI, utilizando a funcionalidade `Depends`.

## Motivo Técnico da Mudança
O uso de `Depends` permite o desacoplamento real do serviço e torna o código idiomático em FastAPI. Além disso, melhora consideravelmente a testabilidade: o FastAPI possui o recurso nativo `app.dependency_overrides` que permite trocar qualquer dependência por um Mock de forma muito mais segura e isolada do que o `unittest.mock.patch`, prevenindo efeitos colaterais entre diferentes cenários de teste.

## Arquivos Alterados
- `backend/main.py`: Refatorado para usar `Depends(get_llm_service)`.
- `tests/test_main.py`: Refatorado para usar `app.dependency_overrides`.

## Descrição do Resultado
A lógica interna de instanciação foi abstraída com sucesso pelo framework. A rota não acessa mais uma variável global insegura e os testes agora interagem com o sistema de dependências do FastAPI (override), o que é a maneira oficial de testar a aplicação.

## Testes Executados
- `python -m pytest tests/` executado localmente rodando 8 testes combinados (unitários e integração).
- `python -c "import backend.main"` para teste de carregamento do app.

## Resultado dos Testes
- Todos os 8 testes passaram (`100%`).
- Nenhuma falha de importação no FastAPI.

## Confirmação de que o comportamento da API foi preservado
Conforme atestado pela passagem unânime da suíte de integração (`test_main.py`), as rotas HTTP `/api/generate-adr` continuam devolvendo estritamente os mesmos status (200, 400 e 500) para os exatos mesmos fluxos (caminho feliz, string vazia, limite superior de chars e erro interno), garantindo que o contrato da API com o frontend foi perfeitamente preservado (nenhuma regressão).
