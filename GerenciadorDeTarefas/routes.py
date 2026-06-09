from flask import render_template
from GerenciadorDeTarefas import app
from flask_login import login_required

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerenciador/')
@login_required
def gerenciador():
    return render_template('gerenciador.html')

@app.route('/tarefa/<id_tarefa>')
@login_required
def tarefas(id_tarefa):
    return render_template('tarefa.html', id_tarefa=id_tarefa)