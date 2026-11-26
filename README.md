# Livros Vai na Web

Aplicação web para cadastrar livros para doação, consultar livros disponíveis e registrar solicitações. O projeto transforma o site original em uma aplicação Flask com páginas dinâmicas e dados persistidos.

## Tecnologias

- Python e Flask
- Jinja2
- Flask-SQLAlchemy e SQLite
- HTML e CSS
- Bootstrap 5 via CDN

## Executar localmente

Requer Python 3.10 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app app run --debug
```

Abra http://127.0.0.1:5000. O banco SQLite e suas tabelas são criados na primeira inicialização. Para criar as tabelas manualmente, use:

```bash
flask --app app init-db
```

## Configuração

As configurações podem ser definidas no arquivo `.env`:

- `SECRET_KEY`: chave usada pelo Flask para assinar sessões. Troque o valor de desenvolvimento por uma chave aleatória antes de publicar.
- `DATABASE_URL`: URL SQLAlchemy. Por padrão, o SQLite fica em `instance/livros.db`.
- `PORT`: porta do servidor (padrão `5000`).
- `FLASK_DEBUG`: use `true` apenas durante o desenvolvimento.

O arquivo `.env` e o banco local não devem ser enviados ao Git.

## Guia do usuário

- **Início:** veja os livros disponíveis mais recentes e acesse as principais áreas do site.
- **Consultar livros:** abra "Livros doados" para ver os livros disponíveis. Use a busca para pesquisar por título, autor ou categoria.
- **Ver detalhes:** selecione um livro para consultar sua descrição, categoria, disponibilidade e informações de quem o compartilhou.
- **Doar um livro:** acesse "Quero doar", preencha os dados do livro e seus dados de contato e envie o formulário.
- **Solicitar um livro:** abra os detalhes de um livro disponível, selecione "Solicitar este livro" e informe seus dados de contato.
- **Sobre:** consulte informações sobre o objetivo do projeto.

As doações e solicitações ficam salvas no banco SQLite e permanecem disponíveis após reiniciar a aplicação.

## Models e persistência

- `Doador`: nome, e-mail único e telefone de contato.
- `Livro`: título, autor, categoria, descrição, imagem, status e referência ao doador.
- `SolicitacaoDoacao`: livro solicitado, pessoa solicitante, mensagem e status.

Os relacionamentos permitem consultar o doador de um livro e as solicitações associadas.

## Rotas

- `/`: página inicial.
- `/livros`: lista e pesquisa livros disponíveis.
- `/livros/<id>`: detalhes de um livro.
- `/doar`: formulário de cadastro de doação.
- `/livros/<id>/solicitar`: formulário de solicitação de um livro.
- `/sobre`: informações sobre o projeto.

## Organização da aplicação

```text
app.py                 configuração e inicialização da aplicação Flask
extensions.py          extensão SQLAlchemy compartilhada
models.py              models Doador, Livro e SolicitacaoDoacao
routes.py              rotas e fluxos de doação e solicitação
templates/             templates Jinja2 das páginas
static/assets/         imagens do site
static/css/styles.css  estilos
tests/                 testes da aplicação
instance/              banco SQLite local, gerado e não versionado
requirements.txt       dependências Python
.env.example           exemplo de configuração por variáveis de ambiente
```

## Testes

Execute os testes com:

```bash
python -m unittest discover -s tests -v
```

## Integrante e tarefa

- Gabrielle Rosa (`n2Gabrielle`): implementação da estrutura Flask, configuração do SQLAlchemy, models `Doador`, `Livro` e `SolicitacaoDoacao`, rotas e persistência de doações e solicitações.