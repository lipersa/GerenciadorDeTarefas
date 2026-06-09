from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GerenciadorDeTarefas.db'
app.config['SECRET_KEY'] = 'eb5f5eed4206b7a69da5a52d3329b35d13736796c89b68607ed9afb821d40cf6'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'


from GerenciadorDeTarefas import routes, models


