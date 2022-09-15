from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from secrets import token_hex
from werkzeug.security import generate_password_hash
from datetime import date, datetime

db = SQLAlchemy ()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)

class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable = False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    # img_url = db.Column(db.String(300), nullable=True)
    apitoken = db.Column(db.String, default=None, nullable=True)

    review = db.relationship("Review", backref='author', lazy=True)

    followed = db.relationship("User", 
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id), 
        secondary = followers,
        backref = db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
        )
    
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)
        # self.img_url = img_url

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }

    def updateUserInfo(self, username, email, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        # self.img_url = img_url

    def saveUpdates(self):
        db.session.commit()

    
    def follow(self,user):
        self.followed.append(user)
        db.session.commit()

    def unfollow(self,user):
        self.followed.remove(user)
        db.session.commit()

    def delete(self):
        print(self)
        db.session.delete(self)
        db.session.commit()

    def get_followed_posts(self):
            followed = Review.query.join(followers, (Review.user_id == followers.c.followed_id)).filter(followers.c.follower_id == self.id)
            mine = Review.query.filter_by(user_id = self.id)
            all = followed.union(mine).order_by(Review.date_created.desc())
            return all

class Review(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150), nullable=True)
    img_url = db.Column(db.String(300))
    review_capt = db.Column(db.String(500))
    date_reviewed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    rating_value = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self,title,img_url,review_capt, rating_value, user_id):
        self.title = title
        self.img_url = img_url
        self.review_capt = review_capt
        self.rating_value = rating_value
        self.user_id = user_id
    
    def updateReview(self,title,img_url,review_capt,rating_value):
        self.title = title
        self.img_url = img_url
        self.review_capt = review_capt
        self.rating_value = rating_value

    def save(self):
        db.session.add(self)
        db.session.commit()

    def saveUpdate(self):
        db.session.commit()

    def deleteReview(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'review': self.review_capt,
            'img_url': self.img_url,
            'date_reviewed': self.date_reviewed,
            'user_id': self.user_id,
            'rating_value' : self.rating_value,
            'author': self.author.username
        }

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150), nullable=True)
    # author = db.Column(db.String(150), nullable=True)
    img_url = db.Column(db.String(300))
    shelf = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self,title, img_url, shelf, user_id):
        self.title = title
        # self.author = author
        self.img_url = img_url
        self.shelf = shelf
        self.user_id = user_id
    
    def updateBook(self,title,img_url,shelf):
        self.title = title
        # self.author = author
        self.img_url = img_url
        self.shelf = shelf

    def save(self):
        db.session.add(self)
        db.session.commit()

    def savebook(self):
        db.session.commit()

    def deleteBook(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            # 'author': self.author,
            'shelf': self.shelf,
            'img_url': self.img_url,
            'user_id': self.user_id,
        }

