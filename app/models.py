from enum import unique
from operator import index

from sqlalchemy.orm import backref
from . import db
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200),index = True)
    email = db.Column(db.String(200),unique = True,index = True)
    bio = db.Column(db.String(200))
    profile_pic_path = db.Column(db.String)
    password_hash = db.Column(db.String(200))

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
    ___Tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    content = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitches_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save_comment(self):
        db.session.add()
        db.session.commit()

    @classmethod
    def get_comments(self,id):
        comment = Comments.query.order_by(Comments.time_commented.desc()).filter_by(pitches_id = id).all()
        return comment



class Votes(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer,primary_key = True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitches_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save_vote(self):
        db.session.add()
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitches_id):
        votes = Votes.filter_by(user_id=user_id, pitches_id=pitches_id).all()
        return votes