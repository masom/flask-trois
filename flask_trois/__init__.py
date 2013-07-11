from flask import Flask


app = Flask(__name__)
app.config.from_object('flask_trois.config')
app.secret_key = "NOT SO RANDOM IS IT?"


from flask_trois.blueprints import auth, shop, blogs, webhooks


app.register_blueprint(auth)
app.register_blueprint(shop)
app.register_blueprint(blogs)
app.register_blueprint(webhooks)
