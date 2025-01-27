from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from .utils import gregorian_to_hebrew

# Join table for User and Family
user_families = db.Table('user_families',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('family_id', db.Integer, db.ForeignKey('family.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(64), default='user', nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    families = db.relationship('Family', secondary=user_families, backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gregorian_death_date = db.Column(db.Date, nullable=False)
    hebrew_year = db.Column(db.Integer, nullable=False)
    hebrew_month = db.Column(db.Integer, nullable=False)
    hebrew_day = db.Column(db.Integer, nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    milestones = db.relationship('Milestone', backref='post', lazy=True, cascade="all, delete-orphan")

    def set_hebrew_death_date(self):
        self.hebrew_year, self.hebrew_month, self.hebrew_day = gregorian_to_hebrew(self.gregorian_death_date)
    
    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(120))
    order = db.Column(db.Integer, nullable=False, default=0)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    def __repr__(self):
        return '<Milestone {}>'.format(self.title)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    members = db.relationship('Post', backref='family', lazy=True)

    def __repr__(self):
        return f'<Family {self.name}>'
