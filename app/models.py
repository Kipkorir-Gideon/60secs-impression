from enum import unique
from operator import index

from sqlalchemy.orm import backref
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200),index = True)
    email = db.Column(db.String(200),unique = True,index = True)
    bio = db.Column(db.String(200))
    profile_pic_path = db.Column(db.String)
    password_hash = db.Column(db.String(200))
    pitches = db.relationship('Pitch',backref='user',lazy='dynamic')
    comment = db.relationship('Comments',backref='user',lazy='dynamic')
    vote = db.relationship('Votes',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'



class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(255))

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        categories = Category.query.all()
        return categories


class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    category_id = db.Column(db.Integer,db.ForeignKey("categories.id"))
    content = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comments',backref='pitches',lazy = 'dynamic')
    vote = db.relationship('Votes',backref='pitches',lazy = 'dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    def get_pitches(id):
        pitches = Pitch.query.filter_by(category_id=id).all()
        return pitches

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(255))
    time_commented = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self,id):
        comment = Comments.query.order_by(Comments.time_commented.desc()).filter_by(pitches_id = id).all()
        return comment



class Votes(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer,primary_key = True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitches_id):
        votes = Votes.filter_by(user_id=user_id, pitches_id=pitches_id).all()
        return votes