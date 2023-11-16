from flask import Flask
from routes.posts import post
from routes.auth import auth
from routes.profile import profile
from routes.news import new
from utils.db import db


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:f12eDGGd2G-b6Db4b2AefHGgFcD6b6Ag@roundhouse.proxy.rlwy.net:12015/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'ClaveUltraSecreta'

db.init_app(app)
 

app.register_blueprint(auth)

app.register_blueprint(post)

app.register_blueprint(profile)

app.register_blueprint(new)

app.add_url_rule('/', endpoint='index')


