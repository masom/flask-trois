from flask import Blueprint, render_template, g
from shopify_trois.models import Store

store = Blueprint(
    'store',
    __name__,
    template_folder='templates/stores',
    url_prefix='/store'
)


@store.route('/')
def view():
    store = g.shopify.view(Store)
    return render_template('index', store=store)
