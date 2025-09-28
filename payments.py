from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from db import get_db
import stripe

bp = Blueprint('payments', __name__)


# -------- Stipe configuration --------
stripe.api_key = 'sk_test_...'
DOMAIN = 'http://localhost:5000'
PRICING = {
    "starter": {"price": 19, "credits": 50},
    "pro": {"price": 49, "credits": 200},
    "enterprise": {"price": 89, "credits": 500}
}


@bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    plan = request.form['plan']
    if plan not in PRICING:
        return "Invalid plan", 400
    price = PRICING[plan]['price'] * 100
    credits = PRICING[plan]['credits']
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': f'Abbonamento {plan.capitalize()} - {credits} crediti'},
                'unit_amount': price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}&plan=' + plan,
        cancel_url=DOMAIN + '/account',
        metadata={'user_id': current_user.id, 'credits': credits}
    )
    return redirect(checkout_session.url, code=303)



@bp.route('/success')
def success():
    session_id = request.args.get('session_id')
    plan = request.args.get('plan')
    if not session_id or not plan:
        return "Dati mancanti", 400
    session_data = stripe.checkout.Session.retrieve(session_id)
    user_id = int(session_data['metadata']['user_id'])
    credits = int(session_data['metadata']['credits'])
    conn = get_db()
    conn.execute('UPDATE users SET credits = credits + ? WHERE id = ?', (credits, user_id))
    conn.commit()
    return f"Pagamento completato! Hai ricevuto {credits} crediti. <a href='/dashboard'>Torna alla dashboard</a>"



@bp.route('/invoices')
@login_required
def invoices():
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()
    stripe_customer = stripe.Customer.search(query=f"email:'{user['email']}'")["data"]
    if not stripe_customer:
        return render_template('invoices.html', invoices=[])
    customer_id = stripe_customer[0]["id"]
    invoice_list = stripe.Invoice.list(customer=customer_id, limit=10)
    return render_template('invoices.html', invoices=invoice_list)
