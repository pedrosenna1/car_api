# Configuração do Projeto

A configuração da **Car API** é gerenciada através de variáveis de ambiente, utilizando a biblioteca `pydantic-settings`.

## Arquivo .env
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL="sqlite+aiosqlite:///./car.db"
JWT_SECRET_KEY="sua_chave_secreta_aqui"
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_MINUTES=30
JWT_REFRESH_EXPIRATION_HOURS=5
```

### Detalhes das Variáveis
- **DATABASE_URL**: URL de conexão com o banco de dados. O projeto usa SQLite de forma assíncrona por padrão.
- **JWT_SECRET_KEY**: Uma string longa e aleatória usada para assinar os tokens JWT. **Nunca compartilhe esta chave**.
- **JWT_ALGORITHM**: Algoritmo de criptografia para o JWT (Padrão: HS256).
- **JWT_EXPIRATION_MINUTES**: Tempo de validade do token de acesso em minutos.
- **JWT_REFRESH_EXPIRATION_HOURS**: Tempo de validade do token de atualização (refresh token) em horas.

## Configuração do Banco de Dados (Alembic)
O arquivo `alembic.ini` e o diretório `migrations/` contêm a configuração para o controle de versão do banco de dados.
- Para criar uma nova migração após alterar um modelo:
  ```bash
  alembic revision --autogenerate -m "descrição da mudança"
  ```
- Para aplicar as mudanças:
  ```bash
  alembic upgrade head
  ```

## Linting e Formatação (Ruff)
O projeto utiliza o **Ruff** para garantir a qualidade do código. As configurações estão presentes no `pyproject.toml`.
- Comandos disponíveis via `taskipy`:
  ```bash
  task lint    # Verifica erros de linting
  task format  # Formata o código automaticamente
  ```
