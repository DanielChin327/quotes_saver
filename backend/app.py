from flask import Flask, request, jsonify  # Import Flask to create the app and handle requests/responses
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy to interact with the database
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # JWT for token-based authentication
from flask_cors import CORS  # CORS to allow communication between frontend and backend

# Create the Flask application
app = Flask(__name__)

# Configuration for the app (e.g., database URI, secret keys)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Used for session encryption and JWT tokens
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/quotes_saver'  # Database URI (replace with your MySQL setup)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy modification tracking (not needed and uses extra memory)

# Initialize the database
db = SQLAlchemy(app)

# Initialize JWT for token-based authentication
jwt = JWTManager(app)

# Enable CORS to allow requests from the frontend
CORS(app)

# ------------------------
# Database Models
# ------------------------
class User(db.Model):
    """
    Represents the 'users' table in the database.
    Each user has a unique ID, a username, and a hashed password.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(100), unique=True, nullable=False)  # Username must be unique
    password = db.Column(db.String(255), nullable=False)  # User's hashed password

    def set_password(self, password):
        """Hashes the user's password and saves it to the 'password' field."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hashed password."""
        return check_password_hash(self.password, password)

class Quote(db.Model):
    """
    Represents the 'quotes' table in the database.
    Each quote is linked to a specific user (via user_id) and contains the text of the quote.
    """
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)  # Unique quote ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key referencing 'users' table
    quote = db.Column(db.Text, nullable=False)  # The text of the quote

# ------------------------
# User Registration Route
# ------------------------
@app.route('/register', methods=['POST'])
def register():
    """
    Registers a new user. Expects a JSON object with 'username' and 'password'.
    Returns a success message if the user is successfully registered.
    """
    data = request.json  # Get the JSON data sent from the frontend
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    # Create a new user and hash their password
    new_user = User(username=username)
    new_user.set_password(password)

    # Add the user to the database and commit the changes
    db.session.add(new_user)
    db.session.commit()

    # Return a success message
    return jsonify({"msg": "User registered successfully"}), 201

# ------------------------
# User Login Route
# ------------------------
@app.route('/login', methods=['POST'])
def login():
    """
    Logs in an existing user. Expects a JSON object with 'username' and 'password'.
    If the credentials are correct, returns a JWT token for the user.
    """
    data = request.json  # Get the JSON data sent from the frontend
    username = data.get('username')
    password = data.get('password')

    # Find the user in the database
    user = User.query.filter_by(username=username).first()

    # If the user doesn't exist or the password is incorrect, return an error
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    # If the credentials are correct, create a JWT token for the user
    access_token = create_access_token(identity=user.id)  # Identity is the user's unique ID

    return jsonify(access_token=access_token), 200  # Return the JWT token

# ------------------------
# Add a New Quote (Authenticated Route)
# ------------------------
@app.route('/quotes', methods=['POST'])
@jwt_required()  # This route requires the user to be logged in
def add_quote():
    """
    Adds a new quote for the logged-in user. Expects a JSON object with 'quote' text.
    Returns a success message if the quote is added.
    """
    user_id = get_jwt_identity()  # Get the ID of the currently logged-in user
    data = request.json  # Get the JSON data sent from the frontend
    quote_text = data.get('quote')

    # Create a new quote and associate it with the logged-in user
    new_quote = Quote(user_id=user_id, quote=quote_text)

    # Add the quote to the database and commit the changes
    db.session.add(new_quote)
    db.session.commit()

    return jsonify({"msg": "Quote added"}), 201  # Return a success message

# ------------------------
# Get Quotes for Logged-In User (Authenticated Route)
# ------------------------
@app.route('/quotes', methods=['GET'])
@jwt_required()  # This route requires the user to be logged in
def get_quotes():
    """
    Retrieves all quotes for the currently logged-in user.
    Returns the list of quotes in JSON format.
    """
    user_id = get_jwt_identity()  # Get the ID of the currently logged-in user
    quotes = Quote.query.filter_by(user_id=user_id).all()  # Fetch all quotes for this user

    # Return the quotes in JSON format
    return jsonify([{"id": q.id, "quote": q.quote} for q in quotes]), 200

# ------------------------
# Run the Flask Application
# ------------------------
if __name__ == "__main__":
    # This will run the Flask app in development mode, so you can see errors and debugging information
    app.run(debug=True)
