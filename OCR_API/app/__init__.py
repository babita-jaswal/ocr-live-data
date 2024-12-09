from flask import Flask
from app.routes import main_bp
from .routes import main_bp        # Import and register blueprints

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.secret_key = 'supersecretkey'  # Secret key for session handling

    return app
