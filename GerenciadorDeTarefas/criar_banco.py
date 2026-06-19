from pathlib import Path
import sys

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from GerenciadorDeTarefas import app, database
from GerenciadorDeTarefas.models import Comentario, Tarefa, Usuario


def _colunas_da_tabela(nome_tabela):
    with database.engine.connect() as conexao:
        resultado = conexao.execute(text(f"PRAGMA table_info({nome_tabela})"))
        return {linha[1] for linha in resultado.fetchall()}


def _adicionar_coluna_se_nao_existir(nome_tabela, nome_coluna, definicao_sql):
    colunas = _colunas_da_tabela(nome_tabela)
    if nome_coluna in colunas:
        return False

    with database.engine.begin() as conexao:
        conexao.execute(text(f"ALTER TABLE {nome_tabela} ADD COLUMN {nome_coluna} {definicao_sql}"))
    return True


def _migrar_tabela_tarefa():
    coluna_criador = _adicionar_coluna_se_nao_existir('tarefa', 'criador_id', 'INTEGER')
    coluna_responsavel = _adicionar_coluna_se_nao_existir('tarefa', 'responsavel_id', 'INTEGER')

    colunas = _colunas_da_tabela('tarefa')
    if 'criador' not in colunas and 'responsavel' not in colunas:
        return coluna_criador or coluna_responsavel

    with database.engine.begin() as conexao:
        if 'criador' in colunas:
            conexao.execute(text("""
                UPDATE tarefa
                SET criador_id = (
                    SELECT usuario.id
                    FROM usuario
                    WHERE usuario.nome = tarefa.criador
                    LIMIT 1
                )
                WHERE criador_id IS NULL
            """))

        if 'responsavel' in colunas:
            conexao.execute(text("""
                UPDATE tarefa
                SET responsavel_id = (
                    SELECT usuario.id
                    FROM usuario
                    WHERE usuario.nome = tarefa.responsavel
                    LIMIT 1
                )
                WHERE responsavel_id IS NULL AND responsavel IS NOT NULL
            """))

    return coluna_criador or coluna_responsavel or 'criador' in colunas or 'responsavel' in colunas


def preparar_banco():
    with app.app_context():
        database.create_all()
        houve_migracao = _migrar_tabela_tarefa()
        if houve_migracao:
            print('Banco de dados atualizado com sucesso!')
        else:
            print('Banco de dados ja estava atualizado.')


if __name__ == '__main__':
    preparar_banco()
