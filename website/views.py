from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from .models import User, Transaction, Category
from datetime import datetime
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.txn_date.desc()).all()


    balance = 0
    for t in transactions:
        if t.txn == "CREDIT":
            balance += t.amount
        else:
            balance -= t.amount


#add
    if request.method == 'POST':
        txn_date = request.form.get('date')
        txn = request.form.get('txn')
        amount = request.form.get('amount')
        category_id = request.form.get('category_id')
        note = request.form.get('note')

#amount
        try:
            amount = float(amount)
        except ValueError:
            flash("Invalid Amount!", category='error')
            return redirect(url_for('views.home'))

#date
        if txn_date:
            try:
                txn_date = datetime.strptime(txn_date, "%Y-%m-%d")
            except ValueError:
                flash("Invalid date format. Use DD-MM-YYYY.", category="error")
                return redirect(url_for('views.home'))
        else:
            txn_date = None


#category
        category_id = int(category_id) if category_id else None


        new_txn = Transaction(
            txn_date = txn_date,
            amount=amount,
            txn = txn,
            category_id = category_id,
            note=note,
            user_id = current_user.id
        )
        db.session.add(new_txn)
        db.session.commit()

        flash("Transaction added!", category="success")
        return redirect(url_for('views.home'))

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', transaction=transactions, categories=categories, balance=balance, user=current_user)

@views.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    if request.method == "POST":
        category = request.form.get('category').strip().upper()

        if category:
            new_cat = Category(name=category, user_id=current_user.id)
            db.session.add(new_cat)
            db.session.commit()
            flash('Category created successfully!', category='success')
        else:
            flash('Category name cannot be empty.', category='error')

        return redirect(url_for('views.categories'))

    cats = Category.query.filter(Category.user_id == current_user.id, Category.name != 'None').all()
    return render_template('categories.html', categories=cats, user=current_user)


@views.route('categories/delete/<int:id>')
@login_required
def categoriesdel(id):

    cat_id = Category.query.get_or_404(id)

    if cat_id.user_id != current_user.id:
        flash("You are not allowed to delete this category!", category='error')
        return redirect(url_for('views.categories'))

    db.session.delete(cat_id)
    db.session.commit()
    
    flash("Cateopry Deleted Successfully!", category='success')
    return redirect(url_for('views.categories'))

@views.route('/update-category/<int:id>', methods=['POST'])
@login_required
def update_category(id):
    txn = Transaction.query.get_or_404(id)

    if txn.user_id != current_user.id:
        flash("You are not allowed to edit this transaction!", category='error')
        return redirect(url_for('views.home'))

    category_id = request.form.get('category_id')
    txn.category_id = int(category_id) if category_id else None

    db.session.commit()
    flash("Category updated successfully!", category='success')
    return redirect(url_for('views.home'))


@views.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit(id):

    edit_txn = Transaction.query.get_or_404(id)
    
    if edit_txn.user_id != current_user.id:
        flash("You are not allowed to edit this transaction!", category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        txn_date = request.form.get('date')
        txn = request.form.get('txn')
        amount = request.form.get('amount')
        category_id = request.form.get('category_id')
        note = request.form.get('note')

        if txn_date:
            try:
                edit_txn.txn_date = datetime.strptime(txn_date, "%Y-%m-%d")
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.", category="error")
                return redirect(url_for('views.edit', id=id))

        edit_txn.txn = txn
        edit_txn.amount=float(amount)
        edit_txn.category_id = category_id if category_id else None
        edit_txn.note=note
        
        db.session.commit()

        flash("Transaction updated successfully!", category="success")
        return redirect(url_for('views.home'))

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('edit_txn.html', txn=edit_txn, categories=categories, user=current_user)

@views.route('/delete/<int:id>')
@login_required
def delete(id):

    del_txn = Transaction.query.get_or_404(id)

    if del_txn.user_id != current_user.id:
        flash("You are not allowed to delete this transaction!", category='error')
        return redirect(url_for('views.home'))

    db.session.delete(del_txn)
    db.session.commit()
    
    flash("Transaction Deleted Successfully!", category='success')
    return redirect(url_for('views.home'))


@views.route('/investments')
@login_required
def investments(id):
    pass


@views.route('/stats')
@login_required
def stats(id):
    pass


@views.route('/goal')
@login_required
def goals(id):
    pass