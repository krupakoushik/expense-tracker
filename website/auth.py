from flask import Blueprint, url_for, render_template, request, flash, redirect
from .models import User, Category
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Email and Password does not match or invalid.', category='error')
        else:
            flash('Email does not exist', category='error')

    
    return render_template('login.html', user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = (request.form.get('username')).strip()
        email = (request.form.get('email')).strip()
        password = (request.form.get('password')).strip()
        cpass = (request.form.get('cpass')).strip()

        print("Form Data:", request.form)

# check input data
        if not username or not email or not password or not cpass:
            flash('All fields are required.', category='error')
        elif len(email) < 4:
            flash('Email is too short or invalid.', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password) < 8:
            flash('Password is too short.', category='error')
        elif password != cpass:
            flash('Passwords do not match.', category='error')
        
        else:
            existing_user = User.query.filter(
                (User.email == email) | (User.username == username)
            ).first()
            if existing_user:
                flash('Email or username already in use.', category='error')
            else:
                new_user = User(
                    username=username,
                    email=email,
                    password=generate_password_hash(password, method='pbkdf2:sha256')
                )
                db.session.add(new_user)
                db.session.commit()

#default category
                def_cat = Category(name="None", user_id=new_user.id)
                db.session.add(def_cat)
                db.session.commit()

                login_user(new_user, remember=True)
                flash('Account Created Successfully!', category='success')

                return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out Successfully!', category='success')
    return redirect(url_for('auth.login'))
