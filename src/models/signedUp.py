from utils.db import db

class SignedUp(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    
    user = db.relationship("User", back_populates="registrations")
    post = db.relationship("Post", back_populates="registrations")


# db.Estudiante.inscripciones = db.relationship("SignedUp", back_populates="user")
# db.Curso.inscripciones = db.relationship("SignedUp", back_populates="post")
