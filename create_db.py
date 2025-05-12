from Explorate import create_app,db # Import the create_app function and db object
from Explorate.models import db # Import all models

# Create the Flask app instance
app = create_app()

# Create all tables in the database
with app.app_context():
    db.create_all()
