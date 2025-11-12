from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from db import db, User

bp = Blueprint('auth', __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Cerca l'utente nel database tramite SQLAlchemy
        user = User.query.filter_by(email=email).first()         
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        flash('Credenziali non valide.')
    return render_template('login.html')


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password_hash = generate_password_hash(request.form['password']) 
        # Controlla se l'email è già registrata
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email già registrata.')
            return redirect(url_for('auth.register'))
        # Crea un nuovo utente
        new_user = User(email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione completata. Puoi ora effettuare il login.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
