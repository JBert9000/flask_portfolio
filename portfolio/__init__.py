from flask import Flask
import os

from datetime import datetime
import sys
import logging
from flask_sqlalchemy import SQLAlchemy
from portfolio.send_email2 import send_email
from sqlalchemy.sql import func
from portfolio.forms import RegistrationForm, LoginForm
# from portfolio.routes import app


app=Flask(__name__)

SECRET_KEY=os.urandom(32)

app.config['SECRET_KEY']='613cbb85c192d44ce3c5e5b66ef35110'

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zeta_g:postgres123@localhost/blog_posts'


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zeta_g:postgres123@localhost/tetris_scores'

# app.config['SQLALCHEMY_DATABASE_URI']='postgres://wwahvywfqyxtzh:f467af8693cb8a633a9307bf43adb8e25ae04b04593dd010770c59e1ec926c08@ec2-107-21-216-112.compute-1.amazonaws.com:5432/ddvtoqgimmm9b9?sslmode=require'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

from portfolio import routes

# $env:FLASK_APP = "portfolio"
