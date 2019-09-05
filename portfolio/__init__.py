from flask import Flask
import os

# from datetime import datetime
import sys
import logging
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
# from portfolio.forms import RegistrationForm, LoginForm #**this line seems to give me problems. Will check it later
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail


app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get('PORTFOLIO_SECRET_KEY')
app.config['SECRET_KEY'] = 'secret key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

app.config['MAIL_SERVER'] = 'smtp.yandex.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('YANDEX_EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('YANDEX_EMAIL_PASS')


mail = Mail(app)

# SECRET_KEY=os.urandom(32)


app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zeta_g:postgres123@localhost/blog_posts'

# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zeta_g:postgres123@localhost/tetris_scores'

# app.config['SQLALCHEMY_DATABASE_URI']='postgres://wwahvywfqyxtzh:f467af8693cb8a633a9307bf43adb8e25ae04b04593dd010770c59e1ec926c08@ec2-107-21-216-112.compute-1.amazonaws.com:5432/ddvtoqgimmm9b9?sslmode=require'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# $env:FLASK_APP = "portfolio"
from portfolio import routes
