import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///real_estate.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False