import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_buddy.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(60), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=True)
    email_verified = db.Column(db.Boolean(), default=False)

    study_plans = db.relationship('StudyPlan', backref='user', lazy=True)
    study_materials = db.relationship('StudyMaterial', backref='user', lazy=True)
    study_sessions = db.relationship('StudySession', backref='user', lazy=True)
    reminders = db.relationship('Reminder', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        if self.validate_email(email):
            self.email = email
        else:
            raise ValueError("Invalid email format")
        self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.id)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.set_password(password)

    def set_password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def validate_email(self, email):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    tags = db.Column(db.String(100), nullable=True)
    attachments = db.Column(db.String(255), nullable=True)
    comments = db.Column(db.Text(), nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=1)
    progress = db.Column(db.Integer, nullable=False, default=0)
    due_date = db.Column(db.DateTime(), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  
    def __repr__(self):
        return '<StudyPlan {}>'.format(self.title)

class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(100), nullable=True)
    attachments = db.Column(db.String(255), nullable=True)
    comments = db.Column(db.Text(), nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=1)
    progress = db.Column(db.Integer, nullable=False, default=0)
    due_date = db.Column(db.DateTime(), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 
    def __repr__(self):
        return '<StudyMaterial {}>'.format(self.title)
    
class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    tags = db.Column(db.String(100), nullable=True)
    attachments = db.Column(db.String(255), nullable=True)
    comments = db.Column(db.Text(), nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=1)
    progress = db.Column(db.Integer, nullable=False, default=0)
    due_date = db.Column(db.DateTime(), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    study_plan_id = db.Column(db.Integer, db.ForeignKey('study_plan.id'), nullable=False)

    def __repr__(self):
        return '<StudySession {}>'.format(self.title)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    reminder_time = db.Column(db.DateTime(), nullable=False)
    tags = db.Column(db.String(100), nullable=True)
    attachments = db.Column(db.String(255), nullable=True)
    comments = db.Column(db.Text(), nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=1)
    progress = db.Column(db.Integer, nullable=False, default=0)
    due_date = db.Column(db.DateTime(), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return '<Reminder {}>'.format(self.title)