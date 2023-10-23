import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from utils.db import db

from models.user import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_exist = User.query.filter_by(email=email).first()
        error = None

        if not username:
            error = 'Se requiere un nombre de ususario.'
        elif not password:
            error = 'Se requiere una contraseña.'
        elif user_exist:
            error = 'Ya existe una cuenta vinculada con este correo'

        if error is None:
            try:
                new_user = User(username, email, generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Username or password incorrect'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('auth.login'))
    
        flash(error)

    return render_template('auth/login.html')

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    
    else:
        g.user = User.query.filter_by(id=user_id).first()

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view