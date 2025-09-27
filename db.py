import sqlite3
from flask_login import UserMixin

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            credits INTEGER DEFAULT 10,
            role TEXT DEFAULT 'user'
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            word_count INTEGER,
            page_count INTEGER,
            top_words TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()



# Flask-Login User class
class User(UserMixin):
    def __init__(self, id, email, role, credits):
        self.id = id
        self.email = email
        self.role = role
        self.credits = credits

    @property
    def is_admin(self):   #it sets the admin
        return self.id == 1 or self.role == "admin"
