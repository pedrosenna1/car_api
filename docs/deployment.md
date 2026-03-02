# Deploy

A **Car API** pode ser implantada em diversos ambientes (Docker, VPS, PaaS como Render/Heroku).

## Preparação para Produção
1. **Ambiente**: Certifique-se de usar uma variável de ambiente `ENV=production`.
2. **Banco de Dados**: Para produção, recomenda-se substituir o SQLite por **PostgreSQL**.
   - Atualize a `DATABASE_URL` no `.env`.
3. **Segurança**: Use uma `SECRET_KEY` forte e gerada aleatoriamente.

## Docker (Recomendado)
Crie um `Dockerfile` na raiz do projeto:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --only main

COPY . .

CMD ["poetry", "run", "uvicorn", "car_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Servidor WSGI/ASGI
Utilizamos o **Uvicorn** como servidor ASGI. Em produção, você pode usar o **Gunicorn** com workers do Uvicorn para maior resiliência:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker car_api.app:app
```

## Checklist de Deploy
- [ ] Variáveis de ambiente configuradas.
- [ ] Migrações do banco de dados executadas (`alembic upgrade head`).
- [ ] Logs configurados para captura externa.
- [ ] Proxy reverso (como Nginx) configurado para gerenciar HTTPS e buffering.
