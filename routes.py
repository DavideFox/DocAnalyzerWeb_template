from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from db import get_db
import os, pdfplumber, json
from collections import Counter
import nltk

bp = Blueprint('routes', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
nltk.download('stopwords')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()
    documents = conn.execute('SELECT * FROM documents WHERE user_id = ?', (current_user.id,)).fetchall()
    return render_template('dashboard.html', credits=user['credits'], documents=documents)


@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['document']
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        with pdfplumber.open(filepath) as pdf:
            text = ''.join(page.extract_text() or '' for page in pdf.pages)
            words = text.split()
            stop_it = set(nltk.corpus.stopwords.words('italian'))
            filtered_words = [w for w in words if w.lower() not in stop_it]
            top_words = Counter(filtered_words).most_common(20)
            conn = get_db()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()
            if user['credits'] <= 0:
                flash("Crediti esauriti.")
                return redirect(url_for('routes.dashboard'))
            conn.execute('UPDATE users SET credits = credits - 1 WHERE id = ?', (current_user.id,))
            conn.execute('INSERT INTO documents (user_id, filename, word_count, page_count, top_words) VALUES (?, ?, ?, ?, ?)',
                         (current_user.id, filename, len(words), len(pdf.pages), json.dumps(top_words)))
            conn.commit()
        return redirect(url_for('routes.dashboard'))


@bp.route('/document/<int:doc_id>')
@login_required
def document(doc_id):
    conn = get_db()
    doc = conn.execute('SELECT * FROM documents WHERE id = ? AND user_id = ?', (doc_id, current_user.id)).fetchone()
    if not doc:
        flash("Documento non trovato.")
        return redirect(url_for('routes.dashboard'))
    top_words = json.loads(doc['top_words'])
    return render_template('document.html', doc=doc, top_words=top_words)


@bp.route('/account')
@login_required
def account():
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()
    return render_template('account.html', user=user)
