from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def db():
    conn = sqlite3.connect("account.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date DATE(10), 
            txn CHAR(6), 
            amount FLOAT(14) , 
            note TEXT(30)
    )
    """)
    conn.commit()
    conn.close()


@app.route('/')
def home():

    conn = sqlite3.connect("account.db")
    c = conn.cursor()

    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()

    c.execute("SELECT txn, amount FROM expenses")
    txns = c.fetchall()
    balance=0
    for txn, amount in txns:
        if txn.upper() == "CREDIT":
            balance += amount
        elif txn.upper() == "DEBIT":
            balance -= amount

    conn.commit()
    conn.close()
    return render_template("index.html", transactions=rows, balance=balance)


@app.route('/add', methods=["GET", "POST"])
def add_txn():
    if request.method == "POST":
        date = request.form['date']
        txn = request.form['txn']
        amount = request.form['amount']
        note = request.form['note']

        conn = sqlite3.connect("account.db")
        c = conn.cursor()
        c.execute("INSERT INTO expenses (date, txn, amount, note) VALUES (?, ?, ?, ?)", (date, txn, amount, note))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    
    return render_template("add_txn.html")


@app.route('/delete/<int:txn_id>')
def del_txn(txn_id):
    conn = sqlite3.connect("account.db")
    c = conn.cursor()

    c.execute("DELETE FROM expenses WHERE id=?", (txn_id, ))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/edit/<int:txn_id>', methods=["GET", "POST"])
def edit_txn(txn_id):
    conn = sqlite3.connect("account.db")
    c = conn.cursor()

    if request.method == 'POST':
        date = request.form['date']
        txn = request.form['txn']
        amount = request.form['amount']
        note = request.form['note']

        c.execute("UPDATE expenses SET date = ?, txn = ?, amount = ?, note = ? WHERE id = ?",  (date, txn, amount, note, txn_id, ))
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))
    
    c.execute("SELECT * FROM expenses where id = ?", (txn_id, ))
    txn = c.fetchone()
    conn.close()

    return render_template('edit_txn.html', txn=txn)

if __name__ == "__main__":
    db()
    app.run(debug=True)