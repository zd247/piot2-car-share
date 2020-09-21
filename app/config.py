import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres:password@localhost:5432/'
database_name = 'piot2'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
    
    # Flask-User settings
    USER_APP_NAME = "CAR SHARE APP"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "piot2@gmail.com"
    
    ALLOWED_HOST = ['obscure-lowlands-84107.herokuapp.com', '127.0.0.1']
    
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # # Configure application to store JWTs in cookies. Whenever you make
    # # a request to a protected endpoint, you will need to send in the
    # # access or refresh JWT via a cookie.
    # JWT_TOKEN_LOCATION = ['cookies']
    
    # # # Set the cookie paths, so that you are only sending your access token
    # # # cookie to the access endpoints, and only sending your refresh token
    # # # to the refresh endpoint.
    # # JWT_ACCESS_COOKIE_PATH = '/api/'
    # # JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    
    # # This is a bad practice, not suppose to do this.
    # JWT_COOKIE_CSRF_PROTECT = False
    
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1, seconds=1)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@/piot2?unix_socket=/cloudsql/piot2790:mysequel'
