# Regras de Custom Instructions para o Projeto

1. **Testabilidade**: Todo novo serviço criado no backend deve possuir funções ou classes bem isoladas para facilitar a escrita de testes unitários com mocks. Não misture regra de negócio com handlers de rota.
2. **Tipagem Estrita**: É obrigatório o uso de *Type Hints* em todas as funções Python (ex: `def func(a: int) -> str:`). O código deve passar em verificações básicas de tipagem estática.
3. **Tratamento de Exceções Seguro**: O backend nunca deve vazar detalhes de erro interno (`500`) ou *stack traces* para o cliente. Toda exceção inesperada deve ser capturada e convertida em uma mensagem genérica de erro HTTP padronizada, registrando o erro real no logger.
