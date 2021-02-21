import os
from unittest import TestCase

from marshmallow import ValidationError

from flask_app import app, db
from flask_app.serializers import user_reg_schema, post_create_schema, posts_list_schema, post_patch_schema, \
    comment_create_schema, comment_patch_schema
from flask_app.models import User, Post, Comment


class BaseTestCase(TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserRegistrationSerializerTestCase(BaseTestCase):

    def test_load_valid(self):
        expected_data = {
            'email': 'email@test.com',
            'username': 'testuser',
            'password': 'testpass'
        }
        load_data = {
            'email': 'email@test.com',
            'username': 'testuser',
            'password': 'testpass'
        }
        data = user_reg_schema.load(load_data)
        self.assertEqual(expected_data, data)

    def test_load_with_unexpected_field(self):
        load_data = {
            'id': 1,
            'email': 'email@test.com',
            'username': 'testuser',
            'password': 'testpass'
        }
        with self.assertRaises(ValidationError):
            user_reg_schema.load(load_data)

    def test_load_without_req_field(self):
        load_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        with self.assertRaises(ValidationError):
            user_reg_schema.load(load_data)

    def test_load_not_unique_email(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        db.session.add(user)
        db.session.commit()

        load_data = {
            'email': 't@t.com',
            'username': 'testuser',
            'password': 'testpass'
        }
        with self.assertRaises(ValidationError):
            user_reg_schema.load(load_data)

    def test_load_not_unique_username(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        db.session.add(user)
        db.session.commit()

        load_data = {
            'email': 'email@test.com',
            'username': 'user1',
            'password': 'testpass'
        }
        with self.assertRaises(ValidationError):
            user_reg_schema.load(load_data)

    def test_load_not_valid_username(self):
        load_data = {
            'email': 'email@test.com',
            'username': '',
            'password': 'testpass'
        }
        with self.assertRaises(ValidationError):
            user_reg_schema.load(load_data)

    def test_load_not_valid_email(self):
        load_data = {
            'email': '',
            'username': 'testuser',
            'password': 'testpass'
        }
        with self.assertRaises(ValidationError):
            user_reg_schema.load(load_data)

    def test_load_not_valid_password(self):
        load_data = {
            'email': 'email@test.com',
            'username': 'testuser',
            'password': ''
        }
        with self.assertRaises(ValidationError):
            user_reg_schema.load(load_data)

    def test_dump_ok(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        db.session.add(user)
        db.session.commit()

        expected_data = {
            'id': user.id,
            'email': 't@t.com',
            'username': 'user1',
        }
        data = user_reg_schema.dump(user)
        self.assertEqual(expected_data, data)


class PostsListSerializerTestCase(BaseTestCase):

    def test_dump_many_posts(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        db.session.add(user)
        db.session.commit()

        post1 = Post(author_id=user.id, title='Title 1', content='Content 1')
        post2 = Post(author_id=user.id, title='Title 2', content='Content 2')
        db.session.add_all([post1, post2])
        db.session.commit()

        expected_data = [
            {
                'id': post1.id,
                'author_id': user.id,
                'title': 'Title 1',
                'content': 'Content 1',
                'publication_datetime': post1.publication_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                'comments': []
            },
            {
                'id': post2.id,
                'author_id': user.id,
                'title': 'Title 2',
                'content': 'Content 2',
                'publication_datetime': post2.publication_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                'comments': []
            }
        ]

        data = posts_list_schema.dump([post1, post2])
        self.assertEqual(expected_data, data)


class PostCreateUpdateSerializerTestCase(BaseTestCase):

    def test_load_valid(self):
        load_data = {
            'title': 'Title',
            'content': 'Content'
        }
        expected_data = {
            'title': 'Title',
            'content': 'Content'
        }
        data = post_create_schema.load(load_data)
        self.assertEqual(expected_data, data)

    def test_load_with_unexpected_field(self):
        load_data = {
            'id': 1,
            'title': 'Title',
            'content': 'Content'
        }
        with self.assertRaises(ValidationError):
            post_create_schema.load(load_data)

    def test_load_without_req_field(self):
        load_data = {
            'title': 'Title'
        }
        with self.assertRaises(ValidationError):
            post_create_schema.load(load_data)

    def test_load_not_valid_title(self):
        load_data = {
            'title': '',
            'content': 'Content'
        }
        with self.assertRaises(ValidationError):
            post_create_schema.load(load_data)

    def test_load_not_valid_content(self):
        load_data = {
            'title': 'Title',
            'content': ''
        }
        with self.assertRaises(ValidationError):
            post_create_schema.load(load_data)

    def test_dump_post(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        db.session.add(user)
        db.session.commit()

        post1 = Post(author_id=user.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        comment1 = Comment(author_id=user.id,
                           post_id=post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        expected_data = {
            'id': post1.id,
            'author_id': user.id,
            'title': 'Title 1',
            'content': 'Content 1',
            'publication_datetime': post1.publication_datetime.strftime('%d-%m-%Y %H:%M:%S'),
            'comments': [
                {
                    'id': comment1.id,
                    'author_id': user.id,
                    'post_id': post1.id,
                    'title': 'Comment Title 1',
                    'content': 'Comment Content 1',
                    'publication_datetime': comment1.publication_datetime.strftime('%d-%m-%Y %H:%M:%S')
                }
            ]

        }
        data = post_create_schema.dump(post1)
        self.assertEqual(expected_data, data)


class PostPartialUpdateSerializerTestCase(BaseTestCase):

    def test_load_valid(self):
        load_data = {
            'title': 'Title'
        }
        expected_data = {
            'title': 'Title'
        }
        data = post_patch_schema.load(load_data)
        self.assertEqual(expected_data, data)

    def test_load_with_unexpected_field(self):
        load_data = {
            'id': 1,
            'title': 'Title'
        }
        with self.assertRaises(ValidationError):
            post_patch_schema.load(load_data)

    def test_load_not_valid_title(self):
        load_data = {
            'title': ''
        }
        with self.assertRaises(ValidationError):
            post_patch_schema.load(load_data)

    def test_load_not_valid_content(self):
        load_data = {
            'content': ''
        }
        with self.assertRaises(ValidationError):
            post_patch_schema.load(load_data)


class CommentCreateUpdateSerializerTestCase(BaseTestCase):

    def test_load_valid(self):
        load_data = {
            'title': 'Comment title',
            'content': 'Comment content'
        }
        expected_data = {
            'title': 'Comment title',
            'content': 'Comment content'
        }
        data = comment_create_schema.load(load_data)
        self.assertEqual(expected_data, data)

    def test_load_with_unexpected_field(self):
        load_data = {
            'id': 1,
            'title': 'Comment title',
            'content': 'Comment content'
        }
        with self.assertRaises(ValidationError):
            comment_create_schema.load(load_data)

    def test_load_without_req_field(self):
        load_data = {
            'title': 'Comment title'
        }
        with self.assertRaises(ValidationError):
            comment_create_schema.load(load_data)

    def test_load_not_valid_title(self):
        load_data = {
            'title': '',
            'content': 'Comment content'
        }
        with self.assertRaises(ValidationError):
            comment_create_schema.load(load_data)

    def test_load_not_valid_content(self):
        load_data = {
            'title': 'Comment title',
            'content': ''
        }
        with self.assertRaises(ValidationError):
            comment_create_schema.load(load_data)

    def test_dump_comment(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        db.session.add(user)
        db.session.commit()

        post1 = Post(author_id=user.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        comment1 = Comment(author_id=user.id,
                           post_id=post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        expected_data = {
            'id': comment1.id,
            'author_id': user.id,
            'post_id': post1.id,
            'title': 'Comment Title 1',
            'content': 'Comment Content 1',
            'publication_datetime': comment1.publication_datetime.strftime('%d-%m-%Y %H:%M:%S')
        }

        data = comment_create_schema.dump(comment1)
        self.assertEqual(expected_data, data)


class CommentPartialUpdateSerializerTestCase(BaseTestCase):

    def test_load_valid(self):
        load_data = {
            'title': 'Comment title'
        }
        expected_data = {
            'title': 'Comment title'
        }
        data = comment_patch_schema.load(load_data)
        self.assertEqual(expected_data, data)

    def test_load_with_unexpected_field(self):
        load_data = {
            'id': 1,
            'title': 'Comment title'
        }
        with self.assertRaises(ValidationError):
            comment_patch_schema.load(load_data)

    def test_load_not_valid_title(self):
        load_data = {
            'title': ''
        }
        with self.assertRaises(ValidationError):
            comment_patch_schema.load(load_data)

    def test_load_not_valid_content(self):
        load_data = {
            'content': ''
        }
        with self.assertRaises(ValidationError):
            comment_patch_schema.load(load_data)
