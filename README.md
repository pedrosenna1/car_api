# Car API

API REST completa para gerenciamento de veículos, marcas e usuários, construída com **FastAPI**, **SQLAlchemy Async** e autenticação **JWT**. Desenvolvida em **Python 3.13** com gerenciamento de dependências via **Poetry**.

---

## Sobre o Projeto

Sistema de catálogo de carros com:

- CRUD completo de **Usuários**, **Marcas** e **Carros**
- Autenticação via **JWT** com `access_token` e `refresh_token`
- Banco de dados assíncrono com **SQLAlchemy AsyncIO**
- Migrações com **Alembic**
- Hash de senhas com **Argon2** (via pwdlib)
- Validação de dados com **Pydantic v2** e **pydantic-settings**
- Filtros avançados na listagem de carros (combustível, transmissão, faixa de preço, busca por texto)
- Controle de propriedade — cada usuário só acessa/edita seus próprios carros
- Proteção de integridade — marcas com carros associados não podem ser deletadas
- Testes automatizados com **pytest-asyncio** e cobertura com **pytest-cov**
- Documentação do projeto com **MkDocs Material**
- Suporte a **SQLite** (dev) e **PostgreSQL** (produção via psycopg)

---

## Stack / Tecnologias

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3.13 |
| Framework Web | FastAPI (com Uvicorn via `fastapi[standard]`) |
| ORM | SQLAlchemy 2.x (AsyncIO) |
| Driver SQLite | aiosqlite |
| Driver PostgreSQL | psycopg (binary) |
| Validação | Pydantic v2, pydantic-settings |
| Autenticação | PyJWT, OAuth2 Password Bearer |
| Hash de Senhas | pwdlib com backend Argon2 |
| Migrações | Alembic |
| Testes | pytest, pytest-asyncio, pytest-cov |
| Linter/Formatter | Ruff |
| Task Runner | Taskipy |
| Documentação | MkDocs + Material Theme + pymdown-extensions |
| Gerenciador de Dependências | Poetry |

---

## Pré-requisitos

- **Linux** (Ubuntu/Debian ou derivados)
- **Python 3.13** ou superior
- **pipx** (para instalar o Poetry de forma isolada)
- **Poetry** (gerenciador de dependências Python)

---

## Instalação passo a passo (Linux)

### 1. Instalar o pipx

O `pipx` instala ferramentas Python CLI em ambientes isolados. Se ainda não tem, instale:

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```

Feche e reabra o terminal (ou rode `source ~/.bashrc`) para que o PATH seja atualizado.

### 2. Instalar o Poetry via pipx

```bash
pipx install poetry
```

Verifique a instalação:

```bash
poetry --version
```

### 3. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/car-api.git
cd car-api
```

### 4. Instalar as dependências do projeto

```bash
poetry install
```

Isso cria automaticamente um ambiente virtual e instala todas as dependências (produção + desenvolvimento).

### 5. Criar o arquivo `.env`

```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:

```env
DATABASE_URL="sqlite+aiosqlite:///./car.db"
JWT_SECRET_KEY="troque_por_uma_chave_secreta_forte"
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_MINUTES=30
JWT_REFRESH_EXPIRATION_HOURS=8
```

> **Para PostgreSQL em produção**, use:
> ```env
> DATABASE_URL="postgresql+psycopg://usuario:senha@localhost:5432/car_api"
> ```

### 6. Rodar as migrações do banco de dados

```bash
poetry run alembic upgrade head
```

### 7. Iniciar o servidor

```bash
poetry run task run
```

A API sobe em **http://127.0.0.1:8000**.

- Swagger UI (docs interativos): **http://127.0.0.1:8000/docs**
- ReDoc: **http://127.0.0.1:8000/redoc**

---

## Comandos úteis (Taskipy)

Todos os comandos são executados via `poetry run task <comando>`:

| Comando | O que faz |
|---|---|
| `poetry run task run` | Inicia o servidor de desenvolvimento (FastAPI dev mode) |
| `poetry run task test` | Roda o linter (Ruff) + testes (pytest) com cobertura + gera relatório HTML |
| `poetry run task lint` | Executa o Ruff para verificar o código |
| `poetry run task format` | Corrige problemas do Ruff e formata o código |
| `poetry run task docs` | Sobe a documentação MkDocs em http://127.0.0.1:8001 |

---

## Testes

Os testes usam **SQLite em memória**, sem necessidade de banco externo:

```bash
poetry run task test
```

Isso executa em sequência:
1. `ruff check` (lint)
2. `pytest -s -x --cov=car_api -vv` (testes com cobertura)
3. `coverage html` (gera relatório em `htmlcov/`)

Abra `htmlcov/index.html` no navegador para ver o relatório de cobertura.

---

## Endpoints da API

Todos os endpoints estão sob o prefixo `/api/v1`.

### Autenticação (`/api/v1/auth`)

| Método | Endpoint | Descrição | Auth |
|---|---|---|---|
| `POST` | `/api/v1/auth/` | Login — retorna `access_token` e `refresh_token` (envia e-mail no campo `username`) | Não |
| `POST` | `/api/v1/auth/refresh` | Gera novo `access_token` a partir do `refresh_token` | Não |

### Usuários (`/api/v1/users`)

| Método | Endpoint | Descrição | Auth |
|---|---|---|---|
| `POST` | `/api/v1/users/add_user` | Criar novo usuário | Não |
| `GET` | `/api/v1/users/` | Listar usuários (com busca por username/email) | Sim |
| `GET` | `/api/v1/users/{user_id}` | Buscar usuário por ID | Sim |
| `PUT` | `/api/v1/users/{user_id}` | Atualizar usuário (somente o próprio) | Sim |
| `DELETE` | `/api/v1/users/{user_id}` | Deletar usuário (somente o próprio) | Sim |

### Marcas (`/api/v1/brands`)

| Método | Endpoint | Descrição | Auth |
|---|---|---|---|
| `POST` | `/api/v1/brands/` | Criar nova marca | Sim |
| `GET` | `/api/v1/brands/` | Listar marcas (filtro por nome, status ativo) | Sim |
| `GET` | `/api/v1/brands/{brand_id}` | Buscar marca por ID | Sim |
| `PUT` | `/api/v1/brands/{brand_id}` | Atualizar marca | Sim |
| `DELETE` | `/api/v1/brands/{brand_id}` | Deletar marca (somente se não tiver carros vinculados) | Sim |

### Carros (`/api/v1/cars`)

| Método | Endpoint | Descrição | Auth |
|---|---|---|---|
| `POST` | `/api/v1/cars/` | Criar novo carro | Sim |
| `GET` | `/api/v1/cars/` | Listar carros do usuário (filtros: busca, combustível, transmissão, preço, marca, disponibilidade) | Sim |
| `GET` | `/api/v1/cars/{car_id}` | Buscar carro por ID (somente do próprio usuário) | Sim |
| `PUT` | `/api/v1/cars/{car_id}` | Atualizar carro (somente o proprietário) | Sim |
| `DELETE` | `/api/v1/cars/{car_id}` | Deletar carro (somente o proprietário) | Sim |

### Health Check

| Método | Endpoint | Descrição | Auth |
|---|---|---|---|
| `GET` | `/health_check` | Verifica se a API está online | Não |

---

## Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | URL de conexão com o banco de dados (async) | `sqlite+aiosqlite:///./car.db` |
| `JWT_SECRET_KEY` | Chave secreta para assinar os tokens JWT | `uma_chave_secreta_bem_forte` |
| `JWT_ALGORITHM` | Algoritmo de assinatura do JWT | `HS256` |
| `JWT_EXPIRATION_MINUTES` | Tempo de expiração do access token (minutos) | `30` |
| `JWT_REFRESH_EXPIRATION_HOURS` | Tempo de expiração do refresh token (horas) | `8` |

---

## Estrutura do Projeto

```
car_api/
├── car_api/
│   ├── __init__.py
│   ├── app.py                  # Ponto de entrada — instância FastAPI, routers, exception handler
│   ├── core/
│   │   ├── database.py         # Engine async do SQLAlchemy e session generator
│   │   ├── security.py         # Hash de senhas (Argon2), criação/verificação JWT, guards de autenticação
│   │   └── settings.py         # Carregamento de variáveis de ambiente via pydantic-settings
│   ├── models/
│   │   ├── base.py             # DeclarativeBase do SQLAlchemy
│   │   ├── users.py            # Model User (id, username, email, password, timestamps)
│   │   └── cars.py             # Models Brand e Car (com enums FuelType e TransmissionType)
│   ├── routers/
│   │   ├── auth.py             # Endpoints de login e refresh token
│   │   ├── users.py            # CRUD de usuários
│   │   ├── brands.py           # CRUD de marcas
│   │   └── cars.py             # CRUD de carros (com filtros avançados)
│   └── schemas/
│       ├── auth.py             # Schemas Token e RefreshToken
│       ├── users.py            # Schemas de criação, atualização e resposta de usuários
│       ├── brands.py           # Schemas de criação, atualização e resposta de marcas
│       └── cars.py             # Schemas de criação, atualização e resposta de carros
├── migrations/
│   ├── env.py                  # Configuração async do Alembic
│   └── versions/               # Arquivos de migração
├── tests/
│   ├── conftest.py             # Fixtures (session em memória, client, user, token, brand)
│   ├── test_auth.py            # Testes de autenticação
│   ├── test_users.py           # Testes de CRUD de usuários
│   ├── test_brands.py          # Testes de CRUD de marcas
│   ├── test_cars.py            # Testes de CRUD de carros
│   └── test_db.py              # Testes de conexão com banco
├── docs/                       # Documentação MkDocs
├── htmlcov/                    # Relatório de cobertura de testes (gerado)
├── alembic.ini                 # Configuração do Alembic
├── mkdocs.yml                  # Configuração do MkDocs Material
├── pyproject.toml              # Configuração do projeto, dependências e ferramentas (Poetry)
├── requirements_docs.txt       # Dependências para documentação (deploy separado)
└── README.md
```

---

## Documentação MkDocs

O projeto inclui documentação completa usando MkDocs com o tema Material:

```bash
poetry run task docs
```

Acesse em **http://127.0.0.1:8001**.

---

## Autor

**Pedro Senna**
