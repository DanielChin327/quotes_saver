from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for ORM functionality
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

# Initialize SQLAlchemy
db = SQLAlchemy()

# -------------------------------------------
# User Model: Represents the users in the database
# -------------------------------------------
class User(db.Model):
    """
    Represents the 'users' table in the database.
    Each user has a unique ID, a username, and a hashed password.
    """
    __tablename__ = 'users'  # Name of the database table

    # Define the columns in the 'users' table
    user_id = db.Column(db.Integer, primary_key=True)  # Primary key (unique user ID)
    username = db.Column(db.String(100), unique=True, nullable=False)  # Username must be unique
    password = db.Column(db.String(255), nullable=False)  # Store the hashed password

    def set_password(self, password):
        """
        Hashes the password using a secure algorithm (SHA-256 with salt) and stores it.
        """
        self.password = generate_password_hash(password)  # Hash the password

    def check_password(self, password):
        """
        Verifies if the provided password matches the stored hashed password.
        """
        return check_password_hash(self.password, password)  # Compare passwords

# -------------------------------------------
# Quote Model: Represents user quotes in the database
# -------------------------------------------
class Quote(db.Model):
    """
    Represents the 'quotes' table in the database.
    Each quote is linked to a specific user (via user_id) and contains the text of the quote.
    """
    __tablename__ = 'quotes'  # Name of the database table

    # Define the columns in the 'quotes' table
    quote_id = db.Column(db.Integer, primary_key=True)  # Primary key (unique quote ID)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Foreign key referencing the user who added the quote
    quote = db.Column(db.Text, nullable=False)  # The text of the quote
