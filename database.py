import sqlite3

def get_connection():
    return sqlite3.connect('expenses.db') 

def create_table():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            date TEXT,
            name TEXT,
            category TEXT,
            amount REAL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            month TEXT UNIQUE,
            amount REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_expense(date, name, category, amount):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO expenses (date, name, category, amount) VALUES (?, ?, ?, ?)', 
              (date, name, category, amount))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT rowid, date, name, category, amount FROM expenses')
    data = c.fetchall()
    conn.close()
    return data

def delete_expense(row_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE rowid = ?', (row_id,))
    conn.commit()
    conn.close()

def set_income(month, amount):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO incomes (month, amount) VALUES (?, ?)', (month, amount))
    conn.commit()
    conn.close()

def get_income(month):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT amount FROM incomes WHERE month = ?', (month,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0.0 