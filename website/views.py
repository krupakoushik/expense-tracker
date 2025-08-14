from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from .models import User, Transaction, Category
from datetime import datetime, date
from . import db
from dotenv import load_dotenv
import os

load_dotenv()
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.txn_date.desc()).all()

    balance = sum(
        t.amount if t.txn == "CREDIT" else -t.amount
        for t in transactions
    )

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        # ---- Add / Edit Transaction ----
        if form_type == "transaction":
            transaction_id = request.form.get('transaction_id')
            category_id = request.form.get('category_id')

            # --- QUICK CATEGORY UPDATE (inline form) ---
            if transaction_id and category_id and not request.form.get('amount'):
                txn_obj = Transaction.query.get_or_404(transaction_id)
                if txn_obj.user_id != current_user.id:
                    flash("Not authorized to edit this transaction!", category='error')
                    return redirect(url_for('views.home'))

                txn_obj.category_id = int(category_id)
                db.session.commit()
                flash("Category updated!", category="success")
                return redirect(url_for('views.home'))

            # --- FULL ADD/EDIT TRANSACTION ---
            txn_date = request.form.get('date')
            txn_type = request.form.get('txn')
            amount = request.form.get('amount')
            note = request.form.get('note')

            try:
                amount = float(amount)
            except (ValueError, TypeError):
                flash("Invalid Amount!", category='error')
                return redirect(url_for('views.home'))

            try:
                txn_date = datetime.strptime(txn_date, "%Y-%m-%d") if txn_date else None
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.", category="error")
                return redirect(url_for('views.home'))

            category_id = int(category_id) if category_id else None

            if transaction_id:  # Editing
                txn_obj = Transaction.query.get_or_404(transaction_id)
                if txn_obj.user_id != current_user.id:
                    flash("Not authorized to edit this transaction!", category='error')
                    return redirect(url_for('views.home'))

                txn_obj.txn_date = txn_date
                txn_obj.txn = txn_type
                txn_obj.amount = amount
                txn_obj.category_id = category_id
                txn_obj.note = note
                flash("Transaction updated!", category="success")
            else:  # Adding
                new_txn = Transaction(
                    txn_date=txn_date,
                    amount=amount,
                    txn=txn_type,
                    category_id=category_id,
                    note=note,
                    user_id=current_user.id
                )
                db.session.add(new_txn)
                flash("Transaction added!", category="success")

            db.session.commit()
            return redirect(url_for('views.home'))


        # ---- Add / Rename Category ----
        elif form_type == "category":
            category_id = request.form.get('category_id')
            category_name = request.form.get('category', '').strip()

            if not category_name:
                flash("Category name cannot be empty.", category="error")
                return redirect(url_for('views.home'))

            if category_id:  # Rename
                cat = Category.query.get_or_404(category_id)
                if cat.user_id != current_user.id:
                    flash("Not authorized to rename this category!", category='error')
                    return redirect(url_for('views.home'))

                cat.name = category_name
                print(category_name)
                flash("Category renamed successfully!", category="success")
            else:  # Add
                new_cat = Category(name=category_name, user_id=current_user.id)
                db.session.add(new_cat)
                print(new_cat)
                flash("Category created successfully!", category="success")

            db.session.commit()
            return redirect(url_for('views.home'))

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'home.html',
        transaction=transactions,
        current_date=date.today().isoformat(),
        categories=categories,
        balance=balance,
        user=current_user
    )

@views.route('/cdelete/<int:id>')
@login_required
def categoriesdel(id):
    cat = Category.query.get_or_404(id)
    if cat.user_id != current_user.id:
        flash("You are not allowed to delete this category!", category='error')
        return redirect(url_for('views.home'))
    db.session.delete(cat)
    db.session.commit()
    flash("Category deleted successfully!", category='success')
    return redirect(url_for('views.home'))

@views.route('/delete/<int:id>')
@login_required
def delete(id):
    del_txn = Transaction.query.get_or_404(id)
    if del_txn.user_id != current_user.id:
        flash("You are not allowed to delete this transaction!", category='error')
        return redirect(url_for('views.home'))
    db.session.delete(del_txn)
    db.session.commit()
    flash("Transaction deleted successfully!", category='success')
    return redirect(url_for('views.home'))


@views.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    import requests

    url = "https://api.coingecko.com/api/v3/simple/price"

    name = request.form.get("cryp") 

    params = {
        "symbols": name,  # comma-separated coin IDs
        "vs_currencies": "inr",     # comma-separated fiat/crypto currencies
        "x_cg_api_key": os.getenv("COINGECKO")  # your API key
    }

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        crypto_price = response.json()
    else:
        flash("Couldn\'t fetch the data.", category="error")
        crypto_price = {}
    
    return render_template('portfolio.html', crypto=crypto_price, user=current_user)


@views.route('/stats')
@login_required
def stats(id):
    pass


@views.route('/goal')
@login_required
def goals(id):
    pass