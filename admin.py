from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from db import db, User, Document

bp = Blueprint('admin', __name__)


@bp.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return "Accesso negato", 403
    # recupera tutti gli utenti
    users = User.query.order_by(User.id).all()
    return render_template('admin.html', users=users)


@bp.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return "Accesso negato", 403
    # controllo se l'utente esiste
    user = User.query.get(user_id)
    if not user:
        flash("Utente non trovato.")
        return redirect(url_for('admin.admin_panel'))
    # Cancella tutti i documenti dell’utente
    Document.query.filter_by(user_id=user_id).delete()
    # Cancella l’utente
    db.session.delete(user)
    db.session.commit()
    flash("Utente e documenti eliminati con successo.")
    return redirect(url_for('admin.admin_panel'))



@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Accesso negato", 403 
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    email_filter = request.args.get('email')
    # Base query con eventuali filtri
    query = Document.query
    if from_date:
        query = query.filter(Document.created_at >= from_date)
    if to_date:
        query = query.filter(Document.created_at <= to_date)
    if email_filter:
        user = User.query.filter_by(email=email_filter).first()
        if user:
            query = query.filter(Document.user_id == user.id)
        else:
            query = query.filter(False)  # Nessun utente trovato → nessun risultato
    # Query aggregata per anno/mese — compatibile con tutti i database
    stats = (
        query.with_entities(
            extract('year', Document.created_at).label('year'),
            extract('month', Document.created_at).label('month'),
            func.count(Document.id).label('count')
        )
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    # Crea liste leggibili per il template
    months = [f"{int(row.year)}-{int(row.month):02d}" for row in stats]
    counts = [row.count for row in stats]
    # Totali globali
    user_count = User.query.count()
    document_count = Document.query.count()

    return render_template(
        "admin_dashboard.html",
        stats={'user_count': user_count, 'document_count': document_count},
        months=months,
        counts=counts
    )