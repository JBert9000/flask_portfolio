from flask import Flask
import sys
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from portfolio.config import Config
import os


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'


mail = Mail()
# $env:FLASK_APP = "portfolio"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI_PORTFOlIO"]

    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    with app.app_context():
        db.init_app(app)
        # db.create_all()

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from portfolio.users.routes import users
    from portfolio.posts.routes import posts
    from portfolio.main.routes import main
    from portfolio.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

    return app
