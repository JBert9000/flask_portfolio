import pytest
import json
from flask_sqlalchemy import SQLAlchemy
from portfolio import create_app
from portfolio.users.routes import users
from flask import url_for


# @pytest.fixture
# def user():
#     user = users
#     return user


# def test_register_route(app):
#     response = app.get("/register/")
#     assert response.status_code == 200

def test_register_route(client):
    assert client.get(url_for('users.register')).status_code == 200
