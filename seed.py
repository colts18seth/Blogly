from models import User, Post, db
from app import app

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