class Configuration:
    """Конфигурация приложения."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ff_user:1q2w3e@localhost/liis_exercise'


class ProductionConfiguration(Configuration):
    DEBUG = False
