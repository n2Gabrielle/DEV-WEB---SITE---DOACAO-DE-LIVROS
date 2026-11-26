# Livros Vai na Web

Aplicação web para cadastrar livros para doação, consultar livros disponíveis e registrar solicitações.

## Executar localmente

Requer Python 3.10 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app app run --debug
```

Abra <http://127.0.0.1:5000>. O banco SQLite e as tabelas são criados na primeira inicialização. Para criar as tabelas manualmente, use `flask --app app init-db`.

## Configuração

As configurações podem ser definidas em `.env`:

- `SECRET_KEY`: chave usada pelo Flask para assinar sessões. Troque o valor de desenvolvimento por uma chave aleatória antes de publicar.
- `DATABASE_URL`: URL SQLAlchemy. Por padrão, o SQLite fica em `instance/livros.db`; outros bancos podem ser configurados usando uma URL SQLAlchemy compatível.
- `PORT`: porta do servidor local (padrão `5000`).
- `FLASK_DEBUG`: use `true` apenas durante desenvolvimento.

O arquivo `.env` e o banco local não devem ser enviados ao Git.

## Models e persistência

- `Doador`: nome, e-mail único e telefone de contato.
- `Livro`: título, autor, categoria, descrição, imagem, status e referência ao doador.
- `SolicitacaoDoacao`: livro solicitado, pessoa solicitante, mensagem e status.

Os relacionamentos permitem consultar o doador de um livro e as solicitações associadas. Os registros são armazenados no SQLite e permanecem disponíveis após reiniciar a aplicação.

## Rotas

- `/`: página inicial com os livros disponíveis mais recentes.
- `/livros`: lista e pesquisa livros disponíveis.
- `/livros/<id>`: detalhes de um livro.
- `/doar`: cadastro persistente de uma doação.
- `/livros/<id>/solicitar`: cadastro persistente de uma solicitação.
- `/sobre`: informações sobre o projeto.

## Estrutura

```text
app.py                 fábrica e configuração da aplicação Flask
extensions.py          extensão SQLAlchemy compartilhada
models.py              models Doador, Livro e SolicitacaoDoacao
routes.py              rotas e fluxos de doação/solicitação
templates/             templates Jinja2
static/assets/         imagens do site
static/css/styles.css  estilos
tests/                 testes da aplicação
instance/              banco SQLite local (gerado; não versionado)
```

## Integrante e tarefa

- **Gabrielle Rosa (`n2Gabrielle`)**: implementação da estrutura Flask, configuração do SQLAlchemy, models `Doador`, `Livro` e `SolicitacaoDoacao`, rotas e persistência de doações e solicitações.
