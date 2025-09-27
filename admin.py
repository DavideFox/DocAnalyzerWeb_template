from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from db import get_db

bp = Blueprint('admin', __name__)


@bp.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return "Accesso negato", 403
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    return render_template('admin.html', users=users)


@bp.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return "Accesso negato", 403
    conn = get_db()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.execute('DELETE FROM documents WHERE user_id = ?', (user_id,))
    conn.commit()
    return redirect(url_for('admin.admin_panel'))


@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Accesso negato", 403
    conn = get_db()
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    email_filter = request.args.get('email')
    query = "SELECT strftime('%Y-%m', created_at) as month, COUNT(*) FROM documents WHERE 1=1"
    params = []
    if from_date:
        query += " AND created_at >= ?"
        params.append(from_date)
    if to_date:
        query += " AND created_at <= ?"
        params.append(to_date)
    if email_filter:
        user = conn.execute("SELECT id FROM users WHERE email = ?", (email_filter,)).fetchone()
        if user:
            query += " AND user_id = ?"
            params.append(user['id'])
    stats = conn.execute(query + " GROUP BY month", tuple(params)).fetchall()
    months = [row['month'] for row in stats]
    counts = [row['COUNT(*)'] for row in stats]
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    document_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    return render_template("admin_dashboard.html",
        stats={'user_count': user_count, 'document_count': document_count},
        months=months,
        counts=counts
    )
