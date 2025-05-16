import os

basedir = os.path.dirname(os.path.abspath(__file__))
default_database_uri = 'sqlite:///' + os.path.join(basedir, 'explorate.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_default_secret')
    
class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_database_uri
    
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    #TESTING = True
    #DEBUG = True
    #WTF_CSRF_ENABLED = False  # Disable CSRF protection for testing
    