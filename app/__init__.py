from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
<<<<<<< HEAD
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

=======

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
>>>>>>> main
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
<<<<<<< HEAD
    login_manager.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
=======
    login.init_app(app)

    with app.app_context():
        from app.models import User  # Importowanie modeli w kontekście aplikacji
        from app.routes import bp as main_bp
        app.register_blueprint(main_bp)

        @login.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
>>>>>>> main
