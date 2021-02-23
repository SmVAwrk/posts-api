import datetime


from . import db
from passlib.apps import custom_app_context as password_hasher


class User(db.Model):
    """Модель пользователей"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    comments = db.relationship('Comment', backref='user', cascade='all, delete',
                               passive_deletes=True, lazy='dynamic')

    def __repr__(self):
        return f'<User id: {self.id}, username: {self.username}>'

    def hash_password(self, password):
        """Метод хеширования пароля"""
        self.password = password_hasher.hash(password)

    def verify_password(self, password):
        """Метод проверки пароля"""
        return password_hasher.verify(password, self.password)


class Post(db.Model):
    """Модель постов"""
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_datetime = db.Column(db.DateTime, default=datetime.datetime.now())

    comments = db.relationship('Comment', backref='post', cascade='all, delete',
                               passive_deletes=True, lazy='dynamic', order_by="Comment.id")

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}>'


class Comment(db.Model):
    """Модель комментариев"""
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_datetime = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f'<Comment id: {self.id}, title: {self.title}>'
