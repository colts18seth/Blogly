from app import app
from unittest import TestCase
from models import User, Post, db

class BloglyTestCase(TestCase):
    """ Testing users/posts flask app project """

    def setUp(self):
        db.drop_all()
        db.create_all()

        user1 = User(first_name="John", last_name="Doe")
        user2 = User(first_name="Jane", last_name="Buck")

        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

        user1_post = Post(title="new post!!", content="i made this post", user_id=1)
        user1_post2 = Post(title="new post...again!!", content="i made this post too", user_id=1)
        user2_post = Post(title="new post 3!!", content="i made this post AGAIN", user_id=2)
        user2_post2 = Post(title="new post #4!!", content="i made this post LAST", user_id=2)


        db.session.add(user1_post)
        db.session.add(user1_post2)
        db.session.add(user2_post)
        db.session.add(user2_post2)

        db.session.commit()

    def test_root_html(self):
        with app.test_client() as client:
            res = client.get('/', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-1 m-5">Users</h1>', html)

    def test_user_details(self):
        with app.test_client() as client:
            res = client.get('/users/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-3 m-5">John Doe</h1>', html)

    def test_create(self):
        with app.test_client() as client:
            res = client.post('/users/new', data={'first_name': 'james', 'last_name': 'johnson', 'image_url': 'no_image.com'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('james', html)

    def test_delete_post(self):
        with app.test_client() as client:
            res = client.post('/posts/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-primary mt-3">Add Post</button>', html)