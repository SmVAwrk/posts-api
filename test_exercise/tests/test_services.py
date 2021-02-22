import os
from unittest import TestCase
from unittest.mock import Mock

from marshmallow import ValidationError

from flask_app import db, app
from flask_app.api.mixins import DataHandlerMixin
from flask_app.models import User, Post, Comment
from flask_app.serializers import post_create_schema


def raise_validation_error(_data):
    raise ValidationError(message='validation error')


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


class RequestDataHandlerTestCase(BaseTestCase):

    def test_normal_data(self):
        data = {
            'title': 'Title 1',
            'content': 'Content 1'
        }
        serializer = Mock()
        serializer.load = Mock(return_value=data)

        handled_data, _ = DataHandlerMixin._request_data_handler(data, serializer)
        self.assertEqual(data, handled_data)
        self.assertIsNone(_)

    def test_empty_data(self):
        data = None
        serializer = Mock()
        serializer.load = Mock(return_value=data)

        message, status = DataHandlerMixin._request_data_handler(data, serializer)
        self.assertEqual({'message': 'no input data provided'}, message)
        self.assertEqual(400, status)

    def test_not_valid_data(self):
        data = {
            'title': 'Title 1'
        }
        serializer = Mock()
        serializer.load = raise_validation_error

        message, status = DataHandlerMixin._request_data_handler(data, serializer)
        self.assertEqual(400, status)
        self.assertEqual(['validation error'], message)


class CheckDataTestCase(BaseTestCase):

    def test_existing_single_data_without_owner_check(self):
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

        not_found = DataHandlerMixin._check_data(post=post1)
        self.assertIsNone(not_found)

    def test_existing_single_data_with_owner_check_from_owner(self):
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

        not_found_or_not_owner = DataHandlerMixin._check_data('post', user, post=post1)
        self.assertIsNone(not_found_or_not_owner)

    def test_existing_single_data_with_owner_check_from_not_owner(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        user2 = User(
            email='t@t2.com',
            username='user2'
        )
        user2.hash_password('1q2w3e')
        db.session.add_all([user, user2])
        db.session.commit()

        post1 = Post(author_id=user2.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        not_found_or_not_owner = DataHandlerMixin._check_data('post', user, post=post1)
        self.assertEqual({'message': 'you cannot edit this post'}, not_found_or_not_owner[0])
        self.assertEqual(403, not_found_or_not_owner[1])

    def test_not_existing_single_data_without_owner_check(self):
        post1 = None

        not_found = DataHandlerMixin._check_data(post=post1)
        self.assertEqual({'message': 'post not found'}, not_found[0])
        self.assertEqual(404, not_found[1])

    def test_not_existing_single_data_with_owner_check(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        db.session.add(user)
        db.session.commit()

        post1 = None

        not_found_or_not_owner = DataHandlerMixin._check_data('post', user, post=post1)
        self.assertEqual({'message': 'post not found'}, not_found_or_not_owner[0])
        self.assertEqual(404, not_found_or_not_owner[1])

    def test_existing_data_without_owner_check(self):
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

        not_found = DataHandlerMixin._check_data(post=post1, comment=comment1)
        self.assertIsNone(not_found)

    def test_existing_data_with_owner_check_from_owner(self):
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

        not_found_or_not_owner = DataHandlerMixin._check_data('comment', user, post=post1, comment=comment1)
        self.assertIsNone(not_found_or_not_owner)

    def test_existing_data_with_owner_check_from_not_owner(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        user2 = User(
            email='t@t2.com',
            username='user2'
        )
        user2.hash_password('1q2w3e')
        db.session.add_all([user, user2])
        db.session.commit()

        post1 = Post(author_id=user.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        comment1 = Comment(author_id=user2.id,
                           post_id=post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        not_found_or_not_owner = DataHandlerMixin._check_data('comment', user, post=post1, comment=comment1)
        self.assertEqual({'message': 'you cannot edit this comment'}, not_found_or_not_owner[0])
        self.assertEqual(403, not_found_or_not_owner[1])

    def test_not_existing_data_without_owner_check(self):
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

        comment1 = None

        not_found = DataHandlerMixin._check_data(post=post1, comment=comment1)
        self.assertEqual({'message': 'comment not found'}, not_found[0])
        self.assertEqual(404, not_found[1])

    def test_not_existing_data_with_owner_check(self):
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

        comment1 = None

        not_found_or_not_owner = DataHandlerMixin._check_data('comment', user, post=post1, comment=comment1)
        self.assertEqual({'message': 'comment not found'}, not_found_or_not_owner[0])
        self.assertEqual(404, not_found_or_not_owner[1])
