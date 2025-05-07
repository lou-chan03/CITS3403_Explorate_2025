from app import create_app
from app.models import db  # Import your models here

# Create the app instance
app = create_app()

# Create all tables in the database (based on the models)
with app.app_context():
    db.create_all()
    print("Database and tables created successfully!")
