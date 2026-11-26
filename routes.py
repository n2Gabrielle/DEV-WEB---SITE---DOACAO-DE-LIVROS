import re
from urllib.parse import urlparse

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from extensions import db
from models import Doador, Livro, SolicitacaoDoacao


main = Blueprint("main", __name__)
FALLBACK_COVER = "assets/livroDoado.png"


def _form_doador():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    telefone = request.form.get("telefone", "").strip()
    if not nome or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return None

    doador = Doador.query.filter_by(email=email).first()
    if doador is None:
        doador = Doador(nome=nome, email=email, telefone=telefone or None)
        db.session.add(doador)
    else:
        doador.nome = nome
        if telefone:
            doador.telefone = telefone
    return doador


def _valid_image_url(value):
    if not value:
        return True
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


@main.get("/")
def index():
    livros = (
        Livro.query.filter_by(status="disponivel")
        .order_by(Livro.criado_em.desc())
        .limit(3)
        .all()
    )
    return render_template("index.html", livros=livros)


@main.get("/livros")
def listar_livros():
    busca = request.args.get("q", "").strip()
    consulta = Livro.query.filter_by(status="disponivel")
    if busca:
        termo = f"%{busca}%"
        consulta = consulta.filter(
            or_(
                Livro.titulo.ilike(termo),
                Livro.autor.ilike(termo),
                Livro.categoria.ilike(termo),
            )
        )
    livros = consulta.order_by(Livro.criado_em.desc()).all()
    return render_template("livros.html", livros=livros, busca=busca)


@main.get("/livros/<int:livro_id>")
def detalhe_livro(livro_id):
    livro = db.get_or_404(Livro, livro_id)
    return render_template("detalhe_livro.html", livro=livro, fallback_cover=FALLBACK_COVER)


@main.route("/doar", methods=["GET", "POST"])
def doar():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        categoria = request.form.get("categoria", "").strip()
        imagem_url = request.form.get("imagem_url", "").strip()
        descricao = request.form.get("descricao", "").strip()
        doador = _form_doador()

        if not titulo or not autor or not categoria or doador is None:
            flash("Informe os dados do livro e um nome e e-mail válidos.", "danger")
            return render_template("doar.html"), 400
        if not _valid_image_url(imagem_url):
            flash("O link da imagem precisa começar com http:// ou https://.", "danger")
            return render_template("doar.html"), 400

        livro = Livro(
            titulo=titulo,
            autor=autor,
            categoria=categoria,
            descricao=descricao or None,
            imagem_url=imagem_url or None,
            doador=doador,
        )
        db.session.add(livro)
        db.session.commit()
        flash("Doação cadastrada. Obrigado por compartilhar!", "success")
        return redirect(url_for("main.detalhe_livro", livro_id=livro.id))

    return render_template("doar.html")


@main.route("/livros/<int:livro_id>/solicitar", methods=["GET", "POST"])
def solicitar_livro(livro_id):
    livro = db.get_or_404(Livro, livro_id)
    if livro.status != "disponivel":
        flash("Este livro não está mais disponível para solicitação.", "warning")
        return redirect(url_for("main.detalhe_livro", livro_id=livro.id))

    if request.method == "POST":
        solicitante = _form_doador()
        mensagem = request.form.get("mensagem", "").strip()
        if solicitante is None:
            flash("Informe um nome e um e-mail válidos para solicitar o livro.", "danger")
            return render_template("solicitar.html", livro=livro), 400

        db.session.flush()
        existente = SolicitacaoDoacao.query.filter_by(
            livro_id=livro.id,
            solicitante_id=solicitante.id,
            status="pendente",
        ).first()
        if existente:
            flash("Você já tem uma solicitação pendente para este livro.", "warning")
            return redirect(url_for("main.detalhe_livro", livro_id=livro.id))

        db.session.add(
            SolicitacaoDoacao(
                livro=livro,
                solicitante=solicitante,
                mensagem=mensagem or None,
            )
        )
        livro.status = "solicitado"
        db.session.commit()
        flash("Solicitação registrada. O doador poderá entrar em contato.", "success")
        return redirect(url_for("main.detalhe_livro", livro_id=livro.id))

    return render_template("solicitar.html", livro=livro)


@main.get("/sobre")
def sobre():
    return render_template("sobre.html")
