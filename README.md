# DocuPro – Analisi Documenti PDF con Flask + SQLite

DocuPro è un'applicazione Flask di esmpio per caricare documenti PDF, analizzarli (numero di parole, pagine, parole più usate), gestire utenti, crediti, abbonamenti Stripe e pannello admin con grafici.

---

## 🛠️ Tecnologie
- Python + Flask
- Custom CSS e Bootstrap 5
- SQLAlchemy
- Stripe Checkout
- Chart.js (per dashboard admin)

---

## 🚀 Setup Locale (sviluppo)

1. **Crea ambiente virtuale:**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Avvia l'app:**

```bash
python app.py
```

---

## 🔐 Admin
- L’utente con ID `1` è admin
- Accedi a `/admin` e `/admin/dashboard`

## 📊 Dashboard
- Grafici con filtro date/email
- Gestione utenti e ruoli

## 💳 Stripe
- Configura `STRIPE_SECRET_KEY` nel `.env`
- Checkout attivo in `/account`

---


---

## 👨‍💻 Autore
DavideFox


## routing

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
@app.route('/logout')
@app.route('/dashboard')
@app.route('/upload', methods=['POST'])
@app.route('/document/<int:doc_id>')
@app.route('/document_demo/')
@app.route('/account')
@app.route('/create-checkout-session', methods=['POST'])
@app.route('/success')
@app.template_filter('datetimeformat')
@app.route('/admin')
@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@app.route('/invoices')
@app.route('/admin/dashboard')