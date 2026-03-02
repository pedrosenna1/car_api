# Release Notes

Acompanhe aqui a evolução da **Car API**.

## v0.1.0 (Versão Inicial)
*Lançamento inicial do projeto.*

### Funcionalidades
- **Sistema de Usuários**: Cadastro, Login e Atualização de perfil.
- **Módulo de Marcas**: CRUD completo de marcas de veículos com controle de status (ativo/inativo).
- **Módulo de Carros**: Cadastro de veículos vinculado a marcas e proprietários.
- **Autenticação**: Implementação de JWT (Access e Refresh tokens).
- **Segurança**: Hashing de senhas com Argon2 e proteção de rotas por proprietário do recurso.
- **Infraestrutura**: Configuração assíncrona com SQLAlchemy e Alembic.

### Melhorias Técnicas
- Configuração do **Ruff** para linting e formatação.
- Documentação técnica utilizando **MkDocs** e diagramas **Mermaid**.
- Testes automatizados básicos com **Pytest**.

---
*Próximos Passos:*
- Implementação de filtros avançados na listagem de carros.
- Adição de suporte a upload de imagens de veículos.
- Integração contínua (CI) com GitHub Actions.
