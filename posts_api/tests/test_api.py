import base64
import os
from unittest import TestCase

from flask_app import db, app
from flask_app.models import User, Post, Comment
from flask_app.serializers import posts_list_schema, post_create_schema


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


class AuthTestCase(BaseTestCase):

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)

    def test_registration_not_valid(self):
        post_data = {
            'email': 't@t.com',
            'username': 'Test_user_1',
        }
        response = self.client.post('/api/v1/registration', json=post_data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, User.query.count())

    def test_registration_valid(self):
        post_data = {
            'email': 't@t.com',
            'username': 'Test_user_1',
            'password': 'password'
        }
        response = self.client.post('/api/v1/registration', json=post_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, User.query.count())

    def test_create_post_without_auth(self):
        post_data = {
            'title': 'Test title',
            'content': 'test content'
        }
        response = self.client.post('/api/v1/posts', json=post_data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(0, Post.query.count())

    def test_create_post_with_auth(self):
        user = User(
            email='t@t.com',
            username='user1'
        )
        user.hash_password('1q2w3e')
        db.session.add(user)
        db.session.commit()

        post_data = {
            'title': 'Test title',
            'content': 'test content'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.post('/api/v1/posts', headers={'Authorization': f'Basic {auth}'}, json=post_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Post.query.count())


class PostsTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.user = User(
            email='t@t.com',
            username='user1'
        )
        self.user.hash_password('1q2w3e')

        self.post_owner = User(
            email='t@t2.com',
            username='user2'
        )
        self.post_owner.hash_password('1q2w3e')
        db.session.add_all([self.user, self.post_owner])
        db.session.commit()

    def test_posts_list(self):
        post1 = Post(author_id=self.user.id, title='Title 1', content='Content 1')
        post2 = Post(author_id=self.user.id, title='Title 2', content='Content 2')
        post3 = Post(author_id=self.user.id, title='Title 3', content='Content 3')
        db.session.add_all([post1, post2, post3])
        db.session.commit()

        response = self.client.get('/api/v1/posts')
        self.assertEqual(200, response.status_code)

        posts = Post.query.order_by(Post.publication_datetime.desc()).all()
        serializer_data = posts_list_schema.dump(posts)
        response_data = response.get_json()
        self.assertEqual(serializer_data, response_data['data'])

    def test_get_post(self):
        post1 = Post(author_id=self.user.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        response = self.client.get(f'/api/v1/posts/{post1.id}')
        self.assertEqual(200, response.status_code)

        serializer_data = post_create_schema.dump(post1)
        response_data = response.get_json()
        self.assertEqual(serializer_data, response_data)

    def test_update_post_not_owner(self):
        post1 = Post(author_id=self.post_owner.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        update_data = {
            'title': 'Test Title 1',
            'content': 'Content 1'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.put(f'/api/v1/posts/{post1.id}', headers={'Authorization': f'Basic {auth}'},
                                   json=update_data)
        self.assertEqual(403, response.status_code)
        self.assertEqual('Title 1', post1.title)

    def test_update_post_owner(self):
        post1 = Post(author_id=self.user.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        update_data = {
            'title': 'Test Title 1',
            'content': 'Content 1'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.put(f'/api/v1/posts/{post1.id}', headers={'Authorization': f'Basic {auth}'},
                                   json=update_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Test Title 1', post1.title)

    def test_partial_update_post_not_owner(self):
        post1 = Post(author_id=self.post_owner.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        update_data = {
            'content': 'Patched Content 1'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.patch(f'/api/v1/posts/{post1.id}', headers={'Authorization': f'Basic {auth}'},
                                     json=update_data)
        self.assertEqual(403, response.status_code)
        self.assertEqual('Content 1', post1.content)

    def test_partial_update_post_owner(self):
        post1 = Post(author_id=self.user.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        update_data = {
            'content': 'Patched Content 1'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.patch(f'/api/v1/posts/{post1.id}', headers={'Authorization': f'Basic {auth}'},
                                     json=update_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Patched Content 1', post1.content)

    def test_delete_post_not_owner(self):
        post1 = Post(author_id=self.post_owner.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.delete(f'/api/v1/posts/{post1.id}', headers={'Authorization': f'Basic {auth}'})
        self.assertEqual(403, response.status_code)
        self.assertEqual(1, Post.query.count())

    def test_delete_post_owner(self):
        post1 = Post(author_id=self.user.id, title='Title 1', content='Content 1')
        db.session.add(post1)
        db.session.commit()

        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.delete(f'/api/v1/posts/{post1.id}', headers={'Authorization': f'Basic {auth}'})
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Post.query.count())


class CommentsTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.user = User(
            email='t@t.com',
            username='user1'
        )
        self.user.hash_password('1q2w3e')
        self.post_owner = User(
            email='t@t2.com',
            username='user2'
        )
        self.post_owner.hash_password('1q2w3e')
        db.session.add_all([self.user, self.post_owner])
        db.session.commit()

        self.post1 = Post(author_id=self.post_owner.id, title='Title 1', content='Content 1')
        db.session.add(self.post1)
        db.session.commit()

    def test_create_comment_without_auth(self):
        post_data = {
            'title': 'Test comment title',
            'content': 'test comment content'
        }
        response = self.client.post(f'/api/v1/posts/{self.post1.id}/comments', json=post_data)
        self.assertEqual(401, response.status_code)

        # Обновление поста в БД
        db.session.add(self.post1)
        db.session.commit()

        self.assertEqual(0, self.post1.comments.count())

    def test_create_comment_with_auth(self):
        post_data = {
            'title': 'Test comment title',
            'content': 'test comment content'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.post(f'/api/v1/posts/{self.post1.id}/comments', headers={'Authorization': f'Basic {auth}'},
                                    json=post_data)
        self.assertEqual(201, response.status_code)

        # Обновление поста в БД
        db.session.add(self.post1)
        db.session.commit()

        self.assertEqual(1, self.post1.comments.count())

    def test_update_comment_not_owner(self):
        comment1 = Comment(author_id=self.post_owner.id,
                           post_id=self.post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        update_data = {
            'title': 'Test Comment Title 1',
            'content': 'Content 1'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.put(f'/api/v1/posts/{self.post1.id}/comments/{comment1.id}',
                                   headers={'Authorization': f'Basic {auth}'}, json=update_data)
        self.assertEqual(403, response.status_code)
        self.assertEqual('Comment Title 1', comment1.title)

    def test_update_comment_owner(self):
        comment1 = Comment(author_id=self.user.id,
                           post_id=self.post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        update_data = {
            'title': 'Test Comment Title 1',
            'content': 'Content 1'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.put(f'/api/v1/posts/{self.post1.id}/comments/{comment1.id}',
                                   headers={'Authorization': f'Basic {auth}'}, json=update_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Test Comment Title 1', comment1.title)

    def test_partial_update_comment_not_owner(self):
        comment1 = Comment(author_id=self.post_owner.id,
                           post_id=self.post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        update_data = {
            'content': 'Content 1'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.patch(f'/api/v1/posts/{self.post1.id}/comments/{comment1.id}',
                                     headers={'Authorization': f'Basic {auth}'}, json=update_data)
        self.assertEqual(403, response.status_code)
        self.assertEqual('Comment Content 1', comment1.content)

    def test_partial_update_comment_owner(self):
        comment1 = Comment(author_id=self.user.id,
                           post_id=self.post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        update_data = {
            'content': 'Test Comment Content 1'
        }
        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.patch(f'/api/v1/posts/{self.post1.id}/comments/{comment1.id}',
                                     headers={'Authorization': f'Basic {auth}'}, json=update_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Test Comment Content 1', comment1.content)

    def test_delete_comment_not_owner(self):
        comment1 = Comment(author_id=self.post_owner.id,
                           post_id=self.post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.delete(f'/api/v1/posts/{self.post1.id}/comments/{comment1.id}',
                                      headers={'Authorization': f'Basic {auth}'})
        self.assertEqual(403, response.status_code)
        self.assertEqual(1, Comment.query.count())

    def test_delete_comment_owner(self):
        comment1 = Comment(author_id=self.user.id,
                           post_id=self.post1.id,
                           title='Comment Title 1',
                           content='Comment Content 1')
        db.session.add(comment1)
        db.session.commit()

        auth = base64.b64encode(b"user1:1q2w3e").decode("utf-8")
        response = self.client.delete(f'/api/v1/posts/{self.post1.id}/comments/{comment1.id}',
                                      headers={'Authorization': f'Basic {auth}'})
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Comment.query.count())
