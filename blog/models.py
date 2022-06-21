from datetime import datetime
from datetime import timedelta

from sqlalchemy import null
from blog import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(500))
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    stars = db.relationship('Reviews', backref='post', lazy='dynamic')
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Data model for user and password set and check functions adapted from Grinberg, 2017. 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    stars = db.relationship('Reviews', backref='user', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)

    def __repr__(self):
        return '{} ({} at {})'.format(self.body, self.author_id, self.timestamp)

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)

    def __repr__(self):
        return '<Comment {}>'.format(self.stars)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))