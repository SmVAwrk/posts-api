web: cd posts_api/ && gunicorn flask_app:app
init: python posts_api/manage.py db init && python posts_api/manage.py db migrate && python posts_api/manage.py db upgrade
test: cd posts_api/ && python -m unittest