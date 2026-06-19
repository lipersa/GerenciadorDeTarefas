from GerenciadorDeTarefas import app
from GerenciadorDeTarefas.criar_banco import preparar_banco

if __name__ == '__main__':
    preparar_banco()
    app.run(debug=True)
