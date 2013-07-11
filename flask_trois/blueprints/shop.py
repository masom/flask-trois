from flask import Blueprint, render_template, g
from flask_trois.helpers import setup_shopify_adapter

from shopify_trois.models import Shop


shop = Blueprint(
    'shop',
    __name__,
    url_prefix='/shop'
)


@shop.route('/')
@setup_shopify_adapter
def view():
    shop = g.shopify.fetch(Shop)
    return render_template('shop/view.html', shop=shop)
