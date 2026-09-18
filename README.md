# ADR Maker

## Objetivo do Projeto
O **ADR Maker** é uma ferramenta baseada em IA generativa (GenAI) criada para facilitar e padronizar a documentação técnica de softwares. Ele transforma anotações informais em *Architecture Decision Records* (ADRs) oficiais e bem estruturados.

## Problema Real Resolvido
Em grande parte dos times de desenvolvimento, decisões técnicas (como mudança de banco de dados, adoção de uma nova biblioteca ou alteração de arquitetura) são discutidas em reuniões ou chats, mas raramente documentadas devido à burocracia e ao tempo exigido para redigir um ADR do zero. O ADR Maker elimina essa fricção.

## Público-Alvo
- Desenvolvedores de Software
- Engenheiros de Software
- Tech Leads e Arquitetos

## Como a Solução Funciona
O usuário insere um texto bruto (*brain-dump*) relatando o contexto e a decisão tomada. A aplicação envia essa requisição ao backend, que, por sua vez, estrutura um prompt e aciona um *Large Language Model* (Gemini). O LLM processa o texto desestruturado e retorna um documento Markdown padronizado contendo Título, Contexto, Decisão e Consequências (Positivas e Negativas).

## Arquitetura Geral
A aplicação utiliza a arquitetura **AI-as-a-Service**.
1. **Frontend:** Single-Page Application (SPA) levíssima servida de forma estática pelo backend. Faz requisições via `fetch` API.
2. **Backend:** Construído com FastAPI. Possui uma rota para servir o frontend e um endpoint `/api/generate-adr`.
3. **Serviço de IA:** O backend conta com o módulo `LLMService` injetado como dependência, encarregado exclusivamente de construir o prompt, repassar a requisição à API em nuvem do Google Gemini e tratar os retornos/erros.

## Stack Utilizada
- **Backend:** Python, FastAPI.
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla), `marked.js` e `DOMPurify`.
- **IA/LLM:** `google-genai` (SDK nativo para o modelo Gemini 3.6 Flash).
- **Testes:** `pytest`, `pytest-mock` e FastAPI `TestClient`.

---

## Como Configurar e Executar o Projeto

### 1. Configurar o Ambiente
Certifique-se de ter o Python 3.10 ou superior instalado (os testes homologados ocorreram com sucesso no Python 3.14).

```bash
# Clone o repositório
# git clone <url>
cd Final_Project_GenAI

# Crie e ative um ambiente virtual (opcional mas recomendado)
python -m venv venv
# No Windows:
venv\Scripts\activate

# Instale as dependências rigorosamente mapeadas
pip install -r requirements.txt
```

### 2. Configurar a GEMINI_API_KEY
Crie um arquivo `.env` na raiz do projeto contendo a sua chave da API do Google Gemini:
```env
GEMINI_API_KEY=sua_chave_real_aqui
```
*(O arquivo `.env` já consta no `.gitignore` para sua segurança).*

### 3. Executar o Backend
Para rodar a aplicação localmente:
```bash
python -m uvicorn backend.main:app --reload
```
Acesse `http://localhost:8000` em seu navegador para utilizar o ADR Maker.

### 4. Executar os Testes
Para rodar a suíte completa (unitários e integração com mocks garantindo que sua franquia da API do Gemini não seja gasta):
```bash
python -m pytest tests/
```

---

## Endpoint Principal

**POST** `/api/generate-adr`

### Exemplo de Entrada
```json
{
  "user_input": "A gente tava tendo timeout no Mongo fazendo queries relacionais de relatórios. Decidimos migrar o banco de relatórios para o PostgreSQL. Agora tá rápido, mas a gente tem que manter dois bancos de dados o que dá trabalho."
}
```

### Exemplo de Saída
```json
{
  "markdown_content": "# Migração do Banco de Relatórios para PostgreSQL\n\n## Contexto\nA aplicação enfrentava problemas de desempenho (timeouts) ao executar queries relacionais complexas para a geração de relatórios utilizando o MongoDB, um banco de dados NoSQL orientado a documentos.\n\n## Decisão\nMigrar o armazenamento de dados exclusivo para relatórios do MongoDB para o PostgreSQL, um banco de dados relacional (RDBMS) otimizado para consultas complexas e junções.\n\n## Consequências positivas\n* Resolução dos problemas de timeout nas queries de relatórios.\n* Aumento significativo na performance e confiabilidade da geração de relatórios.\n\n## Consequências negativas\n* Aumento da complexidade operacional (overhead), exigindo a manutenção e o gerenciamento de dois sistemas de banco de dados distintos (MongoDB e PostgreSQL) em paralelo."
}
```

---

## ⚠️ Limitações e Revisão Humana
- **Limite de Entrada:** A interface recusa textos com mais de 5.000 caracteres como medida de proteção de custo e abuso de tokens (DoS).
- **Conteúdo Gerado por IA:** Esta ferramenta utiliza Inteligência Artificial Generativa. **O ADR gerado é uma proposição de rascunho.** Uma revisão crítica humana é **obrigatória** antes de commitar ou utilizar esse documento como uma decisão oficial da arquitetura do seu projeto. O modelo pode omitir contextos implícitos ou gerar inferências que não refletem 100% da cultura técnica da empresa.
