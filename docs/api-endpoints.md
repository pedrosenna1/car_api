# API Endpoints

A **Car API** está organizada em diferentes grupos de recursos. Abaixo estão os principais endpoints disponíveis.

## Autenticação (`/api/v1/auth`)
Endpoints para obtenção e renovação de tokens de acesso.

| Método | Endpoint | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| POST | `/api/v1/auth/` | Gera um token JWT (OAuth2 Password Flow) | Público |
| POST | `/api/v1/auth/refresh` | Renova o token de acesso usando refresh token | Público |

## Usuários (`/api/v1/users`)
Gerenciamento de contas de usuário.

| Método | Endpoint | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| POST | `/api/v1/users/add_user` | Cria um novo usuário | Público |
| GET | `/api/v1/users/` | Lista usuários (paginado) | Autenticado |
| GET | `/api/v1/users/{id}` | Detalhes de um usuário específico | Autenticado |
| PUT | `/api/v1/users/{id}` | Atualiza dados do usuário (apenas o próprio) | Autenticado |
| DELETE | `/api/v1/users/{id}` | Remove um usuário (apenas o próprio) | Autenticado |

## Carros (`/api/v1/cars`)
Gerenciamento de veículos. Requer autenticação.

| Método | Endpoint | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| POST | `/api/v1/cars/` | Cadastra um novo carro | Autenticado |
| GET | `/api/v1/cars/` | Lista carros do usuário autenticado | Autenticado |
| GET | `/api/v1/cars/{id}` | Detalhes de um carro (apenas se for dono) | Autenticado |
| PUT | `/api/v1/cars/{id}` | Atualiza dados de um carro (apenas se for dono) | Autenticado |
| DELETE | `/api/v1/cars/{id}` | Remove um carro (apenas se for dono) | Autenticado |

## Marcas (`/api/v1/brands`)
Gerenciamento de marcas de veículos. Requer autenticação.

| Método | Endpoint | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| POST | `/api/v1/brands/` | Cadastra uma nova marca | Autenticado |
| GET | `/api/v1/brands/` | Lista todas as marcas | Autenticado |
| GET | `/api/v1/brands/{id}` | Detalhes de uma marca | Autenticado |
| PUT | `/api/v1/brands/{id}` | Atualiza uma marca | Autenticado |
| DELETE | `/api/v1/brands/{id}` | Remove uma marca (se não houver carros vinculados) | Autenticado |

## Saúde do Sistema
| Método | Endpoint | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| GET | `/health_check` | Verifica se a API está online | Público |

---
*Para detalhes sobre os campos de entrada e saída, consulte o Swagger UI em `/docs`.*
