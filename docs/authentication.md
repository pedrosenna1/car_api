# Autenticação e Segurança

A segurança é um pilar fundamental da **Car API**. Utilizamos padrões de mercado para garantir a integridade dos dados e a privacidade dos usuários.

## Mecanismo de Autenticação
A API utiliza **OAuth2 com Password Flow** e tokens **JWT (JSON Web Tokens)**.

1. **Obtenção do Token**: O usuário envia suas credenciais para `/api/v1/auth/token`. A API retorna um `access_token` e um `refresh_token`.
2. **Uso do Token**: Para acessar rotas protegidas (como as de Carros e Marcas), o usuário deve incluir o token de acesso no Header HTTP:
   ```http
   Authorization: Bearer <seu_token_jwt>
   ```
3. **Refresh Token**: O `refresh_token` permite que o usuário obtenha um novo token de acesso sem precisar reenviar as credenciais, aumentando a segurança e melhorando a experiência do usuário. Sua validade é configurada em horas.

## Segurança de Senhas
As senhas **nunca** são armazenadas em texto plano. Utilizamos o algoritmo **Argon2** (via `pwdlib`), que é atualmente um dos mais robustos contra ataques de força bruta e dicionário.

## Controle de Acesso
Além da autenticação, implementamos verificações de autorização:
- **Propriedade do Recurso**: Um usuário só pode visualizar, editar ou excluir carros que ele mesmo cadastrou. Esta verificação é feita através da dependência `verify_car_owner`.
- **Integridade de Usuário**: Usuários só podem alterar seus próprios dados de perfil.

## Proteção contra Erros
A API possui um handler global de exceções que oculta detalhes técnicos de erros internos, retornando mensagens amigáveis e códigos HTTP semânticos (401 para não autenticado, 403 para falta de permissão, etc).

## Boas Práticas Recomendadas
- Use sempre **HTTPS** em ambientes de produção.
- Altere a `JWT_SECRET_KEY` regularmente e use chaves complexas.
- Defina um tempo de expiração curto para o `ACCESS_TOKEN`.
