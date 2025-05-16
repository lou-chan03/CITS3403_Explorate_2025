from Explorate import create_app
from Explorate.models import db 
from Explorate.config import DeploymentConfig

app = create_app(DeploymentConfig)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
