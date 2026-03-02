# Estrutura do Projeto

Abaixo está a organização de diretórios e arquivos da **Car API**.

```text
car_api/
├── car_api/                # Código fonte principal
│   ├── core/               # Configurações globais, segurança e DB
│   │   ├── database.py     # Conexão e sessão do banco
│   │   ├── security.py     # Lógica de JWT e hashing
│   │   └── settings.py     # Configurações via pydantic-settings
│   ├── models/             # Modelos do SQLAlchemy (Banco de Dados)
│   │   ├── base.py         # Classe base declarativa
│   │   ├── cars.py         # Modelos de Carro e Marca
│   │   └── users.py        # Modelo de Usuário
│   ├── routers/            # Definições de rotas (Endpoints)
│   │   ├── auth.py         # Autenticação e Token
│   │   ├── brands.py       # Gerenciamento de marcas
│   │   ├── cars.py         # Gerenciamento de carros
│   │   └── users.py        # Gerenciamento de usuários
│   ├── schemas/            # Schemas do Pydantic (Validação)
│   │   ├── auth.py
│   │   ├── brands.py
│   │   ├── cars.py
│   │   └── users.py
│   └── app.py              # Ponto de entrada da aplicação FastAPI
├── docs/                   # Documentação do projeto (Markdown)
├── migrations/             # Migrações do banco de dados (Alembic)
├── tests/                  # Testes automatizados
├── .env                    # Variáveis de ambiente (não versionado)
├── alembic.ini             # Configuração do Alembic
├── pyproject.toml          # Dependências e configurações de ferramentas
└── README.md               # Instruções rápidas
```

## Descrição dos Diretórios Principais

- **`car_api/core/`**: Centraliza o "coração" da aplicação. Se você precisar mudar como o banco conecta ou como o token é gerado, é aqui.
- **`car_api/models/`**: Define a estrutura das tabelas. Usamos o SQLAlchemy 2.0 com mapeamento tipado (`Mapped`).
- **`car_api/routers/`**: Onde a lógica de interface da API reside. Cada módulo agrupa rotas relacionadas a um domínio.
- **`car_api/schemas/`**: Define como os dados entram e saem da API. Essencial para validação e documentação automática.
- **`migrations/`**: Histórico de evolução do banco de dados. Permite que outros desenvolvedores tenham a mesma estrutura de tabelas.
