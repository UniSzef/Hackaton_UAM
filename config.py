import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///school.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = 'development'
