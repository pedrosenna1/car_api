# Visão Geral do Projeto

A **Car API** é uma solução de backend projetada para facilitar o controle de ativos automotivos. Ela permite que usuários se cadastrem, autentiquem e gerenciem seus próprios veículos, além de permitir a administração de marcas.

## Tecnologias Utilizadas

### Core
- **Python 3.13+**: Linguagem base do projeto.
- **FastAPI**: Framework web moderno e de alta performance.
- **SQLAlchemy 2.0**: ORM para interação com o banco de dados (Assíncrono).
- **Aiosqlite**: Driver assíncrono para SQLite (ambiente de desenvolvimento/testes).
- **Pydantic v2**: Validação de dados e definições de schemas.
- **Alembic**: Gerenciamento de migrações de banco de dados.

### Segurança e Qualidade
- **PyJWT**: Manipulação de tokens JSON Web Token.
- **Argon2**: Algoritmo de hash para senhas (via `pwdlib`).
- **Ruff**: Linter e formatador de código extremamente rápido.
- **Pytest**: Framework para testes automatizados.

### Documentação
- **MkDocs**: Gerador de sites de documentação estática.
- **Material for MkDocs**: Tema moderno para a documentação.
- **Mermaid.js**: Geração de diagramas a partir de texto.

## Arquitetura de Alto Nível
O projeto segue uma estrutura modular, separando responsabilidades entre modelos de banco de dados, schemas de validação, rotas da API e lógica de segurança.

- **Rotas**: Definem os endpoints e gerenciam as requisições HTTP.
- **Modelos**: Representam as entidades no banco de dados.
- **Schemas**: Validam a entrada e formatam a saída de dados.
- **Core**: Contém configurações globais, segurança e conexão com o banco.
