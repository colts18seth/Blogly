"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def home():
    """redirect to /users"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """List users and show form"""
    users = User.query.all()
    return render_template("list.html", users=users)


@app.route("/users/new", methods=["GET", "POST"])
def create_user():
    """Create new user or display form"""

    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url'] or None

        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()

        return redirect("/users")
    else:
        return render_template("new_user.html")


@app.route("/users/<int:user_id>")
def details(user_id):
    """details for user"""
  
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = id)

    return render_template("details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit(user_id):
    """ edit user """

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']

        db.session.add(user)
        db.session.commit()

        return redirect(f"/users/{user_id}")
    else:
        return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    """ delete user """

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def add_post(user_id):
    """ add post """

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        user_id = user.id

        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()

        return redirect(f"/users/{user_id}")
    else:
        return render_template("new_post.html", user=user)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """  show post """

    post = Post.query.get_or_404(post_id)
    user= User.query.filter_by(id = post.user_id).one()

    return render_template("show_post.html", post=post, user=user)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    """ edit post """

    post = Post.query.get_or_404(post_id)
    user = post.user

    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']

        db.session.add(post)
        db.session.commit()

        return redirect(f"/users/{post.user_id}")
    else:
        return render_template("edit_post.html", post=post, user=user)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """ delete post """

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)   
    db.session.commit()
    return redirect(f"/users/{user_id}")