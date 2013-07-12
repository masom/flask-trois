from flask import Blueprint, request, render_template, g, redirect, url_for


from flask_trois.helpers import setup_shopify_adapter

from shopify_trois.models import Webhook


webhooks = Blueprint(
    'webhook',
    __name__,
    template_folder='templates/webhooks',
    url_prefix='/webhooks'
)


@webhooks.route('/')
@setup_shopify_adapter
def index():
    webhooks = g.shopify.index(Webhook)
    return render_template('webhooks/index.html', webhooks=webhooks)


@webhooks.route('/create', methods=['GET', 'POST'])
@setup_shopify_adapter
def create():
    if request.method == 'POST':

        webhook = Webhook(**request.form.to_dict(flat=True))
        try:
            g.shopify.add(webhook)
        except Exception as e:
            print(e.args[0].text)
        return redirect(url_for('.index'))

    return render_template('webhooks/create.html')


@webhooks.route('/delete/<int:id>')
@setup_shopify_adapter
def delete(id):
    webhook = Webhook(id=id)
    g.shopify.delete(webhook)
    return redirect(url_for('.index'))


@webhooks.route('/update/<int:id>', methods=['GET', 'POST'])
@setup_shopify_adapter
def update(id):

    webhook = g.shopify.fetch(Webhook, id)

    if request.method == 'POST':
        webhook.update({'webhook': request.form.to_dict(flat=True)})
        g.shopify.update(webhook)
        return redirect(url_for('.index'))

    return render_template('webhooks/update.html', webhook=webhook)
