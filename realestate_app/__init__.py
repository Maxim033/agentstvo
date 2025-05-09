from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Конфигурация
    from realestate_app.config import Config
    app.config.from_object(Config)

    # Инициализация БД
    db.init_app(app)

    # Регистрация маршрутов
    from realestate_app.routes import bp
    app.register_blueprint(bp)

    # Создание таблиц
    with app.app_context():
        db.create_all()

    return app