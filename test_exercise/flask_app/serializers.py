from marshmallow import Schema, fields, ValidationError

from .models import User


def unique_email(data):
    """Проверка наличия пользователя с указанным email`ом"""
    user = User.query.filter(User.email == data).first()
    if user:
        raise ValidationError('email already exists')


def unique_username(data):
    """Проверка наличия пользователя с указанным именем"""
    user = User.query.filter(User.username == data).first()
    if user:
        raise ValidationError('name already exists')


class UserRegistrationSchema(Schema):
    """Сериализатор для обработки данных при регистрации пользователя"""
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=[fields.Length(max=128), unique_email])
    username = fields.String(required=True, validate=[fields.Length(min=3, max=128), unique_username])
    password = fields.String(required=True, load_only=True, validate=[fields.Length(min=4)])

    class Meta:
        ordered = True


class CommentSchema(Schema):
    """Сериализатор для обработки данных при работе с комментариями"""
    id = fields.Int(dump_only=True)
    author_id = fields.Int(dump_only=True)
    post_id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[fields.Length(min=1, max=255), ])
    content = fields.Str(required=True, validate=[fields.Length(min=1), ])
    publication_datetime = fields.DateTime('%d-%m-%Y %H:%M:%S', dump_only=True)

    class Meta:
        ordered = True


class PostSchema(Schema):
    """Сериализатор для обработки данных при работе с постами"""
    id = fields.Int(dump_only=True)
    author_id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[fields.Length(min=1, max=255), ])
    content = fields.Str(required=True, validate=[fields.Length(min=1), ])
    publication_datetime = fields.DateTime('%d-%m-%Y %H:%M:%S', dump_only=True)
    comments = fields.Nested(CommentSchema, many=True, dump_only=True)

    class Meta:
        ordered = True


user_reg_schema = UserRegistrationSchema()

posts_list_schema = PostSchema(many=True)
post_create_schema = PostSchema()
post_patch_schema = PostSchema(partial=('title', 'content'))

comment_create_schema = CommentSchema()
comment_patch_schema = CommentSchema(partial=('title', 'content'))
