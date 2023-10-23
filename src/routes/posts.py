from flask import Blueprint

post = Blueprint('posts', __name__) #Blueprint de la convocatoria

@post.route('/index')
def hello():
    return "<h1>holaa</h1>"



