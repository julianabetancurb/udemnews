from utils.db import db, signedup

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True,  unique=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    img = db.Column(db.String(300))
    date = db.Column(db.Date)
    deadline = db.Column(db.Date)
    faculty = db.Column(db.String(25))
    reports = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    users = db.relationship('User', secondary='signedup', back_populates='posts_registered')
    user = db.relationship('User', backref='posts')
    

    def __init__(self, title, description, img, date, deadline, faculty, user_id, reports=0):
        self.title = title
        self.description = description
        self.img = img
        self.date = date
        self.deadline = deadline
        self.faculty = faculty
        self.reports = reports
        self.user_id = user_id