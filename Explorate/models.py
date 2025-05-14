
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.Username}>'


class Adventure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adventure_name = db.Column(db.String(255), nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    pets = db.Column(db.Integer, nullable=False)
    choice = db.Column(db.String(10), nullable=False)  # "Yes" or "No"

    def __init__(self, adventure_name, adults, children, pets, choice):
        self.adventure_name = adventure_name
        self.adults = adults
        self.children = children
        self.pets = pets
        self.choice = choice


class UserSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=True)
    answer_1 = db.Column(db.String(100), nullable=True)
    answer_2 = db.Column(db.String(100), nullable=True)
    answer_3 = db.Column(db.String(100), nullable=True)
    answer_4 = db.Column(db.String(100), nullable=True)
    answer_5 = db.Column(db.String(100), nullable=True)
    adventure_id = db.Column(db.Integer, db.ForeignKey('adventure.id'), nullable=False)

    adventure = db.relationship('Adventure', backref=db.backref('user_selections', lazy=True))

    def __repr__(self):
        return f'<UserSelection {self.id} - Session: {self.session_id}>'


class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    selected_state = db.Column(db.String(50), nullable=False)
    recommendation_1 = db.Column(db.String(200))
    recommendation_2 = db.Column(db.String(200))
    recommendation_3 = db.Column(db.String(200))
    recommendation_4 = db.Column(db.String(200))
