from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .routes import main 
from flask_login import LoginManager
from Explorate.config import Config
from .blueprints import register_blueprints
from Explorate.models import db

from Explorate.csrf import csrf, CSRFError

login = LoginManager()
login.login_view = 'main'

def create_app(config):
    # create app from the config
    app = Flask(__name__)
    app.config.from_object(config) 

    csrf.init_app(app)

    # Initialize db with app
    db.init_app(app)

    migrate = Migrate(app, db)

     # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'main.home'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    register_blueprints(app)

    return app

