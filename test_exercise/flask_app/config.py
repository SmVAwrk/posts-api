import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    """Конфигурация приложения."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ff_user:1q2w3e@localhost/liis_exercise'


class ProductionConfiguration(Configuration):
    DEBUG = False
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
