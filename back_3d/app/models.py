
# apap.models.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from .database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    incoming_tokens = db.Column(db.Float, default=0.0)  # Number of tokens received
    outgoing_tokens = db.Column(db.Float, default=0.0)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class TokenPricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # 'incoming' or 'outgoing'
    price_per_million = db.Column(db.Float)  # Price per million tokens

# The load_user function
def load_user(user_id):
    return User.query.get(int(user_id))
