from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from db import get_db, User

bp = Blueprint('auth', __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if user and check_password_hash(user['password'], password):
            user_obj = User(user["id"], user["email"], user["role"], user["credits"])
            login_user(user_obj)
            return redirect(url_for('routes.dashboard'))
        flash('Credenziali non valide.')
    return render_template('login.html')


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            return redirect(url_for('auth.login'))
        except:
            flash('Email già registrata.')
    return render_template('register.html')


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
