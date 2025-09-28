from flask import Flask
from flask_login import LoginManager
from db import init_db, get_db, User
import os
from auth import bp as auth_bp
from routes import bp as routes_bp
from payments import bp as payments_bp
from admin import bp as admin_bp


# -------- init Flask --------
app = Flask(__name__)
app.secret_key = 'your_secret_key'


# -------- Flask-Login setup --------
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if row:
        return User(row["id"], row["email"], row["role"], row["credits"])
    return None


# -------- Import blueprints --------
app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(admin_bp)


# -------- Start --------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)



'''     
------------ riepilogo routes ------------
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
'''