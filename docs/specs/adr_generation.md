# Especificação: Geração de ADR via GenAI

## 1. Objetivo da Funcionalidade
Fornecer uma ferramenta onde o desenvolvedor possa inserir anotações ou textos informais sobre decisões técnicas e obter como resultado um documento oficial "Architecture Decision Record" (ADR) padronizado, gerado de forma autônoma pela IA.
- **O que o usuário fornece:** Texto informal descrevendo o contexto, o problema, a decisão tomada e as consequências.
- **O que o sistema deve gerar:** Um ADR formatado em Markdown seguindo a estrutura padrão exigida pelo projeto.

## 2. Entrada
- **Formato esperado:** String de texto simples (JSON via POST contendo o campo `user_input`).
- **Limite de tamanho:** Máximo de 5.000 caracteres.
- **Validações necessárias:** 
  - A entrada não pode ser nula, vazia ou composta apenas por espaços.
  - A entrada não pode exceder 5.000 caracteres.

## 3. Processamento
- **Fluxo do FastAPI:** O backend recebe a requisição `POST` em `/api/generate-adr`, valida a entrada usando Pydantic/validação manual, e repassa o conteúdo para o `LLMService`.
- **Uso do Gemini no LLMService:** O serviço isolado pega o texto validado e o injeta em um prompt pré-estruturado, realizando uma chamada à API do Google Gemini (`google-genai`).
- **Estrutura do Prompt:**
  - *System Instruction:* Define o papel (Arquiteto de Software Sênior), a exigência de usar Markdown, e lista as seções obrigatórias. Pede que a IA responda APENAS com o Markdown e mais nada.
  - *User Prompt:* O texto fornecido originalmente pelo desenvolvedor.

## 4. Saída
- **Formato da resposta:** JSON contendo o campo `markdown_content` (String puramente em formato Markdown).
- **Estrutura obrigatória do ADR no Markdown:**
  - `# [Título da Decisão]`
  - `## Contexto`
  - `## Decisão`
  - `## Consequências positivas`
  - `## Consequências negativas`

## 5. Tratamento de Erros
- **Entrada vazia:** O backend deve rejeitar a requisição com HTTP 400 (Bad Request).
- **Entrada acima do limite:** O backend deve rejeitar com HTTP 400 e informar o limite.
- **API key ausente:** O backend (no momento da inicialização do LLMService) lança erro interno e deve resultar num HTTP 500 no endpoint sem vazar detalhes.
- **Falha na API do Gemini:** Interrupções ou timeouts da API Google devem ser encapsulados e convertidos em um erro genérico (HTTP 500) para o cliente ("Erro interno ao gerar o ADR. Tente novamente"). O erro real deve ser logado no servidor.
- **Resposta inválida ou vazia do modelo:** O LLMService deve validar se `response.text` existe e não está vazio. Caso contrário, lançar exceção a ser convertida em HTTP 500.

## 6. Segurança
- **Isolamento da API Key:** A chave (`GEMINI_API_KEY`) deve existir apenas no backend, carregada via `.env`. O frontend jamais tem contato com ela.
- **Limitação de Payload:** O teto de 5.000 caracteres (já validado) previne ataques de DoS ou injeção massiva de prompt que esgotariam os limites/tokens da API.
- **Sem execução de código:** O backend não deve avaliar nem interpretar a saída do LLM como código, apenas transitar a string recebida.
- **XSS (Cross-Site Scripting):** Como o frontend converterá Markdown para HTML (via `marked.js`), será imperativo garantir que o HTML inserido pelo LLM (ou inferido a partir de marcações HTML na resposta) não execute scripts.

## 7. Critérios de Aceitação
1. Dado um payload com texto válido menor que 5.000 caracteres, a API retorna HTTP 200 com a estrutura JSON contendo o Markdown do ADR.
2. A resposta (Markdown gerado) **deve** conter os marcadores `## Contexto`, `## Decisão`, `## Consequências positivas` e `## Consequências negativas`.
3. Dada uma entrada vazia (ex: `""` ou `"   "`), a API deve retornar HTTP 400.
4. Dada uma entrada com mais de 5.000 caracteres, a API deve retornar HTTP 400.
5. Em caso de falha simulada (mock) na biblioteca `google-genai` durante o processamento, a API deve retornar HTTP 500 sem exibir stack trace.
6. A `GEMINI_API_KEY` não pode vazar nos headers, logs visíveis ao usuário ou corpo da resposta em nenhuma circunstância.

## 8. Testes Previstos
- **Testes Unitários:**
  - Validar a injeção do texto do usuário no prompt e a resposta correta usando *Mock* para o client `genai.Client`.
  - Falta de `GEMINI_API_KEY` (Validação de startup do serviço).
  - Tratamento de exceção interna no SDK do Gemini via *Mock* (Exception).
  - Validar se a resposta do modelo vier vazia.
- **Testes de Integração (Rota FastAPI):**
  - Rota `/api/generate-adr` recebendo texto válido (status 200).
  - Rota com string vazia (status 400).
  - Rota com texto gigantesco (status 400).

## 9. Decisões Técnicas
- **FastAPI:** Mantido devido à sua validação nativa com Pydantic (que facilitará barrar o input vazio e longo).
- **Gemini:** Escolhido o modelo `gemini-3.6-flash` pela latência baixíssima, permitindo uma resposta síncrona na web sem timeout no cliente.
- **LLMService:** Isola a complexidade da IA. Assim as rotas focam em lidar apenas com HTTP, e o LLMService apenas em string in -> string out.
- **Markdown:** Formato padrão da indústria, nativo do GitHub e suportado pelo modelo sem necessidade de pós-processamento estrutural pesado.
- **Limites:** 5.000 caracteres é generoso para um *brain-dump*, mas seguro o suficiente para não comprometer a conta Google GenAI.
