#!/usr/bin/env python3
"""Файл для управления приложением."""

from flask_app import manager, app, db
import flask_app.views


if __name__ == '__main__':
    manager.run()
