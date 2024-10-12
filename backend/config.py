import os

class Config:
    # Secret key for JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')

    # Database connection URI (use MySQL with pymysql)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3307/quotes_saver'

    # Disable modification tracking for SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
