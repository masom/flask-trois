from flask import (Blueprint, render_template, session, redirect, url_for,
                   request, abort)

from shopify_trois import Credentials
from shopify_trois.engines.http import Json as Shopify

from flask_trois import app

auth = Blueprint('auth', __name__)


@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if 'store' in session:
        return redirect(url_for('store.view'))

    if request.method == 'POST':
        # Get the base app credentials
        credentials = app.config.get('SHOPIFY_CREDENTIALS')

        #Setup a session to store the shop_name
        session['shop_name'] = shop_name = request.form['shop_name']

        #Setup a shopify adapter instance to create the authorization url
        shopify = Shopify(shop_name=shop_name, credentials=credentials)

        #Generate a url pointing back to an action on this blueprint
        redirect_to = url_for('.shopify_callback', _external=True)

        #Generate the oauth authorization url with a redirection to our app
        oauth_url = shopify.oauth_authorize_url(
            redirect_to=redirect_to
        )

        return redirect(oauth_url)

    return render_template('auth/login.html')


@auth.route('/shopify_callback')
def shopify_callback():
    if not 'shop_name' in session:
        abort(401)

    shop_name = session['shop_name']

    # Get the base app credentials
    base_credentials = app.config.get('SHOPIFY_CREDENTIALS')

    #Generate a new credential object with the base values
    credentials = Credentials(
        api_key=base_credentials.api_key,
        secret=base_credentials.secret
    )

    #Setup a shopify adapter instance to create the authorization url
    shopify = Shopify(shop_name=shop_name, credentials=credentials)

    #Verify the signature
    if not shopify.verify_signature(request.args):
        raise Exception("invalid signature")

    #Update the credentials object with the provided temporary code
    credentials.code = request.args.get('code')

    #Exchange the code for an access token
    shopify.setup_access_token()

    #Store the access token in the session
    session['access_token'] = credentials.oauth_access_token

    return redirect(url_for('shop.view'))
