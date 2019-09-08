from flask import Flask

# from datetime import datetime
import sys
import logging
from flask_sqlalchemy import SQLAlchemy

# from portfolio.forms import RegistrationForm, LoginForm #**this line seems to give me problems. Will check it later
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from portfolio.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'


mail = Mail()

# SECRET_KEY=os.urandom(32)


# $env:FLASK_APP = "portfolio"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from portfolio.users.routes import users
    from portfolio.posts.routes import posts
    from portfolio.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

    return app
