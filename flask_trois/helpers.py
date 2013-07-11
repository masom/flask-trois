from functools import wraps

from flask import session, g, redirect

from flask_trois import app

from shopify_trois import Credentials
from shopify_trois.engines.http import Json as Shopify


def setup_shopify_adapter(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'shop_name' in session or not 'access_token' in session:
            return redirect("/")

        access_token = session['access_token']
        shop_name = session['shop_name']
        base_credentials = app.config.get('SHOPIFY_CREDENTIALS')

        credentials = Credentials(
            api_key=base_credentials.api_key,
            secret=base_credentials.secret,
            oauth_access_token=access_token
        )

        g.shopify = Shopify(shop_name=shop_name, credentials=credentials)

        return f(*args, **kwargs)
    return decorated_function
