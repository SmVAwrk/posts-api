web: cd test_exercise/ && gunicorn flask_app:app
init: python test_exercise/manage.py db init && python test_exercise/manage.py db migrate && python test_exercise/manage.py db upgrade
test: cd test_exercise/ && python -m unittest