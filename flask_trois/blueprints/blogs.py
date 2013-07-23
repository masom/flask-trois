from flask import Blueprint, request, render_template, g, redirect, url_for

from flask_trois.helpers import setup_shopify_adapter

from shopify_trois.models import Blog, Article, BlogMetafield


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


@blogs.route('/<int:id>/metafields')
@setup_shopify_adapter
def metafields(id):
    args = dict(
        blog=g.shopify.fetch(Blog, id),
        metafields=g.shopify.index(BlogMetafield, parent_id=id)
    )

    return render_template('blogs/metafields.html', **args)


@blogs.route('/<int:blog_id>/metafields/create', methods=['GET', 'POST'])
@setup_shopify_adapter
def metafields_add(blog_id):
    if request.method == 'POST':
        metafield = BlogMetafield(**request.form.to_dict(flat=True))
        metafield.blog_id = blog_id

        g.shopify.add(metafield)
        return redirect(url_for('.metafields', id=blog_id))

    return render_template('blogs/metafields_create.html', blog_id=blog_id)


@blogs.route(
    '/<int:blog_id>/metafields/delete/<int:metafield_id>',
    methods=['GET', 'POST']
)
@setup_shopify_adapter
def metafields_delete(blog_id, metafield_id):
    metafield = BlogMetafield(id=metafield_id, blog_id=blog_id)
    g.shopify.delete(metafield)

    return redirect(url_for('.metafields', id=blog_id))
