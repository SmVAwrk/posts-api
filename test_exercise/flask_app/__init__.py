from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_rest_paginate import Pagination
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from .config import Configuration

# Приложение
app = Flask(__name__)
app.config.from_object(Configuration)

# База данных
db = SQLAlchemy(app)

# Миграции БД
from .models import *

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Пагинация
pagination = Pagination(app, db)

# Регистрация BP
from .api.blueprint import api_bp

app.register_blueprint(api_bp, url_prefix='/api/v1')
