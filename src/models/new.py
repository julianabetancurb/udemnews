from utils.db import db

class New(db.Model):
    id = db.Column(db.Integer, primary_key=True,  unique=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    date = db.Column(db.Date)
    reports = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    user = db.relationship('User')

    def __init__(self, title, description, date, user_id):
        self.title = title
        self.description = description
        self.date = date
        self.user_id = user_id