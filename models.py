from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid

# The db object instantiated from the class SQLAlchemy represents the database and
# provides access to all the functionality of Flask-SQLAlchemy
db = SQLAlchemy()

# create tables for db
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    
    catches = db.relationship('Catch', backref='user')
    
    def __repr__(self):
        return '<User %r>' % self.username

class Catch(db.Model):
    __tablename__ = 'catches'
    
    catch_id = db.Column(db.String(36), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    fish_type = db.Column(db.String(20))
    weight = db.Column(db.Float)
    length = db.Column(db.Float)
    lure = db.Column(db.String(20))
    location = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    user_username = db.Column(db.String(20), db.ForeignKey('users.username'))
    
    def __repr__(self):
        return '<Catch %r>' % self.catch_id