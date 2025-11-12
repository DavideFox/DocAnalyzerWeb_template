from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from db import db, User, Document
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
    # Recupera utente e documenti tramite ORM
    user = User.query.get(current_user.id)
    documents = Document.query.filter_by(user_id=current_user.id).order_by(Document.created_at.desc()).all()
    return render_template('dashboard.html', credits=user.credits, documents=documents)


@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['document']
    if not file or not file.filename.endswith('.pdf'):
        flash("Carica un file PDF valido.")
        return redirect(url_for('routes.dashboard'))
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    # elabora file
    with pdfplumber.open(filepath) as pdf:
        text = ''.join(page.extract_text() or '' for page in pdf.pages)
        words = text.split()
        stop_it = set(nltk.corpus.stopwords.words('italian'))
        filtered_words = [w for w in words if w.lower() not in stop_it]
        top_words = Counter(filtered_words).most_common(20)
        # Aggiorna i crediti dell’utente
        user = User.query.get(current_user.id)
        if user.credits <= 0:
            flash("Crediti esauriti.")
            return redirect(url_for('routes.dashboard'))
        user.credits -= 1
        # Crea nuovo documento
        new_doc = Document(
            user_id=current_user.id,
            filename=filename,
            word_count=len(words),
            page_count=len(pdf.pages),
            top_words=json.dumps(top_words)
        )
        db.session.add(new_doc)
        db.session.commit()
    flash("Documento caricato con successo!")
    return redirect(url_for('routes.dashboard'))


@bp.route('/document/<int:doc_id>')
@login_required
def document(doc_id):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first()
    if not doc:
        flash("Documento non trovato.")
        return redirect(url_for('routes.dashboard'))
    top_words = json.loads(doc.top_words or "[]")
    return render_template('document.html', doc=doc, top_words=top_words)


@bp.route('/document_demo')
def document_demo():
    doc = {
        "filename": "LucioBattisti_biografia.pdf",
        "word_count": 6047,
        "page_count": 12,
        "top_words": [
            ["Battisti", 74], ["canzone", 33], ["più", 30], ["successo", 23],
            ["Battisti,", 21], ["stesso", 21], ["disco", 21], ["testi", 20],
            ["anni", 20], ["Mogol", 18], ["Mogol,", 16], ["Lucio", 15],
            ["primo", 13], ["-", 12], ["viene", 12], ["album", 12],
            ["due", 11], ["brano", 11], ["Battisti.", 10], ["quali", 9],
        ],
    }
    return render_template('document.html', doc=doc, top_words=doc['top_words'])


@bp.route('/account')
@login_required
def account():
    user = User.query.get(current_user.id)
    return render_template('account.html', user=user)