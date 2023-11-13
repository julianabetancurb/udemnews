from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

signedup = db.Table('signedup',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)