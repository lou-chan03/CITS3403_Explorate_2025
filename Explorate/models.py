
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    dateofbirth = db.Column(db.String(10), nullable=False)
    adventure = db.relationship('Adventure')

    def __repr__(self):
        return f'<User {self.Username}>'


class Adventure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adventure_name = db.Column(db.String(255), nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    pets = db.Column(db.Integer, nullable=False)
    choice = db.Column(db.String(10), nullable=False)  # "Yes" or "No"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, adventure_name, adults, children, pets, choice,user_id):
        self.user_id = user_id
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
    session_id = db.Column(db.String(50), db.ForeignKey('user_selection.session_id'), unique=True, nullable=False)
    selected_state = db.Column(db.String(50), nullable=False)
    recommendation_1 = db.Column(db.String(200))
    recommendation_2 = db.Column(db.String(200))
    recommendation_3 = db.Column(db.String(200))
    recommendation_4 = db.Column(db.String(200))

    user_selection = db.relationship('UserSelection', backref=db.backref('recommendations', lazy=True))

    def __repr__(self):
        return f'<Recommendations {self.id} - Session: {self.session_id}>'

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #adventure_id = db.Column(db.Integer, db.ForeignKey('adventure.id'), nullable=False) 
    
    location_rating = db.Column(db.Integer, nullable=False)
    food_rating = db.Column(db.Integer, nullable=False)
    attractions_rating = db.Column(db.Integer, nullable=False)
    accommodation_rating = db.Column(db.Integer, nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)
    
    #user = db.relationship('User', back_populates='ratings')
    #adventures = db.relationship('Adventure', back_populates='ratings')