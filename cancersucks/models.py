from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
class Meetup(db.Model):
    __tablename__ = "meetup"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String())
    date = db.Column(db.DateTime, server_default=db.func.now())
    title = db.Column(db.String())
    location = db.Column(db.String())
    longlat = db.Column(db.String())
    time = db.Column(db.String())
    sponsor = db.Column(db.String())
    description = db.Column(db.String())
     
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer(), primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    date = db.Column(db.DateTime, server_default=db.func.now())
    msg = db.Column(db.String())
        

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    about_me = db.Column(db.String())
    email = db.Column(db.String())
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    address =  db.Column(db.String())
    phone_number= db.Column(db.String())
    treatment_center =  db.Column(db.String())
    children_name = db.Column(db.String())
    children_age = db.Column(db.String())
    children_hobbies = db.Column(db.String())
    longlat = db.Column(db.String())
    social_worker_phone = db.Column(db.String())
    social_worker_name = db.Column(db.String())
    birthday = db.Column(db.String())
    siblings = db.Column(db.String())
    facebook = db.Column(db.String())
    twitter = db.Column(db.String())
    acc_type = db.Column(db.String())
    state = db.Column(db.String())
    diagnosis = db.Column(db.String())
    approved = db.Column(db.Boolean(), default=False) 

    def __init__(self, username="", password="", email="", address="", phone_number="", treatment_center="", children_hobbies="", children_age="", children_name="", longlat="", social_worker_name="", social_worker_phone="", birthday="", siblings="", facebook="", twitter="", acc_type="", state="", diagnosis="", firstname="", lastname="", about_me=""):
        self.username = username
        self.password = password
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.treatment_center = treatment_center
        self.children_hobbies = children_hobbies
        self.children_name = children_name
        self.children_age = children_age
        self.longlat = longlat
        self.social_worker_phone = social_worker_phone
        self.social_worker_name = social_worker_name
        self.birthday = birthday
        self.siblings = siblings
        self.facebook = facebook
        self.twitter = twitter
        self.acc_type = acc_type
        self.state = state
        self.diagnosis = diagnosis
        self.firstname = firstname
        self.lastname = lastname
        self.about_me = about_me
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username
