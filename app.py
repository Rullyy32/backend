from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
app = Flask(__name__)

app.secret_key = 'supersentimentalsecrettheory'

def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        try:
        # Cek apakah email sudah terdaftar
            c.execute("SELECT * FROM users WHERE email = ?", (email,))

            if c.fetchone():
                flash('Email is already registered!', 'error')
            else:
                c.execute("INSERT INTO users (nama, email, password) VALUES (?, ?, ?)", (nama, email, password))
                conn.commit()
                flash('Register successful! Please Login.', 'success')
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Error : Failed to save data.', 'error')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = c.fetchone()

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('join'))
        else:
            flash('Invalid Email or Password!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
