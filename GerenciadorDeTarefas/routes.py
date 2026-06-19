from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_

from GerenciadorDeTarefas import app, bcrypt, database
from GerenciadorDeTarefas.forms import FormCriarConta, FormLogin
from GerenciadorDeTarefas.models import Tarefa, Usuario


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('gerenciador'))

    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for('perfil', id_usuario=usuario.id))

        flash('E-mail ou senha invalidos.', 'erro')

    return render_template('homepage.html', form=formlogin)


@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    if current_user.is_authenticated:
        return redirect(url_for('gerenciador'))

    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha_hash = bcrypt.generate_password_hash(formcriarconta.senha.data).decode('utf-8')
        usuario = Usuario(
            nome=formcriarconta.username.data,
            email=formcriarconta.email.data,
            senha=senha_hash,
        )

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('criarConta.html', form=formcriarconta)


@app.route('/gerenciador/')
@login_required
def gerenciador():
    tarefas = Tarefa.query.filter(
        or_(Tarefa.criador_id == current_user.id, Tarefa.responsavel_id == current_user.id)
    ).order_by(Tarefa.data_criacao.desc()).all()
    return render_template('gerenciador.html', tarefas=tarefas)


@app.route('/perfil/<int:id_usuario>')
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    tarefas_criadas = Tarefa.query.filter_by(criador_id=usuario.id).order_by(Tarefa.data_criacao.desc()).all()
    tarefas_recebidas = Tarefa.query.filter_by(responsavel_id=usuario.id).order_by(Tarefa.data_criacao.desc()).all()
    return render_template(
        'perfil.html',
        usuario=usuario,
        tarefas_criadas=tarefas_criadas,
        tarefas_recebidas=tarefas_recebidas,
        visualizando_proprio_perfil=usuario.id == current_user.id,
    )


@app.route('/tarefa/<int:id_tarefa>')
@login_required
def tarefas(id_tarefa):
    tarefa = Tarefa.query.filter(
        or_(Tarefa.id == id_tarefa, Tarefa.id_tarefa == id_tarefa)
    ).first_or_404()
    return render_template('tarefa.html', tarefa=tarefa)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))
