from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth.routes import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main.routes import main as main_bp
    app.register_blueprint(main_bp)

    return app
