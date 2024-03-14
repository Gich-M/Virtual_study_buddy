import bcrypt
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import random
import string
import pyotp

Base = declarative_base()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), default='user')
    date_of_birth = Column(DateTime)
    profile_picture = Column(String(255))
    bio = Column(String(255))
    location = Column(String(100))
    account_status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    otp_secret = Column(String(16))
    otp_enabled = Column(Boolean, default=False)

    def __init__(self, username, email, password):
        self.first_name, self.middle_name, self.last_name = self.parse_username(username)
        self.email = email
        self.password = self.hash_password(password)

    def parse_username(self, username):
        parts = username.split()
        first_name = parts[0]
        last_name = parts[-1]
        middle_name = ' '.join(parts[1:-1]) if len(parts) > 2 else ''
        return first_name, middle_name, last_name

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def get_role(self):
        return self.role
    
    def get_account_status(self):
        return self.account_status

    def enable_otp(self):
        if not self.otp_enabled:
            self.otp_enabled = True
            self.otp_secret = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])

    def disable_otp(self):
        if self.otp_enabled:
            self.otp_enabled = False
            self.otp_secret = None

    def generate_otp(self):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()
        return pyotp.TOTP(self.otp_secret)

    def verify_otp(self, otp):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp)

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

