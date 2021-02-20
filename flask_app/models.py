import datetime

from app import db
from passlib.apps import custom_app_context as password_hasher


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return self.username

    def hash_password(self, password):
        self.password = password_hasher.encrypt(password)

    def verify_password(self, password):
        return password_hasher.verify(password, self.password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_datetime = db.Column(db.DateTime, default=datetime.datetime.now())
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return 'Post: ' + self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_datetime = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return 'Comment: ' + self.title
