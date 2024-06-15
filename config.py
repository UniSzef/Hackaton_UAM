import os

class Config:
<<<<<<< HEAD
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
=======
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///school.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = 'development'
>>>>>>> main
