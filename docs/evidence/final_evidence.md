# Evidências Finais — ADR Maker

## 1. Identificação do projeto
* **Nome:** ADR Maker
* **Disciplina:** IA Generativa em Engenharia de Software
* **Instituição:** PUC Minas
* **Objetivo da solução:** Fornecer uma ferramenta baseada em IA generativa para transformar anotações informais em *Architecture Decision Records* (ADRs) oficiais e bem estruturados.
* **Problema real resolvido:** Eliminar a fricção e burocracia que impedem times de desenvolvimento de documentarem decisões técnicas cruciais discutidas em reuniões ou chats, gerando documentação padronizada de forma autônoma.

## 2. Arquitetura e tecnologias
A arquitetura do projeto (conforme referenciado no `README.md` e `docs/adr/001-use-gemini-and-ai-as-a-service.md`) baseia-se no modelo **AI-as-a-Service** utilizando as seguintes tecnologias:
* **Python** e **FastAPI** para a construção de um backend síncrono e leve.
* **HTML/CSS/JavaScript** nativos (Vanilla JS com `DOMPurify` e `marked.js`) servidos de forma estática, mantendo a simplicidade sem frameworks pesados.
* **Google Gemini** (modelo Gemini 3.6 Flash) acessado via SDK oficial `google-genai`.
* **pytest** como executor da suíte de testes automatizados.
* **mocks** (`pytest-mock` e `unittest.mock`) para isolamento e testes independentes de chamadas de rede reais.

## 3. Integração com GenAI
* **Onde o Gemini é utilizado:** O modelo é empregado como motor principal na geração do conteúdo estruturado Markdown dos ADRs a partir dos *brain-dumps* do usuário.
* **Como o backend conversa com o modelo:** O backend possui o módulo isolado `LLMService` que recebe a string validada, constrói o prompt (instrução de sistema + input) e efetua a requisição HTTP nativa à API do Google via SDK.
* **Por que a API não é chamada diretamente pelo frontend:** Para preservar a segurança da chave de acesso e evitar vazamentos de credenciais no lado do cliente. Adicionalmente, permite ao backend exercer papel de filtro, validando os inputs antes do consumo da cota de nuvem.
* **Como a API key é protegida:** A chave (`GEMINI_API_KEY`) é declarada e consumida apenas no backend via arquivo oculto `.env` manipulado pela biblioteca `dotenv`, sendo ativamente ignorada no `.gitignore`.

## 4. Desenvolvimento orientado por especificação
O projeto foi desenvolvido obedecendo integralmente aos requisitos definidos previamente no documento `docs/specs/adr_generation.md`.
* **Requisitos definidos antes da implementação:** Regras de negócio restritas sobre formato de entrada, modelo de IA e validações mandatórias.
* **Endpoint:** `POST /api/generate-adr`.
* **Validações:** Bloqueio direto a strings vazias ou nulas e restrição de limite máximo (payload < 5.000 caracteres) antes de qualquer iteração com a IA.
* **Comportamento esperado:** Entrega de um JSON com a string puramente em Markdown estruturada obrigatoriamente com Título, Contexto, Decisão e Consequências (positivas/negativas).
* **Tratamento de erros:** Regras explícitas sobre conversão de erros de IA (timeouts/dados vazios) em status HTTP 500 padronizado, escondendo o *stack trace* do usuário.
* **Requisitos de segurança:** Exigência de controle de XSS na renderização via `DOMPurify`.

A adesão restrita a essa especificação foi comprovada e documentada em `docs/evidence/spec_driven_implementation.md`.

## 5. Refatoração assistida por IA
A refatoração de design auxiliada pela GenAI está documentada no arquivo `docs/evidence/ai_refactoring.md`. 
O problema consistia no acoplamento global da classe `LLMService`. O agente de IA conduziu a mudança arquitetural para **Dependency Injection** (*Injeção de Dependência*) nativa do FastAPI utilizando a instrução `Depends(get_llm_service)`. A evidência fundamental do sucesso dessa operação está no fato de que a suíte completa de testes de integração permaneceu passando (`8 passed`) intocada, provando que o contrato da API permaneceu preservado.

## 6. Testes automatizados
A aplicação é protegida por uma robusta bateria de testes rodando via `pytest`, obtendo-se o resultado real e registrado de **`8 passed`** (100% de sucesso).
* **Testes unitários:** Validação atômica do módulo `LLMService` garantindo a construção do prompt e chamadas exatas.
* **Mocks:** Uso de `MagicMock` e `patch` interceptando as chamadas para `genai.Client` para não gerar cobrança real na franquia da API durante a execução contínua.
* **Dependency override:** Utilização primorosa do `app.dependency_overrides` no FastAPI via *fixtures* (`clear_overrides`), permitindo o teste limpo e isolado de rotas.
* **Validação de erros:** Cenários provando falhas (como limite de string ou ausência de `.env`), certificando a blindagem a erros não tratados.
* **Validação do endpoint:** O uso do `TestClient` provando o contrato HTTP e garantindo o status HTTP 200 nas rotas do caminho feliz.

## 7. Teste real de integração com Gemini
Foi realizado o teste real integrado onde a requisição validou a comunicação sistêmica ponta a ponta com a API em nuvem do Gemini e comprovou de fato que a geração autônoma de um arquivo Markdown de ADR a partir do tráfego executado funcionou na prática.

## 8. Documentação gerada/assistida por IA
Conforme relatado formalmente no arquivo `docs/evidence/documentation_generation.md`, o ferramental de GenAI teve protagonismo primário na produção da camada documental da aplicação, operando diretamente e colaborativamente nos arquivos:
* `README.md`
* `docs/adr/001-use-gemini-and-ai-as-a-service.md`

Tais produções sofreram rigorosa auditoria e revisão crítica para assegurar precisão técnica das métricas e das restrições estipuladas ao usuário final, confirmando a governança obrigatória descrita na política do projeto.

## 9. Custom Instructions
As instruções customizadas consolidadas sob diretiva estão definidas em `.agents/rules/custom_instructions.md`.
As 3 regras criadas e testáveis são:
1. **Testabilidade:** Determina isolamento na elaboração dos serviços (desvinculando rotas das regras de negócio), o que é integralmente verificável pela eficiência alcançada ao plugar os *mocks* e *fixtures* no `TestClient`.
2. **Tipagem Estrita:** Uso obrigatório de *Type Hints* (assinaturas com formato `def func() -> tipo:`), que é imediatamente testável por rodar linter simples e checagem de corretude em editores/ferramentas como o *Mypy*.
3. **Tratamento de Exceções Seguro:** Determina não espelhar erros profundos, passível de teste efetivo ao injetar anomalia simulada no serviço provando que apenas o *HTTP 500 genérico* emerge nas portas expostas da API.

## 10. Segurança e governança
De acordo com a averiguação explícita apontada no documento central `docs/evidence/security_analysis.md`, o projeto mantém os seguintes contornos sistêmicos:
* **Proteção da API key:** Resguardada integralmente no backend via ocultação ativada por *dotenv*.
* **Validação de entrada:** Restrição provada a textos vazios e limitação superior a 5.000 caracteres no payload do FastAPI.
* **DOMPurify:** Ativo no processamento do *Frontend* bloqueando execução invasiva (*Cross-Site Scripting* - XSS).
* **Tratamento de exceções:** Contenção executada pelo FastAPI evitando vazar *stack trace* original para requisições de origem web.
* **Ausência de funções perigosas:** Inexistência verificada manualmente da presença de `eval()`, `exec()` e similares.
* **Rate limiting:** Catalogado como **melhoria futura**.
* **Security headers:** Catalogado como **melhoria futura**.
* **Limitações analíticas Bandit:** Ausente no ambiente; as verificações estáticas dependem de revisão ativa suplementar em sua falta temporária.
* **Limitações analíticas pip-audit:** Ferramenta ausente no momento; impõe limitação para detectar *CVEs* transitivos dinamicamente sob as pinagens estáticas atuais de dependências.
* **Política de revisão humana:** Reiterada e alertada por banner visual estático dentro da própria ferramenta em tempo de execução e assinalada no `README.md`.

## 11. Arquitetura de GenAI
Adoção do *AI-as-a-Service* atestada em ADR (`001-use-gemini-and-ai-as-a-service.md`).
* **Custo & Latência:** Consumo baixíssimo e sob demanda contrapondo tempos de processamento síncronos velozes e fluidos por ser da categoria flash em nuvem.
* **Infraestrutura, Manutenção e Controle:** Delegação massiva do ônus e gestão de *hardware* e modelo complexo aos cuidados do Google; o controle do produto perde escopo em parâmetros avançados em favor da ultra simplificação na adoção via API.
* **Modelos locais:** Dispensados pelo altíssimo impeditivo de investimento de capital/esforço atrelado em hospedar *GPUs* ativas frente ao escopo simplificado da aplicação MVP (ADR Maker).
* **AI Gateway:** Preterido para este estagio sob justificativa pautada de representar *overengineering* (custos e latências indesejáveis em uma rota monolítica básica).

## 12. Matriz final de requisitos

| Requisito da disciplina | Evidência | Status |
|---|---|---|
| Problema real e específico | Documentado expressamente no `README.md` | Atendido |
| Integração com LLM | Conexão de sucesso e código estruturado provada no backend via SDK | Atendido |
| Feature com suporte de IA | Conversor interativo de texto informal > ADR oficial Markdown operante | Atendido |
| Spec/plan/prompts | Prompts listados no doc de evidência; Specs devidamente respeitadas | Atendido |
| Refatoração assistida por IA | Aplicação fluida de Injeção de Dependências detalhada via IA | Atendido |
| Testes automatizados | Módulo em `pytest` em vigor cobrindo a raiz lógica da aplicação | Atendido |
| Mock/fixture | Implementação e uso recorrente de simulacros da classe `genai` atestados | Atendido |
| Resultado real dos testes | Log com compilação sem falha (`8 passed`) documentado ativamente | Atendido |
| README | Estruturado via GenAI explicitando obrigatoriedade da auditoria humana | Atendido |
| ADR | Documento 001 oficializado detalhando AI-as-a-Service, revisado e aceito | Atendido |
| Custom Instructions | Documento nativo na pasta raiz contendo três diretrizes específicas | Atendido |
| Análise de segurança | Doc conclusivo avaliando os méritos da restrição e a falta de *linters* | Atendido |
| Revisão humana | Política e visualizações restritivas publicadas na especificação e UI | Atendido |
| Arquitetura GenAI | Argumentada detalhadamente listando os perfis e restrições (*trade-offs*) | Atendido |
| Evidências para apresentação | Ver Matriz de pendências (apresentação de slides, vídeo demonstrativo) | Pendente de produção extra |

## 13. Pendências para apresentação
A seguir os aparatos que não compõem a esteira direta de codificação ou das evidências textuais já criadas, mas demandam finalização expressa preparatória rumo à entrega da banca avaliativa:
* Planejar o **roteiro da demonstração oral** do pitch oficial.
* Produzir um conjunto de **screenshots ou vídeo demonstrativo** atestando a interatividade orgânica fluída dentro da ferramenta sem erros HTTP 500 no caminho feliz.
* Encadeamento de uma **sequência de demonstração** focada testando limites para explicitar que tentativas como inserções de mais de 5.000 caracteres não funcionam.
* Acondicionar toda hierarquia destas evidências e arquivos no escopo formal para o submetimento em **organização do ZIP final**.
