from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Username = request.form.get('Username')
        password3 = request.form.get('password3')

        user = User.query.filter_by(Username=Username).first()
        if user:
            if check_password_hash(user.password, password3):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                print("User logged in:", user.Username)
                return redirect(url_for('main.FindAdv'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')
    
    return render_template("auth.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    # session.pop('user_id', None)
    session.clear()
    logout_user()
    return redirect(url_for('main.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        Username = request.form.get('createUsername')
        password1 = request.form.get('password')
        password2 = request.form.get('confirmPassword')
        birthdate = request.form.get('birthdate')
        country = request.form.get('country')

        if not all([email, Username, password1, password2, birthdate, country]):
            flash('Please fill out all fields.', category='error')
            return redirect(url_for('auth.sign_up', form='signup'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            return redirect(url_for('auth.sign_up', form='signup'))
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            return redirect(url_for('auth.sign_up', form='signup'))
        elif len(Username) < 2:
            flash('Username must be greater than 1 character.', category='error')
            return redirect(url_for('auth.sign_up', form='signup'))
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            return redirect(url_for('auth.sign_up', form='signup'))
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            return redirect(url_for('auth.sign_up', form='signup'))
        else:
            new_user = User(Username=Username,email=email,  password=generate_password_hash(password1, method='pbkdf2:sha256'),dateofbirth=birthdate, country=country)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("auth.html", user=current_user)