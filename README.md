# DocuPro – Analisi Documenti PDF con Flask + MySQL

DocuPro è un'applicazione Flask professionale per caricare documenti PDF, analizzarli (numero di parole, pagine, parole più usate), gestire utenti, crediti, abbonamenti Stripe e pannello admin con grafici.

---

## 🛠️ Tecnologie
- Python + Flask
- Tailwind CSS
- SQLite
- Stripe Checkout
- Flask-Mail
- Chart.js (per dashboard admin)

---

## 🚀 Setup Locale (sviluppo)

1. **Crea ambiente virtuale:**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configura db**

3. **Configura .env** (vedi file `.env` incluso)

4. **Avvia l'app:**

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

## 📧 Email
- Richiede Gmail (app password) o SMTP compatibile
- Email di benvenuto e alert all’admin

---

## 📂 Struttura Progetto
```
/templates/
    login.html, register.html, dashboard.html, document.html,
    account.html, admin.html, invoices.html, admin_dashboard.html
/uploads/
/app.py
/requirements.txt
/.env
```

---

## 👨‍💻 Autore
Generato con ❤️ da GPT-4 per un'app di analisi documenti PDF moderna e pronta per il deploy.

## routing

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
@app.route('/logout')
@app.route('/dashboard')
@app.route('/upload', methods=['POST'])
@app.route('/document/<int:doc_id>')
@app.route('/account')
@app.route('/create-checkout-session', methods=['POST'])
@app.route('/success')
@app.template_filter('datetimeformat')
@app.route('/admin')
@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@app.route('/invoices')
@app.route('/admin/dashboard')