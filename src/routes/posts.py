from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from routes.auth import login_required
from utils.db import db
from models.post import Post

post = Blueprint('post', __name__)

@post.route('/')
def index():
    return render_template('base.html')

@post.route('/posts')
def index_post():
    posts = db.session.query(Post).all()
    return render_template('post/index_post.html', posts=posts)

@post.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        img = request.form['img']
        date = request.form['date']
        deadline = request.form['deadline']
        faculty = request.form.get('selected_question')
        user_id = g.user.id
        error = None


        if not title or not description:
            error = "Hay datos incompletos"

        if error is not None:
            flash(error)

        else:
            new_post = Post(title, description, img, date, deadline, faculty, user_id)
            db.session.add(new_post)
            db.session.commit()
        
            return redirect(url_for('post.index'))
        
    return render_template('post/create.html')

def get_post(id):
    post = Post.query.filter_by(id=id).first()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")


    return post

@post.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        img = request.form['img']
        error = None

        if not title or not description:
            error = 'Faltan campos por completar'
        
        if error:
            flash(error)
        
        else:
            post.title = title
            post.description = description
            post.img = img
            db.session.commit()
            return redirect(url_for('post.index'))
        
    return render_template('post/update.html', post=post)


@post.route('/<int:id>/details', methods=['GET'])
@login_required
def details(id):
    post = get_post(id)
    if post is None:
        abort(404)
    return render_template('post/details.html', post=post)



@post.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    post = get_post(id)

    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.index'))

