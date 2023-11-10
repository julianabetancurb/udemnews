from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from routes.auth import login_required
from utils.db import db
from models.new import New

new = Blueprint('new', __name__, url_prefix='/new')

@new.route('/news', methods=['GET'])
def index_new():
    news = db.session.query(New).all()
    return render_template('new/index_new.html', news=news)

@new.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        user_id = g.user.id
        error = None


        if not title or not description:
            error = "Hay datos incompletos"

        if error is not None:
            flash(error)

        else:
            new = New(title, description, date, user_id)
            db.session.add(new)
            db.session.commit()
        
            return redirect(url_for('new.index_new'))
        
    return render_template('new/create.html')

def get_new(id, check_author=True):
    new = New.query.filter_by(id=id).first()

    if new is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and new.user_id != g.user.id:
        abort(403)

    return new

@new.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    new = get_new(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        error = None

        if not title or not description:
            error = 'Faltan campos por completar'
        
        if error:
            flash(error)
        
        else:
            new.title = title
            new.description = description
            new.date = date
            db.session.commit()
            return redirect(url_for('new.index'))
        
    return render_template('new/update.html', new=new)


@new.route('/<int:id>/details', methods=['GET'])
@login_required
def details(id):
    new = get_new(id)
    if new is None:
        abort(404)
    return render_template('new/details.html', new=new)



@new.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    new = get_new(id)

    if new:
        db.session.delete(new)
        db.session.commit()
        return redirect(url_for('new.index_new'))
