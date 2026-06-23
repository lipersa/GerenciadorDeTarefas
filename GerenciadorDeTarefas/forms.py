from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError

from GerenciadorDeTarefas.models import Usuario


class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao = SubmitField("Entrar")


class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Usuario", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=8)])
    confirmeSenha = PasswordField("Confirme Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email ja cadastrado, faca login novamente.")


class FormCriarTarefa(FlaskForm):
    titulo = StringField("Titulo", validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField("Descricao", validators=[Optional(), Length(max=2000)])
    prazo = DateTimeLocalField("Prazo", format="%Y-%m-%dT%H:%M", validators=[Optional()])
    prioridade = SelectField(
        "Prioridade",
        choices=[("Baixa", "Baixa"), ("Media", "Media"), ("Alta", "Alta")],
        validators=[DataRequired()],
        default="Baixa",
    )
    botao_confirmacao = SubmitField("Criar tarefa")
