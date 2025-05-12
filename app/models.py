
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Adventure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adventure_name = db.Column(db.String(255), nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    pets = db.Column(db.Integer, nullable=False)
    choice = db.Column(db.String(10), nullable=False)  # "Yes" or "No"

    # Define reverse relationship to UserSelection
    #user_selections = db.relationship('UserSelection', back_populates='adventure', cascade='all, delete-orphan')

    def __init__(self, adventure_name, adults, children, pets, choice):
        self.adventure_name = adventure_name
        self.adults = adults
        self.children = children
        self.pets = pets
        self.choice = choice



class UserSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing unique ID
    session_id = db.Column(db.String(50), nullable=True)  # Optional session ID for tracking users
    answer_1 = db.Column(db.String(100), nullable=True)  # Answer for question 1
    answer_2 = db.Column(db.String(100), nullable=True)  # Answer for question 2
    answer_3 = db.Column(db.String(100), nullable=True)  # Answer for question 3
    answer_4 = db.Column(db.String(100), nullable=True)  # Answer for question 4
    answer_5 = db.Column(db.String(100), nullable=True)  # Answer for question 5
    adventure_id = db.Column(db.Integer, db.ForeignKey('adventure.id'), nullable=False)  # Foreign key to Adventure

    # Establish relationship with Adventure
    adventure = db.relationship('Adventure', backref=db.backref('user_selections', lazy=True))

    def __repr__(self):
        return f'<UserSelection {self.id} - Session: {self.session_id}>'


# User model (DB schema)

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

