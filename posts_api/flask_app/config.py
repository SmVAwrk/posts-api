import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    """Конфигурация приложения."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ff_user:1q2w3e@localhost/posts_api'


class ProductionConfiguration(Configuration):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
