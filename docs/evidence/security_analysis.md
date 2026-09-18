# Análise de Segurança do Código Assistido por IA

## 1. Objetivo
Esta análise foi realizada com o objetivo de identificar potenciais riscos e vulnerabilidades introduzidos ou potencializados pelo uso de GenAI no desenvolvimento da aplicação (ADR Maker).

## 2. SAST (Static Application Security Testing)
Durante o processo de verificação de vulnerabilidades no código-fonte Python:
* **Ferramenta considerada:** Bandit
* **Comando utilizado:** `python -m bandit -r backend/ tests/`
* **Resultado:** A ferramenta Bandit não estava instalada no ambiente de execução.
* **Métricas automatizadas:** Nenhuma métrica automatizada foi produzida devido à ausência da ferramenta.
* **Análise complementar:** Uma análise manual rigorosa e complementar foi realizada para compensar parcialmente a ausência da varredura automatizada.

## 3. Análise manual do código
A inspeção manual validou de forma satisfatória os seguintes pontos na arquitetura atual:
* **Ausência de API keys hardcoded:** O código-fonte não possui segredos inseridos diretamente.
* **Isolamento de credenciais:** O projeto utiliza corretamente a estratégia `os.getenv("GEMINI_API_KEY")` integrada com `dotenv` para carregamento seguro.
* **Ausência de funções perigosas:** Não há instâncias de uso de funções críticas de execução de strings ou processos no nível do sistema operativo, como `eval()`, `exec()`, `os.system()` e `subprocess`.
* **Tratamento genérico de erros HTTP 500:** As falhas internas e exceções são tratadas de forma genérica no backend (via FastAPI `HTTPException`), emitindo um erro HTTP 500 sem vazar a *stack trace* para o cliente.
* **Validação de entrada:** O backend (FastAPI) recusa textos vazios e limita o payload recebido a 5.000 caracteres, reduzindo o tamanho máximo do conteúdo processado.
* **Proteção contra XSS:** O frontend utiliza DOMPurify para sanitizar o HTML resultante da conversão do Markdown antes de inseri-lo no DOM, reduzindo o risco de XSS.
* **Fluxo do conteúdo:** O dado bruto inserido não interage de forma direta ou irrefletida com o DOM antes de transitar via API para o modelo generativo e regressar sanitizado para a renderização no navegador.

## 4. Riscos identificados
Apesar dos controles de segurança atualmente implementados, dois riscos arquiteturais significativos foram detectados:

### 4.1 Ausência de Rate Limiting
A falta de um limitador de requisições permite que usuários mal-intencionados realizem chamadas automatizadas excessivas em frações de segundo. Isso não apenas sobrecarrega a API do Gemini consumindo rapidamente cotas/custos, mas afeta diretamente a disponibilidade do serviço.
* **Tratamento recomendado:** Implementar rate limiting no backend, por exemplo configurando um middleware limitador de frequência ou biblioteca apropriada (ex: `slowapi`).
* **Status:** `Melhoria futura / não implementada nesta versão`.

### 4.2 Ausência de Security Headers
O backend da aplicação não configura explicitamente e nem transmite proativamente cabeçalhos estritos de segurança ao cliente web, tais como *Content-Security-Policy (CSP)* ou *X-Frame-Options*.
* **Tratamento recomendado:** Adicionar middleware ou configurações no aplicativo FastAPI para devolver e reforçar headers de segurança na comunicação.
* **Status:** `Melhoria futura / não implementada nesta versão`.

## 5. Auditoria de dependências
A verificação dos módulos de terceiros instalados demonstrou o seguinte:
* **Versões:** A aplicação adota fixação de versões (*version pinning*) listadas no `requirements.txt`.
* **Correspondência:** Foi atestado e confirmado que as versões efetivamente instaladas e operacionais na máquina correspondem fielmente às declaradas no `requirements.txt`.
* **Ferramenta automática:** O pacote `pip-audit` não estava instalado no ambiente.
* **Consequência:** A auditoria automatizada de vulnerabilidades transitivas **não foi executada**. 

**Importante:** A inspeção manual passiva não identificou versões notoriamente comprometidas *à primeira vista*, mas sob hipótese alguma isso serve como afirmação de que as dependências estão livres de vulnerabilidades recém-descobertas (CVEs). Isto não substitui a devida conferência e não valida a eficácia de uma ferramenta de auditoria baseada em um banco de dados de vulnerabilidades estruturado.

## 6. Limitações
A condução desta auditoria está atrelada às seguintes limitações de ambiente:
* Bandit não disponível.
* pip-audit não disponível.
* Ausência integral de varredura automatizada contra vulnerabilidades transitivas.
* A análise manual detectou e cobriu aspectos lógicos, mas de modo algum substitui processos SAST/SCA automatizados.

## 7. Política de tratamento
Visando orientar a adoção responsável da GenAI, aplicam-se os seguintes trâmites:
* Nenhuma chave de API ou segredo jamais deve ser "commitado" ao repositório ou divulgado.
* Todo código gerado ou modificado por IA deve passar por rigorosa revisão humana.
* Bibliotecas e dependências devem ser avaliadas antes da sua inclusão no projeto.
* Testes automatizados unitários e de integração precisam ser sempre executados e repassados após a inserção ou alteração do fluxo funcional.
* Os riscos identificados devem ser documentados e devidamente tratados antes da subida para o ambiente de produção.

## 8. Conclusão
A aplicação possui controles importantes de segurança, como proteção da API key, validação de entrada, tratamento de exceções e sanitização do conteúdo renderizado no frontend. Foram identificadas melhorias arquiteturais preventivas relacionadas a rate limiting e security headers. A análise automatizada completa da *stack* infelizmente ficou limitada pela ausência das ferramentas analíticas especializadas (Bandit e pip-audit) no ambiente local, portanto essas limitações da averiguação devem permanecer explicitamente registradas.

| Verificação | Resultado | Status |
|---|---|---|
| API key hardcoded | Não encontrado | OK |
| eval/exec/os.system/subprocess | Não encontrado | OK |
| XSS | DOMPurify utilizado | OK |
| Validação de entrada | Implementada | OK |
| Stack trace exposto | Não identificado | OK |
| Rate limiting | Ausente | Melhoria futura |
| Security Headers | Ausentes | Melhoria futura |
| Bandit | Não disponível | Limitação |
| pip-audit | Não disponível | Limitação |
