# Modelagem do Sistema

Esta seção apresenta a modelagem técnica da **Car API** utilizando diagramas Mermaid.

## Modelos de Dados (ERD)
O diagrama abaixo representa a estrutura das tabelas no banco de dados e seus relacionamentos.

```mermaid
erDiagram
    USER ||--o{ CAR : "possui"
    BRAND ||--o{ CAR : "categoriza"
    
    USER {
        int id PK
        string username
        string password
        string email
        datetime created_at
        datetime updated_at
    }
    
    BRAND {
        int id PK
        string name
        boolean is_active
        string description
        datetime created_at
        datetime updated_at
    }
    
    CAR {
        int id PK
        int brand_id FK
        int owner_id FK
        string model
        int factory_year
        int model_year
        string color
        string plate
        string fuel_type
        string transmission
        decimal price
        string description
        boolean is_available
        datetime created_at
        datetime updated_at
    }
```

## Arquitetura do Sistema
A API segue uma arquitetura multicamadas baseada em FastAPI.

```mermaid
graph TD
    Client[Cliente/Frontend] -- HTTP Request --> API[FastAPI App]
    API -- Injeção de Dependência --> Router[Routers /api/v1/...]
    Router -- Validação --> Schemas[Pydantic Schemas]
    Router -- Autenticação --> Security[JWT/Auth Middleware]
    Router -- Operações DB --> Session[SQLAlchemy AsyncSession]
    Session -- SQL --> DB[(SQLite/PostgreSQL)]
```

## Fluxo de Autenticação
Processo de obtenção e validação do token JWT.

```mermaid
sequenceDiagram
    participant User as Cliente
    participant Auth as Auth Router
    participant Security as Security Core
    participant DB as Banco de Dados

    User->>Auth: POST /api/v1/auth/ (email as username, password)
    Auth->>DB: Busca usuário por email
    DB-->>Auth: Retorna Usuário + Hash Senha
    Auth->>Security: Verifica Hash Senha
    Security-->>Auth: Senha Válida
    Auth->>Security: create_access_token(user_id)
    Security-->>Auth: JWT Access Token + Refresh Token
    Auth-->>User: 200 OK (access_token, refresh_token)
```

## Fluxo CRUD de Carros
Exemplo de criação de um novo veículo com validações.

```mermaid
sequenceDiagram
    participant User as Cliente Autenticado
    participant CarRouter as Car Router
    participant Security as valid_token Dependency
    participant DB as Banco de Dados

    User->>CarRouter: POST /api/v1/cars/
    CarRouter->>Security: Valida JWT
    Security-->>CarRouter: Retorna User Object
    CarRouter->>DB: Verifica se Brand existe e está ativa
    DB-->>CarRouter: OK
    CarRouter->>DB: Verifica se Plate já existe
    DB-->>CarRouter: Não existe
    CarRouter->>DB: INSERT INTO cars ...
    DB-->>CarRouter: Created
    CarRouter-->>User: 201 Created (Car Data)
```

## Fluxo de Segurança
Como protegemos os recursos de acesso não autorizado.

```mermaid
graph LR
    Req[Requisição HTTP] --> Token[Verifica Token JWT]
    Token -- Inválido --> Error401[401 Unauthorized]
    Token -- Válido --> OwnerCheck[verify_car_owner / verify_user]
    OwnerCheck -- Não é dono --> Error403[403 Forbidden / 404 Not Found]
    OwnerCheck -- É dono --> Success[Executa Ação]
```
