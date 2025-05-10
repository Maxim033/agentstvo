import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.utils import secure_filename

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Конфигурация
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join('realestate_app', 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Регистрация Blueprint
    from realestate_app.routes import bp
    app.register_blueprint(bp)

    # Создание папки для загрузок
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Кастомные фильтры
    @app.template_filter('format_price')
    def format_price(value):
        try:
            return "{:,.0f}".format(value).replace(",", " ")
        except:
            return str(value)

    @app.template_filter('property_type_name')
    def property_type_name(value):
        types = {
            'apartment': 'Квартира',
            'house': 'Дом',
            'commercial': 'Коммерческая'
        }
        return types.get(value, value)

    return app