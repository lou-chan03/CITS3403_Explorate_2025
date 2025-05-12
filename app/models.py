# User model (DB schema)

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'