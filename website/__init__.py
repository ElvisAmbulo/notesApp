import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # Read secrets / DB URL from environment (safe for Render)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"sqlite:///{DB_NAME}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)

    # Register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models so they are known to SQLAlchemy
    # (use the actual filename you have: modals.py or models.py)
    from .modals import User, Note

    # Setup Flask-Login
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # user_id is a string from the session — convert to int if your PK is int
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # Create DB tables if missing (inside app context)
    create_database(app)

    return app


def create_database(app):
    db_path = path.join('website', DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
        print('Created Database!')
