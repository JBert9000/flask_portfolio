import pytest
import json
from flask_sqlalchemy import SQLAlchemy
from portfolio import create_app
from portfolio.users.routes import users
from flask import url_for, Response


def test_register_route(client):
    assert client.get(url_for('users.register')).status_code == 200
