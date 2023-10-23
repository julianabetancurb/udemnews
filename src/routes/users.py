from flask import Blueprint, render_template
from utils.db import db

user = Blueprint('users', __name__) #Blueprint del usuario

# @user.route('/')
# def home():
#     return render_template('index.html')


# @user.route('/users', methods=['GET'])
# def users():
#     return render_template('usuarios.html')