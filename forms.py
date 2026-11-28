from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email

categorias_livros = [('autoajuda', 'Autoajuda'), ('aventura', 'Aventura'), 
                     ('biografia', 'Biografia / Autobiografia'), ('cronica', 'Ensaio / Crônica'),
                     ('distopia', 'Distopia'), ('fantasia', 'Fantasia'), ('ficcao', 'Ficção'),
                     ('policial', 'Policial'), ('religiao', 'Religião / Espiritualidade'),
                     ('romance', 'Romance'), ('suspense', 'Suspense'),
                     ('tecnico', 'Livro Técnico / Acadêmico'), ('terror', 'Terror')]

class DoarLivros(FlaskForm):
    titulo = StringField('titulo', validators=[DataRequired(), Length(max=50)])
    autor = StringField('autor', validators=[DataRequired(), Length(min=3, max=50)])
    categoria = SelectField('categoria', validators=[DataRequired()], choices=categorias_livros)
    img_url = StringField('imagem', validators=[])
    descricao = TextAreaField('descricao')

    nome = StringField('nome', validators=[Length(max=70)])
    email = EmailField('email', validators=[])
    telefone = StringField('telefone', validators=[Length(max=14)])
    enviar = SubmitField('Cadastrar Doação')