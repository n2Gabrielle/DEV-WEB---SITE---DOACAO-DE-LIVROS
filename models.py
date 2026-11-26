from datetime import datetime, timezone

from sqlalchemy import CheckConstraint

from extensions import db


class Doador(db.Model):
    __tablename__ = "doadores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    telefone = db.Column(db.String(30))
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    livros = db.relationship("Livro", back_populates="doador")
    solicitacoes = db.relationship("SolicitacaoDoacao", back_populates="solicitante")


class Livro(db.Model):
    __tablename__ = "livros"
    __table_args__ = (
        CheckConstraint(
            "status IN ('disponivel', 'solicitado', 'doado')",
            name="ck_livros_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(180), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text)
    imagem_url = db.Column(db.String(500))
    status = db.Column(db.String(20), nullable=False, default="disponivel", index=True)
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    doador_id = db.Column(db.Integer, db.ForeignKey("doadores.id"), nullable=False)

    doador = db.relationship("Doador", back_populates="livros")
    solicitacoes = db.relationship("SolicitacaoDoacao", back_populates="livro")


class SolicitacaoDoacao(db.Model):
    __tablename__ = "solicitacoes_doacao"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pendente', 'aceita', 'recusada')",
            name="ck_solicitacoes_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default="pendente", index=True)
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    livro_id = db.Column(db.Integer, db.ForeignKey("livros.id"), nullable=False)
    solicitante_id = db.Column(db.Integer, db.ForeignKey("doadores.id"), nullable=False)

    livro = db.relationship("Livro", back_populates="solicitacoes")
    solicitante = db.relationship("Doador", back_populates="solicitacoes")
