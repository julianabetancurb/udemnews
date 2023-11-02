from utils.db import db
from models.user import User
from routes.auth import is_valid_email

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/profile', methods=['GET'])
def profile_index():
    user = User.query.filter_by(id=g.user.id).first()
    return render_template('profile/profile.html', user=user)

@profile.route('/update_profile', methods=['GET','POST'])
def update():
    user = User.query.filter_by(id=g.user.id).first()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        error = None
        valid_email = is_valid_email(email)

        if not username or not email:
            error = 'Faltan campos por completar'

        if valid_email is False:
            error = 'Correro no valido'

        if error:
            flash(error)

        else:
            user.username = username
            user.email = email
            db.session.commit()
            return redirect(url_for('profile.profile_index'))

    return render_template('profile/update.html', user=user)