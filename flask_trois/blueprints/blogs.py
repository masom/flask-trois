from flask import Blueprint, request, render_template, g, redirect, url_for

from flask_trois.helpers import setup_shopify_adapter

from shopify_trois.models import Blog, Article


blogs = Blueprint(
    'blogs',
    __name__,
    url_prefix='/blogs'
)


@blogs.route('/')
@setup_shopify_adapter
def index():
    blogs = g.shopify.index(Blog)
    return render_template('blogs/index.html', blogs=blogs)


@blogs.route('/create', methods=['GET', 'POST'])
@setup_shopify_adapter
def create():

    if request.method == 'POST':
        blog = Blog(**request.form)
        g.shopify.add(blog)
        return redirect(url_for('.view', id=blog.id))

    return render_template('blogs/create.html')


@blogs.route('/view/<int:id>')
@setup_shopify_adapter
def view(id):
    blog = g.shopify.fetch(Blog, id)

    articles = g.shopify.index(Article, parent_id=blog.id)
    return render_template('blogs/view.html', blog=blog, articles=articles)
