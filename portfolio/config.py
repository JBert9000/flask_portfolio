import os
from subprocess import Popen, PIPE
# from boto3.s3.connection import S3Connection


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

    # SQLALCHEMY_DATABASE_URI = S3Connection(os.environ['DATABASE_URL'])

    # #################

    SECRET_KEY = MAIL_USERNAME = MAIL_PASSWORD = SQLALCHEMY_DATABASE_URI = None
    stdout, stderr = Popen(['heroku', 'config'], stdout=PIPE, stderr=PIPE, encoding='utf-8').communicate()
    for line in stdout.split('\n'):
        split = line.split(':')
        if len(split) == 2:
            if split[0] == 'SECRET_KEY':
                SECRET_KEY = split[1].strip()
            elif split[0] == 'YANDEX_EMAIL_USER':
                MAIL_USERNAME = split[1].strip()
            elif split[0] == 'YANDEX_EMAIL_PASS':
                MAIL_PASSWORD = split[1].strip()
            elif split[0] == 'SQLALCHEMY_DATABASE_URI':
                SQLALCHEMY_DATABASE_URI_PORTFOlIO = split[1].strip()
