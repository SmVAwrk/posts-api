from flask import jsonify, request, g
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from marshmallow import ValidationError

from app import app, api, db
from models import Post, User, Comment
from serializers import posts_list_schema, user_reg_schema, user_ins_schema, post_create_schema, post_detail_schema, \
    post_patch_schema, comment_create_schema, comment_patch_schema

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
        return {'message': 'Successful registration', 'user': user_ins_schema.dump(user)}


api.add_resource(UserRegistration, '/registration')


class PostsListView(Resource):
    def get(self):
        posts = Post.query.order_by(Post.publication_datetime.desc()).all()
        if not posts:
            return {'message': 'There is no posts'}
        return {'posts': posts_list_schema.dump(posts)}

    @auth.login_required
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = post_create_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        post = Post(
            author_id=g.user.id,
            title=data['title'],
            content=data['content']
        )
        db.session.add(post)
        db.session.commit()
        return {'message': 'Successful create', 'post': post_detail_schema.dump(post)}


api.add_resource(PostsListView, '/posts')


class PostEditView(Resource):
    @auth.login_required
    def put(self, id):
        post = Post.query.filter(Post.id == id).first()
        if not post:
            return {'message': 'Post not found'}, 404
        current_user_username = auth.username()
        user = User.query.filter(User.username == current_user_username).first()
        if not post.author_id == user.id:
            return {'message': 'You cannot edit this post'}, 403

        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = post_create_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        post.title = data['title']
        post.content = data['content']
        db.session.add(post)
        db.session.commit()
        return post_detail_schema.dump(post)

    @auth.login_required
    def patch(self, id):
        post = Post.query.filter(Post.id == id).first()
        if not post:
            return {'message': 'Post not found'}, 404
        current_user_username = auth.username()
        user = User.query.filter(User.username == current_user_username).first()
        if not post.author_id == user.id:
            return {'message': 'You cannot edit this post'}, 403

        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = post_patch_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        for key in data:
            setattr(post, key, data[key])
        db.session.add(post)
        db.session.commit()
        return post_detail_schema.dump(post)

    @auth.login_required
    def delete(self, id):
        post = Post.query.filter(Post.id == id).first()
        if not post:
            return {'message': 'Post not found'}, 404
        current_user_username = auth.username()
        user = User.query.filter(User.username == current_user_username).first()
        if not post.author_id == user.id:
            return {'message': 'You cannot delete this post'}, 403
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Post deleted'}, 204

    # def _check_data(self, id):
    #     post = Post.query.filter(Post.id == id).first()
    #     if not post:
    #         return {'message': 'Post not found'}, 404
    #     current_user_username = auth.username()
    #     user = User.query.filter(User.username == current_user_username).first()
    #     if not post.author_id == user.id:
    #         return {'message': 'You cannot edit this post'}, 403


api.add_resource(PostEditView, '/posts/<int:id>')


class CommentsCreateView(Resource):

    @auth.login_required
    def post(self, post_id):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = comment_create_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        comment = Comment(
            post_id=post_id,
            author_id=g.user.id,
            title=data['title'],
            content=data['content']
        )
        db.session.add(comment)
        db.session.commit()
        return comment_create_schema.dump(comment)


api.add_resource(CommentsCreateView, '/posts/<int:post_id>/comments')


class CommentsEditView(Resource):

    @auth.login_required
    def put(self, post_id, id):
        post = Post.query.filter(Post.id == post_id).first()
        if not post:
            return {'message': 'Post not found'}, 404
        comment = Comment.query.filter(Comment.id == id).first()
        if not comment:
            return {'message': 'Comment not found'}, 404
        current_user_username = auth.username()
        user = User.query.filter(User.username == current_user_username).first()
        if not comment.author_id == user.id:
            return {'message': 'You cannot edit this comment'}, 403

        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = comment_create_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        comment.title = data['title']
        comment.content = data['content']
        db.session.add(comment)
        db.session.commit()
        return comment_create_schema.dump(comment)

    @auth.login_required
    def patch(self, post_id, id):
        post = Post.query.filter(Post.id == post_id).first()
        if not post:
            return {'message': 'Post not found'}, 404
        comment = Comment.query.filter(Comment.id == id).first()
        if not comment:
            return {'message': 'Comment not found'}, 404
        current_user_username = auth.username()
        user = User.query.filter(User.username == current_user_username).first()
        if not comment.author_id == user.id:
            return {'message': 'You cannot edit this comment'}, 403

        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = comment_patch_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        for key in data:
            setattr(comment, key, data[key])
        db.session.add(comment)
        db.session.commit()
        return comment_create_schema.dump(comment)

    @auth.login_required
    def delete(self, post_id, id):
        post = Post.query.filter(Post.id == post_id).first()
        if not post:
            return {'message': 'Post not found'}, 404
        comment = Comment.query.filter(Comment.id == id).first()
        if not comment:
            return {'message': 'Comment not found'}, 404
        current_user_username = auth.username()
        user = User.query.filter(User.username == current_user_username).first()
        if not comment.author_id == user.id:
            return {'message': 'You cannot delete this comment'}, 403
        db.session.delete(comment)
        db.session.commit()
        return {'message': 'Comment deleted'}, 204


api.add_resource(CommentsEditView, '/posts/<int:post_id>/comments/<int:id>')
