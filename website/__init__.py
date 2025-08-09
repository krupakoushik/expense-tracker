from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'duckthisshitimout'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Category, Transaction

    create_db(app)

    manager = LoginManager()
    manager.login_view = 'auth.login'
    manager.init_app(app)

    @manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    return app

def create_db(app):
    if not path.exists('website/' + NAME):
        with app.app_context():
            db.create_all()
        print('Database created')
