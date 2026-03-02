# Desenvolvimento

Este guia é destinado a desenvolvedores que desejam contribuir ou estender as funcionalidades da **Car API**.

## Fluxo de Trabalho Recomendado

1. **Criação de Features**:
   - Crie uma branch para a nova funcionalidade: `git checkout -b feat/nova-funcao`.
   - Adicione os modelos necessários em `car_api/models/`.
   - Gere a migração correspondente: `alembic revision --autogenerate -m "add feature model"`.

2. **Desenvolvimento de Schemas e Routers**:
   - Defina os schemas de Entrada e Saída em `car_api/schemas/`.
   - Implemente as rotas em `car_api/routers/`.

3. **Garantia de Qualidade**:
   - Execute o formatador: `task format`.
   - Verifique o linting: `task lint`.
   - Rode os testes (veja a seção de [Testes](testing.md)).

## Scripts Úteis (Taskipy)
Facilitamos o uso de comandos comuns através do `taskipy`. Confira no `pyproject.toml`:
- `task run`: Inicia o servidor FastAPI em modo de desenvolvimento (hot reload).
- `task lint`: Roda o Ruff para verificar o código.
- `task format`: Roda o Ruff para formatar o código.
- `task docs`: Inicia o servidor do MkDocs para visualizar esta documentação localmente.

## Dicas de Desenvolvimento
- **Hot Reload**: O comando `task run` utiliza o `fastapi dev`, que reinicia o servidor automaticamente a cada alteração no código.
- **Banco de Dados Local**: O arquivo `car.db` é criado automaticamente. Você pode usar ferramentas como *SQLite Browser* ou a extensão do VS Code para visualizar os dados.
- **Logs**: Fique atento ao terminal onde o servidor está rodando para capturar erros e logs de depuração.
