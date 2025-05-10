from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from realestate_app import db, login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    properties = db.relationship('Property', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rooms = db.Column(db.Integer)
    area = db.Column(db.Float)
    property_type = db.Column(db.String(50))
    image = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Property {self.title}>'

    def image_url(self):
        if self.image:
            from flask import url_for
            return url_for('static', filename=f'uploads/{self.image}')
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))