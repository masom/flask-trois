from flask import Blueprint, render_template, g, session
from shopify_trois.engines.http import Json as Shopify

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates/auth',
)

@store.route('/')
@store.route('/login', methods=['GET', 'POST'])
def login():

    if 'store' in session:
        return redirect(url_for('store.view'))

    if request.method == 'POST':
        session['store'] = request.form['store']

        shopify = Shopify(store_name=session['store'], credentials=credentials)
        return redirect(url_for('store.view'))

    return render_template('login')
