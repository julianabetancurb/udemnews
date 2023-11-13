from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import datetime
from werkzeug.exceptions import abort
from routes.auth import login_required
from utils.db import db
from models.post import Post
from models.user import User
from models.signed_up import SignedUp
import os

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
        date = datetime.now()
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
        
            return redirect(url_for('post.index_post'))
        
    return render_template('post/create.html')

#Funcion para obtener una convocatoria
def get_post(id):
    post = Post.query.filter_by(id=id).first()

    if post is None:
        abort(404, f"Post id {id} no existe.")


    return post

#Funcion para obtener un usuario
def get_user(id):
    user = User.query.filter_by(id=id).first()

    if user is None:
        abort(404, f"Usuario id {id} no existe.")
    
    return user

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
            return redirect(url_for('post.index_post'))
        
    return render_template('post/update.html', post=post)


@post.route('/<int:id>/details', methods=['GET'])
@login_required
def details(id):
    post = get_post(id)
    user_id = g.user.id
    record = SignedUp.query.filter_by(user_id=user_id, post_id=id).first()
    if post is None:
        abort(404)
    return render_template('post/details.html', post=post, record=record)



@post.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    post = get_post(id)

    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.index_post'))
    
@post.route('/<int:id>/get_registers', methods=['GET'])
@login_required
def get_registers(id):
    post = get_post(id)

    if post:
        records = SignedUp.query.filter_by(post_id=post.id).all()
        registered_users = list(map(get_user, [record.user_id for record in records]))

        return render_template('post/get_registers.html', registered_users=registered_users)
    
@post.route('/<int:id>/register_user', methods=['GET','POST'])
@login_required
def register_user(id):
    post = get_post(id)
    user_id = g.user.id
    error = None

    record = SignedUp.query.filter_by(user_id=user_id).first()

    if record:
        error = 'Ya estabas registrado en esta convocatoria'
        flash(error)
        return redirect(url_for('post.details', id=id))

    else:
        new_record = SignedUp(user_id, post.id)
        db.session.add(new_record)
        db.session.commit()
        flash('Te inscribiste con exito')
        return redirect(url_for('post.index_post'))

@post.route('/<int:id>/delete_register', methods=['POST'])
@login_required
def delete_register(id):

    user_id = g.user.id
    record = SignedUp.query.filter_by(user_id=user_id, post_id=id).first()

    if record:
        db.session.delete(record)
        db.session.commit()
        flash(' convocatoria')
        return redirect(url_for('post.index_post'))




