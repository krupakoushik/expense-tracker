import sqlite3

conn = sqlite3.connect("account.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date TEXT, 
        txn TEXT, 
        amount REAL , 
        note TEXT
)
""")

def add_expense():
    date = input("Enter date (DD-MM-YYYY): ").strip()
    txn = input("Enter the type of transaction (CREDIT or DEBIT): ").strip().upper()
    amount = float(input("Enter amount: ").strip())
    note = input("Enter note: ").strip().lower()

    c.execute("INSERT INTO expenses (date, txn, amount, note) VALUES (?, ?, ?, ?)", (date, txn, amount, note))
    conn.commit()
    print("Expense Recorded")

def show_balance():
    c.execute("SELECT txn, amount FROM expenses")
    rows = c.fetchall()
    balance = 0

    for txn, amount in rows:
        if txn.upper() == "CREDIT":
            balance += amount
        elif txn.upper() == "DEBIT":
            balance -= amount
    
    print("--------------------------------------")
    print(f"\nCurrent Balance: ₹{balance:.2f}\n")
    print("--------------------------------------\n")

add_expense()
show_balance()