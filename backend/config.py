import os  # Import os to handle environment variables

class Config:
    """
    Configuration class for the Flask app.
    Contains settings for the secret key and database URI.
    """

    # Secret key for encrypting session data and signing JWT tokens
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')  # Default value if not set in environment

    # Database connection URI (using MariaDB with the pymysql driver)
    SQLALCHEMY_DATABASE_URI = 'mariadb+pymysql://root:@localhost:3307/quotes_saver'  # Update the URI as needed

    # Disable SQLAlchemy event system (not needed and consumes resources)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
