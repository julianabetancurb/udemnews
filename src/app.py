from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from routes.posts import post
from routes.auth import auth
from routes.profile import profile
from routes.news import new
from utils.db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/udmnews'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'ClaveUltraSecreta'

db.init_app(app)
# migrate = Migrate(app, db)

app.register_blueprint(auth)

app.register_blueprint(post)

app.register_blueprint(profile)

app.register_blueprint(new)

app.add_url_rule('/', endpoint='index')


