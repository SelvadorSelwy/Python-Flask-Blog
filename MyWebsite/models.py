from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(150), unique=True)
    email= db.Column(db.String(150), unique=True)
    password= db.Column(db.String(20))
    created_date= db.Column(db.DateTime(timezone=True),default=func.now())
    posts= db.relationship('Post', backref='user', passive_deletes=True)
    comments= db.relationship('Comment', backref='user', passive_deletes= True)
    likes= db.relationship('Like', backref='user', passive_deletes= True)


class Post(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    text= db.Column(db.Text, nullable= False)
    created_date= db.Column(db.DateTime(timezone=True), default= func.now())
    author= db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comments= db.relationship('Comment', backref='post', passive_deletes= True)
    likes= db.relationship('Like', backref='post', passive_deletes= True)


class Comment(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    comment= db.Column(db.Text(200), nullable=False)
    created_date= db.Column(db.DateTime(timezone=True), default=func.now())
    author= db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable= False)
    post_id= db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)


class Like(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date_created= db.Column(db.DateTime(timezone=True), default=func.now())
    author= db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable= False)
    post_id= db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable= False)