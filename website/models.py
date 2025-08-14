from . import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    transactions = db.relationship('Transaction', backref='owner', lazy=True)
    categories = db.relationship('Category', backref='owner', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    transactions = db.relationship('Transaction', backref='category', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    txn_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    amount = db.Column(db.Float, nullable=False)
    txn = db.Column(db.String(6), nullable=False, server_default='DEBIT')
    note = db.Column(db.String, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        CheckConstraint("txn IN ('CREDIT', 'DEBIT')", name="check_txn_type"),
    )

