"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

now = datetime.now()

def connect_db(app):
    """Connect to databse."""
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User Model """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                               primary_key=True,
                               autoincrement=True)
    first_name = db.Column(db.String(20),
                                             nullable=False)
    last_name = db.Column(db.String(20),
                                            nullable=True)
    image_url = db.Column(db.String,
                                            nullable=True,
                                            default='https://seeba.se/wp-content/themes/consultix/images/no-image-found-360x260.png')

    posts = db.relationship("Post", backref="user", cascade="all")

    def __repr__(self):
        """Show user info"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"


class Post(db.Model):
    """ Post Model """

    __tablename__= "posts"

    id = db.Column(db.Integer,
                               primary_key=True,
                               autoincrement=True)
    title = db.Column(db.String(20),
                                  nullable=False)
    content = db.Column(db.String,
                                        nullable=False)
    created_at = db.Column(db.String,
                                            default=now.strftime("%m/%d/%y, %H:%M:%S"))
    user_id = db.Column(db.Integer,
                                        db.ForeignKey('users.id'),
                                        nullable=False)

    tags = db.relationship('Tag', secondary='post_tag', backref='posts')
    
    def __repr__(self):
        """Show post info"""
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at}>"


class Tag(db.Model):
    """ Tags """

    __tablename__= "tags"

    id = db.Column(db.Integer,
                               primary_key=True,
                               autoincrement=True)
    name = db.Column(db.String(20),
                                  nullable=False)
    
    def __repr__(self):
        """Show tag info"""
        t = self
        return f"<Tag {t.id} {t.name}>"    


class PostTag(db.Model):
    """ Post/Tag Model """

    __tablename__= "post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),primary_key=True)
    
    def __repr__(self):
        """Show post info"""
        pt = self
        return f"<Post_Tag {pt.post_id} {pt.tag_id}>"