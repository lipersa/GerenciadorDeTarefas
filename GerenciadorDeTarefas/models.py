from GerenciadorDeTarefas import database
from datetime import datetime

class Usuario(database.Model):
    id                  = database.Column(database.Integer, primary_key=True)
    nome                = database.Column(database.String(100), nullable=False)
    email               = database.Column(database.String(100), unique=True, nullable=False)
    senha               = database.Column(database.String(100), nullable=False)
    cargo               = database.Column(database.String(50), nullable=False)
    permissionamento    = database.Column(database.String(50), nullable=False)

class Tarefa(database.Model):
    id                  = database.Column(database.Integer, primary_key=True)
    responsavel_id      = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=True)
    criador_id          = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    titulo              = database.Column(database.String(100), nullable=False)
    data_criacao        = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    data_finalizacao    = database.Column(database.DateTime, nullable=True)
    status              = database.Column(database.String(20), nullable=False, default='Pendente')
    descricao           = database.Column(database.Text, nullable=True)
    prazo               = database.Column(database.DateTime, nullable=True)
    prioridade          = database.Column(database.String(20), nullable=False, default='Baixa')
    id_tarefa           = database.Column(database.Integer, autoincrement=True, unique=True)
    comentarios         = database.relationship('Comentario', backref='tarefa', lazy=True)
    pontuacao           = database.Column(database.Integer, nullable=True)

class Comentario(database.Model):
    id                  = database.Column(database.Integer, primary_key=True)
    id_tarefa           = database.Column(database.Integer, database.ForeignKey('tarefa.id'), nullable=False)
    autor               = database.Column(database.String(100), database.ForeignKey('usuario.nome'), nullable=False)
    data_comentario     = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    conteudo            = database.Column(database.Text, nullable=False)
