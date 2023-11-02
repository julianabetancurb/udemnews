import functools
import re

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
        recovery_question = request.form.get('selected_question')
        recovery_answer = request.form['recovery_answer']
        user_exist = User.query.filter_by(email=email).first()
        valid_email = is_valid_email(email)
        valid_password = is_valid_password(password)
        error = None

        if not username:
            error = 'Se requiere un nombre de ususario.'
        elif not password:
            error = 'Se requiere una contraseña.'
        elif user_exist:
            error = 'Ya existe una cuenta vinculada con este correo.'
        elif valid_email is False:
            error = 'El email no es valido.'
        elif valid_password is False:
            error = 'La contraseña no es valida.'
        elif bool(re.match(r'^\d*$', username)):
            error = 'Este nombre no es valido.'
        elif not recovery_question: 
            error = 'Selecciona una pregunta'
        elif not recovery_answer: 
            error = 'No olvides tu respuesta'

        if error is None:
            try:
                new_user = User(username, email, generate_password_hash(password), recovery_question, recovery_answer)
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
            error = 'Email incorrecto.'
        elif not check_password_hash(user.password_hash, password):
            error = 'Contraseña incorrecta.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
    
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

@auth.route('/recovery_stage_1', methods=['GET', 'POST'])
def recovery_stage_1():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not email:
            flash('Por favor, ingrese su dirección de correo electrónico.')
        elif not user:
            flash('No se encontró un usuario con esta dirección de correo electrónico.')
        else:
             return redirect(url_for('auth.recovery_stage_2', user_id=user.id))

    return render_template('auth/recovery_password_stage1.html')

@auth.route('/recovery_stage_2/<int:user_id>', methods=['GET', 'POST'])
def recovery_stage_2(user_id):

    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        recovery_answer = request.form.get('recovery_answer')
        error = None

        if user is None:
            error = 'No se encontró un usuario con ese correo electrónico'

        if user and recovery_answer.lower() != user.recovery_answer.lower():
            error = 'Respuesta incorrecta'

        if error is None:
            return redirect(url_for('auth.change_password', user_id=user.id))

        flash(error)

    return render_template('auth/recovery_password_stage2.html', user=user)


@auth.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
def change_password(user_id):
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        password  = request.form['new_password']
        password_check = request.form['confirm_password']
        error = None
        valid_password = is_valid_password(password)

        if not password or not password_check:
            error = 'Faltan campos por completar.'

        if password_check != password_check:
            error = 'Las contraseñas no coinciden.'

        if valid_password is False:
            error = 'Contraseña no valido.'

        if error:
            flash(error)

        else:
            user.password_hash = generate_password_hash(password)
            db.session.commit()
            return redirect(url_for('auth.login'))
    
    return render_template('auth/change_password.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(email_regex, email):
        return True
    else:
        return False
    
def is_valid_password(password):
    min_length = 8 
    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_special = any(char in "!@#$%^&*()_+-=[]{}|;:'<>,.?/" for char in password)

    if len(password) >= min_length and has_digit and has_upper and has_special:
        return True
    else:
        return False

