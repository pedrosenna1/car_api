# Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

## 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/car-api.git
cd car-api
```

## 2. Instalar Dependências
Utilize o Poetry para instalar todas as dependências do projeto, incluindo as de desenvolvimento:
```bash
poetry install
```

## 3. Configurar o Ambiente Virtual
O Poetry criará automaticamente um ambiente virtual. Você pode ativá-lo com:
```bash
poetry shell
```

## 4. Configurar Variáveis de Ambiente
Copie o arquivo de exemplo (se disponível) ou crie um arquivo `.env` na raiz do projeto:
```bash
cp .env.example .env
```
*Certifique-se de configurar a `SECRET_KEY` para o JWT.*

## 5. Executar Migrações
Crie as tabelas no banco de dados SQLite utilizando o Alembic:
```bash
alembic upgrade head
```

## 6. Iniciar a Aplicação
Execute o servidor de desenvolvimento:
```bash
task run
```
A API estará disponível em `http://127.0.0.1:8000`.

## 7. Acessar a Documentação Interativa
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
