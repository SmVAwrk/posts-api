from marshmallow import Schema, fields, ValidationError

from models import User


def unique_email(data):
    user = User.query.filter(User.email == data).first()
    if user:
        raise ValidationError('email already exists')


def unique_username(data):
    user = User.query.filter(User.username == data).first()
    if user:
        raise ValidationError('name already exists')


class UserRegistrationSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=[fields.Length(max=128), unique_email])
    username = fields.String(required=True, validate=[fields.Length(min=3, max=128), unique_username])
    password = fields.String(required=True, validate=[fields.Length(min=4)])

    class Meta:
        ordered = True


class UserInspectSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(dump_only=True)
    username = fields.String(dump_only=True)


class CommentSubSchema(Schema):
    id = fields.Int(dump_only=True)
    author_id = fields.Int(dump_only=True)
    post_id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[fields.Length(max=255), ])
    content = fields.Str(required=True)
    publication_datetime = fields.DateTime('%d-%m-%Y %H:%M:%S', dump_only=True)

    class Meta:
        ordered = True


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    author_id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[fields.Length(max=255), ])
    content = fields.Str(required=True)
    publication_datetime = fields.DateTime('%d-%m-%Y %H:%M:%S', dump_only=True)
    comments = fields.Nested(CommentSubSchema, many=True, dump_only=True)

    class Meta:
        ordered = True


user_reg_schema = UserRegistrationSchema()
user_ins_schema = UserInspectSchema()

posts_list_schema = PostSchema(many=True)
post_create_schema = PostSchema(only=('title', 'content'))
post_patch_schema = PostSchema(partial=('title', 'content'))
post_detail_schema = PostSchema(exclude=('comments', ))

comment_create_schema = CommentSubSchema()
comment_patch_schema = CommentSubSchema(partial=('title', 'content'))

