#!/usr/bin/env python3
"""Файл для запуска приложения."""

from api.blueprint import api_bp
from app import app, db
import views

app.register_blueprint(api_bp, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run()
