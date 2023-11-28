from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db


views= Blueprint('views', __name__)


@views.route("/")
@views.route("/main", methods=['GET'])
def main():
    posts= Post.query.all()
    return render_template("main.html",user= None, posts= posts,  ) 

@views.route("/home")
@login_required
def index():
    posts= Post.query.all()
    return render_template("home.html" , name= current_user.username, user= current_user, posts=posts)

@login_required
@views.route("/create-post", methods=["GET", "POST"])
def create_post():
    if request.method== "POST":
        text= request.form.get("text")
        if not text:
            flash('Post can not be empty', category= 'error')
        else:
            post= Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post Created!', category='success')
            return redirect(url_for("views.index"))

    return render_template("create_post.html", user= current_user)
# ---------------
# Delete  Post
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id= id).first()
    print(f"Post ID: {post.id}")
    print(f"Author ; {post.author} ")
    print(f"Current user id: {current_user.id}")
    if not post:
        flash("This Post is not exist!", category= "error")

    elif current_user.id != post.author:
        flash("You don\'t have the premission to delete this post", category= "error")

    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfuly.", category= "success")

    return redirect(url_for("views.index"))
# ----------------------------------------


# Viewing all user posts
@login_required
@views.route("/all-user-posts/<username>" )
def all_user_posts(username):
    user= User.query.filter_by(username= username).first()
    if not user:
        flash("No user with that username!", category="error")
        return redirect(url_for("views.index"))
     
    posts= user.posts
    return render_template(f"all_user_posts.html" ,user=current_user, posts= posts, username= username)

# Create comment View

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text= request.form.get('text')
    if not text:
        flash('Comment can not be empty!', category='error')
    else:
        post= Post.query.filter_by(id= post_id) 
        if post:
            comment= Comment(comment=text, author= current_user.id, post_id= post_id)
            db.session.add(comment)
            db.session.commit()
            # flash('You add a comment successfuly.', category= 'success')
        else:
            flash('Post Doesn\'t exist!' , category= 'error') 
        
    return redirect(url_for('views.index'))


# Delete Comments
@views.route("/delete-comment/<id>")
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id= id).first()
  
    if not comment:
        flash("This comment is not exist!", category= "error")

    elif current_user.id != comment.author:
        flash("You don\'t have the premission to delete this comment", category= "error")

    else:
        db.session.delete(comment)
        db.session.commit()
        flash("comment deleted successfuly.", category= "success")

    return redirect(url_for("views.index"))

# Controling likes
@views.route('/like-post/<post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post= Post.query.filter_by(id= post_id).first()
    like= Like.query.filter_by(author= current_user.id, post_id= post_id).first()
    if not post:
        jsonify({'error': 'Post dose not exist.'},400)
        
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like= Like(author= current_user.id, post_id= post_id)
        db.session.add(like)
        db.session.commit()
    return jsonify({"likes": len(post.likes), "liked" : current_user.id in map(lambda x:  x.author, post.likes)})