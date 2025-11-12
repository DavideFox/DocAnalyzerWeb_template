from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Istanza globale del database (da inizializzare in app.py)
db = SQLAlchemy()


# ----------------------- MODELLI DEL DATABASE -----------------------

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    credits = db.Column(db.Integer, default=10)
    role = db.Column(db.String(50), default='user')

    documents = db.relationship('Document', backref='user', lazy=True)

    @property
    def is_admin(self):
        return self.id == 1 or self.role == "admin"

    def __repr__(self):
        return f"<User {self.email}>"


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    word_count = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    top_words = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Document {self.filename}>"



# ----------------------- FUNZIONE DI INIZIALIZZAZIONE -----------------------

def init_db(app):
    """    Inizializza il database collegandolo a Flask. Crea le tabelle se non esistono.    """
    db.init_app(app)

    with app.app_context():
        db.create_all()





'''
DB tabels

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            credits INTEGER DEFAULT 10,
            role TEXT DEFAULT 'user'
        )

        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            word_count INTEGER,
            page_count INTEGER,
            top_words TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
'''