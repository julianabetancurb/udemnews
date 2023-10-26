from utils.db import db
#from sqlalchemy.sql import func

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500))
    img = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    user = db.relationship('User', backref='posts')

    def __init__(self, title, description, img, user_id):
        self.title = title
        self.description = description
        self.img = img
        self.user_id = user_id