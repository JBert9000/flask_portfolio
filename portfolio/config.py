import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    MAIL_SERVER = 'smtp.yandex.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('YANDEX_EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('YANDEX_EMAIL_PASS')

    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_LOCAL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_PORTFOlIO')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
