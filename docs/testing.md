# Testes

A **Car API** utiliza o framework **Pytest** para garantir a estabilidade e o funcionamento correto das funcionalidades.

## Estrutura de Testes
Os testes estão localizados no diretório `tests/` e são divididos por categorias:
- **Unitários**: Testam funções isoladas (ex: hashing de senha).
- **Integração**: Testam a comunicação com o banco de dados e fluxos completos de API.

## Como Executar os Testes

Para rodar todos os testes:
```bash
pytest
```

Para rodar testes com cobertura (se configurado):
```bash
pytest --cov=car_api
```

## Configuração de Testes
- Utilizamos uma base de dados SQLite em memória ou um arquivo separado para testes para evitar corromper os dados de desenvolvimento.
- As fixtures do Pytest (em `tests/conftest.py`) gerenciam a criação do cliente de teste e a limpeza do banco de dados após cada execução.

## Escrevendo Novos Testes
Sempre que adicionar uma nova funcionalidade, adicione um arquivo correspondente em `tests/`.
- Nome do arquivo deve começar com `test_`.
- Use nomes de funções descritivos.
- Siga o padrão **AAA** (Arrange, Act, Assert):
  1. **Arrange**: Prepare os dados e o ambiente.
  2. **Act**: Execute a ação/chamada da API.
  3. **Assert**: Verifique se o resultado é o esperado.
