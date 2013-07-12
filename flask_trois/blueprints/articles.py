from flask import Blueprint, request, render_template, g, redirect, url_for

from flask_trois.helpers import setup_shopify_adapter

from shopify_trois.models import Article


articles = Blueprint(
    'articles',
    __name__,
    url_prefix='/articles'
)


@articles.route('/create', methods=['GET', 'POST'])
@setup_shopify_adapter
def create(blog_id):

    if request.method == 'POST':
        article = Article(**request.form.to_dict(flat=True))
        article.blog_id = blog_id

        g.shopify.add(article)

        return redirect(url_for('.view', id=article.id))

    return render_template('articles/create.html')


@articles.route('/view/<int:blog_id>/<int:id>')
@setup_shopify_adapter
def view(blog_id, id):
    article = g.shopify.fetch(Article, primary_key=id, parent_id=blog_id)

    return render_template('articles/view.html', article=article)
