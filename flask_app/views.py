from flask import jsonify, request, g
from flask_restful import Resource, abort
from flask_httpauth import HTTPBasicAuth
from marshmallow import ValidationError

from app import app, api, db
from models import Post, User
from serializers import posts_schema, user_reg_schema, user_ins_schema

auth = HTTPBasicAuth()


@app.route('/')
@auth.login_required
def index():
    return jsonify({
        'page_name': 'Index',
    })


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter(User.username == username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@auth.error_handler
def auth_error(status):
    return jsonify({'message': 'Access Denied'}), status


class UserRegistration(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = user_reg_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        user = User(
            email=data['email'],
            username=data['username']
        )
        user.hash_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'successful registration', 'user': user_ins_schema.dump(user)}


api.add_resource(UserRegistration, '/registration')


class PostsListView(Resource):
    def get(self):
        posts = Post.query.order_by(Post.publication_datetime).all()
        if not posts:
            return {'message': 'there is no posts'}
        return {'posts': posts_schema.dump(posts)}


api.add_resource(PostsListView, '/posts')
