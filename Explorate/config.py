import os

basedir = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_default_secret')
    
class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.join(basedir, '..', 'instance')), 'explorate.db')
    
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.join(basedir, '..', 'instance')), 'test.db')
    #TESTING = True
    #DEBUG = True
    #WTF_CSRF_ENABLED = False  # Disable CSRF protection for testing
    