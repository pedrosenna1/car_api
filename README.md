# Car API

Uma API RESTful para gerenciamento de um catálogo de carros, construída com FastAPI, SQLAlchemy e Pydantic, com autenticação de usuários via JWT.

---

## 📜 Sobre o Projeto

Este projeto fornece uma plataforma robusta para cadastrar, consultar, atualizar e deletar informações sobre carros, marcas e usuários. É uma API completa que serve como um excelente ponto de partida para aplicações mais complexas, demonstrando as melhores práticas de desenvolvimento com FastAPI, incluindo o uso de repositórios assíncronos, schemas de validação com Pydantic e gerenciamento de dependências com Poetry.

---

## ✨ Principais Funcionalidades

-   **Autenticação JWT**: Sistema de login seguro com `access_token` e `refresh_token`.
-   **Gerenciamento de Usuários (CRUD)**:
    -   Criação de novos usuários.
    -   Leitura de usuários (listagem e por ID).
    -   Atualização de informações de usuário.
    -   Exclusão de usuários.
-   **Gerenciamento de Marcas (CRUD)**:
    -   Criação de novas marcas de carros.
    -   Leitura de marcas.
    -   Atualização de marcas.
    -   Exclusão de marcas (somente se não houver carros associados).
-   **Gerenciamento de Carros (CRUD)**:
    -   Criação de novos carros associados a uma marca e um proprietário.
    -   Leitura de carros com filtros avançados (busca, combustível, transmissão, preço, etc.).
    -   Atualização de informações de carros.
    -   Exclusão de carros.

---

## 🛠️ Tecnologias Utilizadas

-   **Python 3.11+**
-   **FastAPI**: Framework web para a construção da API.
-   **SQLAlchemy (com Asyncio)**: ORM para comunicação assíncrona com o banco de dados.
-   **Pydantic**: Para validação de dados e schemas.
-   **Alembic**: Para migrações de banco de dados.
-   **Poetry**: Para gerenciamento de dependências e do ambiente virtual.
-   **Pytest**: Para a suíte de testes unitários e de integração.
-   **Ruff**: Linter e formatador de código para garantir a qualidade e consistência.
-   **Taskipy**: Para automação e execução de tarefas comuns (run, test, lint).

---

## 🚀 Começando

Siga estas instruções para obter uma cópia funcional do projeto em sua máquina local.

### Pré-requisitos

-   **Python 3.11** ou superior.
-   **Poetry** instalado. Você pode instalar seguindo as instruções [aqui](https://python-poetry.org/docs/#installation).

### Instalação

1.  **Clone o repositório:**
    ```sh
    git clone https://seu-repositorio-aqui/car-api.git
    cd car-api
    ```

2.  **Instale as dependências com Poetry:**
    ```sh
    poetry install
    ```

### Configuração

1.  **Crie o arquivo de ambiente:**
    Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`.
    ```sh
    cp .env.example .env
    ```

2.  **Configure as variáveis de ambiente:**
    Abra o arquivo `.env` e, se necessário, ajuste as variáveis. Para fins de segurança, é altamente recomendável alterar a `JWT_SECRET_KEY`.

    ```env
    DATABASE_URL="sqlite+aiosqlite:///./car.db"
    JWT_SECRET_KEY="your_super_secret_key_here"
    JWT_ALGORITHM="HS256"
    JWT_EXPIRATION_MINUTES=30
    JWT_REFRESH_EXPIRATION_HOURS=8
    ```
3.  **Execute as migrações do banco de dados (se aplicável):**
    *Este projeto utiliza Alembic. Se houver migrações a serem aplicadas, use:*
    ```sh
    poetry run alembic upgrade head
    ```

---

## 🏃‍♀️ Executando a Aplicação

Para iniciar o servidor de desenvolvimento, utilize o `taskipy`:

```sh
poetry run task run
```

A API estará disponível em `http://127.0.0.1:8000`. A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

---

## ✅ Executando os Testes

Para rodar a suíte de testes e verificar a cobertura, use o comando:

```sh
poetry run task test
```

Este comando irá executar todos os testes com `pytest` e gerar um relatório de cobertura de testes na pasta `htmlcov/`.

---

## 🗺️ Endpoints da API

Abaixo está um resumo dos principais endpoints disponíveis.

| Endpoint                               | Método | Descrição                                    | Autenticação |
| -------------------------------------- | ------ | ---------------------------------------------- | ------------ |
| `/api/v1/auth/`                        | `POST` | Autentica um usuário e retorna os tokens.      | Nenhuma      |
| `/api/v1/auth/refresh`                 | `POST` | Gera um novo `access_token` usando um `refresh_token`. | Nenhuma      |
| `/api/v1/users/`                       | `GET`  | Lista todos os usuários.                       | Obrigatória  |
| `/api/v1/users/add_user`               | `POST` | Cria um novo usuário.                          | Nenhuma      |
| `/api/v1/users/{user_id}`              | `GET`  | Obtém um usuário por ID.                       | Obrigatória  |
| `/api/v1/users/{user_id}`              | `PUT`  | Atualiza um usuário.                           | Obrigatória  |
| `/api/v1/users/{user_id}`              | `DELETE`| Deleta um usuário.                             | Obrigatória  |
| `/api/v1/brands/`                      | `GET`  | Lista todas as marcas.                         | Nenhuma      |
| `/api/v1/brands/`                      | `POST` | Cria uma nova marca.                           | Obrigatória  |
| `/api/v1/brands/{brand_id}`            | `GET`  | Obtém uma marca por ID.                        | Nenhuma      |
| `/api/v1/brands/{brand_id}`            | `PUT`  | Atualiza uma marca.                            | Obrigatória  |
| `/api/v1/brands/{brand_id}`            | `DELETE`| Deleta uma marca.                              | Obrigatória  |
| `/api/v1/cars/`                        | `GET`  | Lista carros com filtros.                      | Obrigatória  |
| `/api/v1/cars/`                        | `POST` | Cria um novo carro.                            | Obrigatória  |
| `/api/v1/cars/{car_id}`                | `GET`  | Obtém um carro por ID.                         | Obrigatória  |
| `/api/v1/cars/{car_id}`                | `PUT`  | Atualiza um carro.                             | Obrigatória  |
| `/api/v1/cars/{car_id}`                | `DELETE`| Deleta um carro.                               | Obrigatória  |

---

## 📁 Estrutura do Projeto

```
car-api/
├── car_api/
│   ├── core/         # Configurações globais, banco de dados, segurança
│   ├── models/       # Modelos SQLAlchemy (tabelas do banco)
│   ├── routers/      # Lógica dos endpoints da API
│   ├── schemas/      # Schemas Pydantic para validação e serialização
│   └── app.py        # Ponto de entrada da aplicação FastAPI
├── tests/            # Testes unitários e de integração
├── .env.example      # Arquivo de exemplo para variáveis de ambiente
├── alembic.ini       # Configuração do Alembic
├── pyproject.toml    # Definições do projeto e dependências (Poetry)
└── README.md         # Este arquivo
```
