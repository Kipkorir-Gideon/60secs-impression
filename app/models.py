from enum import unique
from operator import index
from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200),index = True)
    email = db.Column(db.String(200),unique = True,index = True)
    bio = db.Column(db.String(200))
    profile_pic_path = db.Column(db.String)
    password_hash = db.Column(db.String(200))