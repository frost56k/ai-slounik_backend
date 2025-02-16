from flask import Flask
from flask_cors import CORS  # Добавляем импорт
from app.routes import main

def create_app():
    app = Flask(__name__)
    
    # Настройка CORS для всего приложения
    CORS(
        app,
        resources={r"/api/*": {
            "origins": "https://ai-slounik.andchar.of.by",
            "methods": ["POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }}
    )
    
    # Регистрация Blueprint
    app.register_blueprint(main)
    
    return app
