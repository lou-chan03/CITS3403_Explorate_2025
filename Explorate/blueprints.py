from .auth import auth
from .routes import main

def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(auth)