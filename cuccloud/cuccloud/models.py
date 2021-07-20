# -*- encoding=UTF-8 -*-

from flask.helpers import send_file
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy.orm import backref
from cuccloud import app, db, login_manager
from datetime import datetime
import random


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(36), unique=True)
    usernickname = db.Column(db.String(80))
    password = db.Column(db.String(32))
    salt = db.Column(db.String(10))
    #public_key = db.relationship('', backref='user', lazy='dynamic')
    #private_key = 
    def __init__(self, username, usernickname, password, salt=''):
        self.username = username
        self.usernickname = usernickname
        self.password = password
        self.salt = salt

    def __repr__(self):
        return '<User %d %s %s >' % (self.id, self.username, self.usernickname)

    # Flask Login接口
    def is_authenticated(self):
        print
        'is_authenticated'
        return True

    def is_active(self):
        print
        'is_active'
        return True

    def is_anonymous(self):
        print
        'is_anonymous'
        return False

    def get_id(self):
        print
        'get_id'
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)