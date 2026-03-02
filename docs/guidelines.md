# Guidelines e Padrões

Para manter a consistência e a qualidade do código na **Car API**, seguimos as diretrizes abaixo.

## Padrões de Código
- **PEP 8**: Seguimos rigorosamente as recomendações de estilo do Python.
- **Tipagem Estática**: Utilizamos `Type Hints` em todas as funções, modelos e schemas para facilitar a manutenção e detecção de bugs.
- **Async/Await**: Toda a interação com o banco de dados e endpoints da API deve ser assíncrona.

## Estrutura de Resposta API
As respostas da API devem ser consistentes:
- **Sucesso (200, 201)**: Retorna o objeto criado ou solicitado.
- **Erros (400, 401, 403, 404)**: Devem retornar um JSON com o formato:
  ```json
  {
    "error": 404,
    "detail": "Mensagem descritiva do erro"
  }
  ```

## Nomeclatura
- **Variáveis e Funções**: `snake_case`.
- **Classes**: `PascalCase`.
- **Constantes**: `UPPER_CASE`.
- **Endpoints**: `kebab-case` (ex: `/api/v1/user-profiles`). No momento, utilizamos o padrão singular/plural consistente.

## Validação de Dados
- Utilizamos **Pydantic Schemas** para validar toda entrada e saída de dados.
- Nenhuma lógica de validação complexa deve estar diretamente nas rotas; prefira validadores do Pydantic ou serviços dedicados.

## Controle de Versão (Git)
- Commits devem ser claros e descritivos.
- Sugestão de prefixos para commits:
  - `feat:` para novas funcionalidades.
  - `fix:` para correção de bugs.
  - `docs:` para alterações na documentação.
  - `refactor:` para melhorias no código sem alterar comportamento.
  - `test:` para adição ou modificação de testes.
