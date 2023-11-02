from utils.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    recovery_question = db.Column(db.String(70), nullable=False)
    recovery_answer = db.Column(db.String(40), nullable=False)

    registrations = db.relationship("SignedUp")

    def __init__(self, username, email, password, recovery_question, recovery_answer):
        self.username = username
        self.email = email
        self.password_hash = password
        self.recovery_question = recovery_question
        self.recovery_answer = recovery_answer
