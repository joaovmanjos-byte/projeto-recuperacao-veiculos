# API de Frota de Veiculos

Projeto individual de recuperacao: gerenciamento de veiculos com FastAPI, Pydantic, SQLAlchemy e SQLite.

## Estrutura e responsabilidades

- database.py: configura engine, SessionLocal, Base e get_db; fecha a sessao ao terminar cada requisicao.
- models.py: define a tabela veiculos usando SQLAlchemy.
- schemas.py: valida os dados de entrada e define a resposta. Usa from_attributes=True para ler objetos do ORM.
- routers/veiculos.py: implementa o CRUD, o filtro por marca e os erros HTTP.
- main.py: cria a aplicacao, registra o router e executa create_all().
- requirements.txt: dependencias do projeto.
- .gitignore: impede o versionamento do ambiente virtual, banco e caches.

## Instalacao e execucao no Windows

Requisitos: Python e Git instalados. Abra um terminal na pasta do projeto.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\fastapi.exe dev main.py
```

Swagger: http://127.0.0.1:8000/docs

Para executar com o ambiente ativado, abra o Prompt de Comando na pasta do projeto:

```bat
.venv\Scripts\activate.bat
fastapi dev main.py
```

Para parar o servidor: Ctrl+C.

## Campos e validacoes

| Campo | Tipo | Regra |
|---|---|---|
| id | inteiro | Chave primaria gerada pelo banco; nao enviar no cadastro |
| placa | texto | Unica; aceita formato ABC1234 ou ABC1D23 |
| marca | texto | Obrigatorio, de 1 a 50 caracteres |
| modelo | texto | Obrigatorio, de 1 a 80 caracteres |
| ano | inteiro | De 1886 ate o proximo ano; nao aceita texto ou decimal |
| ativo | booleano | Obrigatorio; true ou false |

A placa e convertida para maiusculas e tem o hifen removido.
Campos extras sao rejeitados. POST e PUT exigem todos os cinco campos de entrada.
O PUT substitui todos os campos editaveis e preserva o id.

## Contrato das rotas HTTP

URL base: http://127.0.0.1:8000

| Metodo | Rota | Entrada | Sucesso | Erros |
|---|---|---|---|---|
| POST | /veiculos/ | JSON com os cinco campos | 201: objeto criado com id | 409: placa duplicada; 422: dados invalidos |
| GET | /veiculos/ | Query parameter marca, opcional | 200: lista de veiculos | 422: parametros invalidos |
| GET | /veiculos/{id} | id inteiro na URL | 200: objeto encontrado | 404: inexistente; 422: id invalido |
| PUT | /veiculos/{id} | id e JSON completo | 200: objeto atualizado | 404: inexistente; 409: placa duplicada; 422: dados invalidos |
| DELETE | /veiculos/{id} | id inteiro na URL | 204: sem corpo | 404: inexistente; 422: id invalido |

GET sem filtro lista todos em ordem de id. Sem resultados, retorna [].
Exemplo de filtro: /veiculos/?marca=Fiat.
O filtro ignora diferencas entre maiusculas e minusculas para marcas como Fiat.
O filtro usa ILIKE: os caracteres % e _ funcionam como curingas SQL.

### Exemplo de corpo para POST e PUT

```json
{
  "placa": "ABC1D23",
  "marca": "Fiat",
  "modelo": "Uno",
  "ano": 2020,
  "ativo": true
}
```

### Exemplo de resposta do POST (201)

```json
{
  "placa": "ABC1D23",
  "marca": "Fiat",
  "modelo": "Uno",
  "ano": 2020,
  "ativo": true,
  "id": 1
}
```

O id acima e ilustrativo. Use o id retornado pelo seu banco.

### Exemplo de erro 404

```json
{"detail": "Veiculo nao encontrado"}
```

Placa duplicada retorna 409 com detail "Placa ja cadastrada".
Erros de validacao retornam 422 com uma lista detail indicando os campos invalidos.

## Persistencia

O arquivo frota.db e criado automaticamente na pasta de database.py.
As alteracoes sao gravadas por db.commit(). Fechar o servidor nao apaga os dados.
create_all() cria tabelas ausentes, sem apagar registros existentes.
O banco e local e nao e enviado ao GitHub. Uma nova copia do projeto inicia com banco vazio.

## Roteiro de demonstracao no Swagger

1. Apresentar nome completo e tema: Sistema de Frota de Veiculos.
2. Explicar os arquivos e a separacao em camadas.
3. Cadastrar dois veiculos de marcas diferentes via POST e conferir 201.
4. Listar com GET sem filtro e depois filtrar por marca.
5. Alterar um veiculo pelo PUT e consultar novamente para confirmar.
6. Excluir o outro pelo DELETE e conferir 204.
7. Repetir a exclusao do mesmo id e conferir 404.
8. Parar com Ctrl+C, fechar o VS Code e reabrir o projeto.
9. Iniciar novamente e executar GET para confirmar o registro restante.

## Versionamento

O historico registra a construcao por etapas: configuracao, banco, modelo,
validacoes, cadastro e consultas, atualizacao e exclusao, integracao e documentacao.

Para consultar:

```powershell
git log --oneline
```
