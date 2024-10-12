from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

# User model: Represents the users in the database
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        # Hash the password and store it
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # Check if the given password matches the stored hash
        return check_password_hash(self.password, password)

# Quote model: Represents user quotes in the database
class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quote = db.Column(db.Text, nullable=False)
