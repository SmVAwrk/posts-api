from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

# Приложение
app = Flask(__name__)
app.config.from_object(Configuration)

# API
api = Api(app)


# База данных
db = SQLAlchemy(app)


# Миграции БД
from models import *

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


