from flask import Blueprint, jsonify, request, g, url_for
from flask_restful import Api, Resource

from .mixins import DataHandlerMixin
from flask_app import db, pagination
from flask_app.models import Post, User, Comment
from flask_app.serializers import (
    posts_list_schema, user_reg_schema,
    post_create_schema, post_patch_schema,
    comment_create_schema, comment_patch_schema
)
from flask_app.views import auth

api_bp = Blueprint(name='api', import_name=__name__)
api = Api(api_bp)


@api_bp.route('/')
def api_root():
    """Корень API."""
    return jsonify(
        {
            'registration': url_for('api.registration'),
            'posts': url_for('api.posts')
        }
    )


class UserRegistration(DataHandlerMixin, Resource):
    """Представление для регистрации пользователей."""

    def post(self):
        """
        Метод обработки POST-запроса, реализует создание пользователя.
        """
        if 'Authorization' in request.headers:
            return {'message': 'access denied'}, 400
        json_data = request.get_json()
        data, status = self._request_data_handler(json_data, user_reg_schema)
        if status:
            return data, status

        user = User(
            email=data['email'],
            username=data['username']
        )
        user.hash_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'user': user_reg_schema.dump(user)}, 201


class PostsListView(DataHandlerMixin, Resource):
    """Представление для просмотра и создания постов."""

    def get(self):
        """
        Метод обработки GET-запроса, возвращает список постов с комментариями к ним.
        """
        posts = Post.query.order_by(Post.publication_datetime.desc()).all()
        if not posts:
            return {'message': 'There is no posts'}
        return pagination.paginate(posts, posts_list_schema, True)

    @auth.login_required
    def post(self):
        """
        Метод обработки POST-запроса, реализует создание поста.
        Доступно только авторизованным пользователям.
        """
        json_data = request.get_json()
        data, status = self._request_data_handler(json_data, post_create_schema)
        if status:
            return data, status

        post = Post(
            author_id=g.user.id,
            title=data['title'],
            content=data['content']
        )
        db.session.add(post)
        db.session.commit()
        return post_create_schema.dump(post), 201


class PostEditView(DataHandlerMixin, Resource):
    """Представление для редактирования и удаления постов."""

    @auth.login_required
    def put(self, id):
        """
        Метод обработки PUT-запроса, реализует изменение поста.
        Права доступа имеет только автор поста.
        """
        post = Post.query.filter(Post.id == id).first()
        not_found_or_not_owner = self._check_data('post', g.user, post=post)
        if not_found_or_not_owner:
            return not_found_or_not_owner[0], not_found_or_not_owner[1]

        json_data = request.get_json()
        data, status = self._request_data_handler(json_data, post_create_schema)
        if status:
            return data, status

        post.title = data['title']
        post.content = data['content']
        db.session.add(post)
        db.session.commit()
        return post_create_schema.dump(post)

    @auth.login_required
    def patch(self, id):
        """
        Метод обработки PATCH-запроса, реализует частичное изменение поста.
        Права доступа имеет только автор поста.
        """
        post = Post.query.filter(Post.id == id).first()
        not_found_or_not_owner = self._check_data('post', g.user, post=post)
        if not_found_or_not_owner:
            return not_found_or_not_owner[0], not_found_or_not_owner[1]

        json_data = request.get_json()
        data, status = self._request_data_handler(json_data, post_patch_schema)
        if status:
            return data, status

        for key in data:
            setattr(post, key, data[key])
        db.session.add(post)
        db.session.commit()
        return post_create_schema.dump(post)

    @auth.login_required
    def delete(self, id):
        """
        Метод обработки DELETE-запроса, реализует удаление поста.
        Права доступа имеет только автор поста.
        """
        post = Post.query.filter(Post.id == id).first()
        not_found_or_not_owner = self._check_data('post', g.user, post=post)
        if not_found_or_not_owner:
            return not_found_or_not_owner[0], not_found_or_not_owner[1]
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Post deleted'}, 204


class CommentsCreateView(DataHandlerMixin, Resource):
    """Представление для создания комментариев к постам."""

    @auth.login_required
    def post(self, post_id):
        """
        Метод обработки POST-запроса, реализует создание комментария к посту.
        Доступно только авторизованным пользователям.
        """
        post = Post.query.filter(Post.id == post_id).first()
        not_found_or_not_owner = self._check_data(post=post)
        if not_found_or_not_owner:
            return not_found_or_not_owner[0], not_found_or_not_owner[1]

        json_data = request.get_json()
        data, status = self._request_data_handler(json_data, comment_create_schema)
        if status:
            return data, status

        comment = Comment(
            post_id=post_id,
            author_id=g.user.id,
            title=data['title'],
            content=data['content']
        )
        db.session.add(comment)
        db.session.commit()
        return comment_create_schema.dump(comment), 201


class CommentEditView(DataHandlerMixin, Resource):
    """Представление для редактирования и удаления комментариев к постам."""

    @auth.login_required
    def put(self, post_id, id):
        """
        Метод обработки PUT-запроса, реализует изменение комментария к посту.
        Права доступа имеет только автор комментария.
        """
        post = Post.query.filter(Post.id == post_id).first()
        not_found = self._check_data(post=post)
        if not_found:
            return not_found[0], not_found[1]
        comment = post.comments.filter(Comment.id == id).first()
        not_found_or_not_owner = self._check_data(user=g.user, permission_key='comment', comment=comment)
        if not_found_or_not_owner:
            return not_found_or_not_owner[0], not_found_or_not_owner[1]

        json_data = request.get_json()
        data, status = self._request_data_handler(json_data, comment_create_schema)
        if status:
            return data, status

        comment.title = data['title']
        comment.content = data['content']
        db.session.add(comment)
        db.session.commit()
        return comment_create_schema.dump(comment)

    @auth.login_required
    def patch(self, post_id, id):
        """
        Метод обработки PATCH-запроса, реализует частичное изменение комментария к посту.
        Права доступа имеет только автор комментария.
        """
        post = Post.query.filter(Post.id == post_id).first()
        not_found = self._check_data(post=post)
        if not_found:
            return not_found[0], not_found[1]
        comment = post.comments.filter(Comment.id == id).first()
        not_found_or_not_owner = self._check_data(user=g.user, permission_key='comment', comment=comment)
        if not_found_or_not_owner:
            return not_found_or_not_owner[0], not_found_or_not_owner[1]

        json_data = request.get_json()
        data, status = self._request_data_handler(json_data, comment_patch_schema)
        if status:
            return data, status

        for key in data:
            setattr(comment, key, data[key])
        db.session.add(comment)
        db.session.commit()
        return comment_create_schema.dump(comment)

    @auth.login_required
    def delete(self, post_id, id):
        """
        Метод обработки DELETE-запроса, реализует удаление комментария к посту.
        Права доступа имеет только автор комментария.
        """
        post = Post.query.filter(Post.id == post_id).first()
        not_found = self._check_data(post=post)
        if not_found:
            return not_found[0], not_found[1]
        comment = post.comments.filter(Comment.id == id).first()
        not_found_or_not_owner = self._check_data(user=g.user, permission_key='comment', comment=comment)
        if not_found_or_not_owner:
            return not_found_or_not_owner[0], not_found_or_not_owner[1]

        db.session.delete(comment)
        db.session.commit()
        return {'message': 'comment deleted'}, 204


api.add_resource(UserRegistration, '/registration', endpoint='registration')
api.add_resource(PostsListView, '/posts', endpoint='posts')
api.add_resource(PostEditView, '/posts/<int:id>')
api.add_resource(CommentsCreateView, '/posts/<int:post_id>/comments')
api.add_resource(CommentEditView, '/posts/<int:post_id>/comments/<int:id>')
