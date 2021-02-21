from flask import jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import redirect

from . import app
from .models import User

auth = HTTPBasicAuth()


@app.route('/')
def index():
    """Представление индексной страницы"""
    return redirect(url_for('api.api_root'))


@app.errorhandler(404)
def error_handler():
    pass
    # TODO


@auth.verify_password
def verify_password(username, password):
    """Функция для проверки пользователя и пароля"""
    user = User.query.filter(User.username == username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@auth.error_handler
def auth_error(status):
    """Кастомная обработка ошибок валидации"""
    return jsonify({'message': 'access denied'}), status
