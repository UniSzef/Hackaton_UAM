from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    with app.app_context():
        from app.models import User  # Importowanie modeli w kontekście aplikacji
        from app.routes import bp as main_bp
        app.register_blueprint(main_bp)

        @login.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
