from GerenciadorDeTarefas import database, app
from GerenciadorDeTarefas.models import Usuario, Tarefa, Comentario

with app.app_context():
    database.create_all()
    print("Banco de dados criado com sucesso!")