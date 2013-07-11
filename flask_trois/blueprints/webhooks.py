from flask import Blueprint, request, render_template, g, redirect, url_for
from shopify_trois.models import Webhook

webhooks = Blueprint(
    'webhook',
    __name__,
    template_folder='templates/webhooks',
    url_prefix='/webhooks'
)


@webhooks.route('/')
def index():
    webhooks = g.shopify.index(Webhook)
    return render_template('index.html', webhooks=webhooks)


@webhooks.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':
        webhook = Webhook(**request.form)
        g.shopify.add(webhook)
        return redirect(url_for('view', id=webhook.id))

    return render_template('create.html')


@webhooks.route('/view/<int:id>')
def view(id):
    webhook = g.shopify.fetch(Webhook, id)
    return render_template('view.html', webhook=webhook)


@webhooks.route('/delete/<int:id>')
def delete(id):
    webhook = Webhook(id=id)
    g.shopify.delete(webhook)
    return redirect(url_for('index'))


@webhooks.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    webhook = Webhook(id=id)

    if request.method == 'POST':
        webhook.update(request.form)
        g.shopify.update(webhook)
        return redirect(url_for('view', id=webhook.id))
    return render_template('update.html', webhook=webhook)
