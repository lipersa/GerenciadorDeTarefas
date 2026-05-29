from flask import render_template
from GerenciadorDeTarefas import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerenciador/')
def gerenciador():
    return render_template('gerenciador.html')

@app.route('/tarefa/<id_tarefa>')
def tarefas(id_tarefa):
    return render_template('tarefa.html', id_tarefa=id_tarefa)