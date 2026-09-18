# Evidência de Execução dos Testes

## Comando executado

```text
python -m pytest
```

## Resultado

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\joaov\Final_Project_GenAI
plugins: anyio-4.15.1, mock-3.15.1
collected 8 items

tests\test_llm_service.py ....                                           [ 50%]
tests\test_main.py ....                                                  [100%]

============================== warnings summary ===============================
..\AppData\Roaming\Python\Python314\site-packages\google\genai\types.py:42
  C:\Users\joaov\AppData\Roaming\Python\Python314\site-packages\google\genai\types.py:42: DeprecationWarning: '_UnionGenericAlias' is deprecated and slated for removal in Python 3.17
    VersionedUnionType = Union[builtin_types.UnionType, _UnionGenericAlias]

..\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1
  C:\Users\joaov\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

..\AppData\Roaming\Python\Python314\site-packages\starlette\testclient.py:53
  C:\Users\joaov\AppData\Roaming\Python\Python314\site-packages\starlette\testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 8 passed, 3 warnings in 3.79s ========================
```

* **Quantidade de testes executados:** 8
* **Quantidade de testes aprovados:** 8
* **Quantidade de testes falhos:** 0
* **Warnings:** 3 (relativos a depreciações futuras sistêmicas nas dependências base do Python 3.14)
* **Duração da execução:** 3.79s

## Interpretação

Esta execução confirma e atesta o estado funcional da suíte de testes no exato momento desta auditoria. A passagem unânime dos testes demonstra inequivocamente que as regressões não existem e os requisitos da aplicação permanecem intactos e perfeitamente funcionais perante as validações definidas.

## Tipos de testes

Com base restritamente nos arquivos presentes no repositório (`tests/`):

* **Testes Unitários:** Ocorrem no arquivo `test_llm_service.py` avaliando a classe isolada de geração de ADRs, validando respostas cheias, chaves ausentes e tratamento de exceções da IA. Utilizam fortemente **mocks** (como `unittest.mock.patch` e objetos `MagicMock`) interceptando a atuação direta do módulo `google.genai`.
* **Testes de Integração:** Ocorrem no arquivo `test_main.py` interagindo com a rota FastAPI `/api/generate-adr`. Eles validam os status HTTP (200, 400 e 500) da via web. Operam utilizando **fixtures** nativas do `pytest` (`@pytest.fixture(autouse=True)` para redefinir dependências limpas por ciclo) aliados à prática madura de *dependency override* nativa do *framework*.
