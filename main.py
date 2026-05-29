from flask import Flask , render_template
from GerenciadorDeTarefas import app

if __name__ == '__main__':
    app.run(debug=True)