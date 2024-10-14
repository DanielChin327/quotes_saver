from flask import Flask, request, jsonify  # Import Flask and functions to handle requests and responses
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database interactions
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # JWT for token-based authentication
from flask_cors import CORS  # CORS to handle frontend-backend cross-origin requests
from models import db, User, Quote  # Import database models from models.py

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py (e.g., database URI, secret key)
app.config.from_object('config.Config')

# Initialize the database with the Flask app
db.init_app(app)

# Initialize JWT for token-based authentication management
jwt = JWTManager(app)

# Enable CORS to allow requests from the frontend (e.g., React app)
CORS(app)

# -------------------------------------------
# Root Route: Basic test route
# -------------------------------------------
@app.route('/')
def testing():
    """
    A simple route to check if the app is running.
    Returns a string message.
    """
    return "Routes is Working."

# -------------------------------------------
# Register Route: To create a new user
# -------------------------------------------
@app.route('/register', methods=['POST'])
def register():
    """
    Handles user registration. Expects a JSON object with 'username' and 'password'.
    Creates a new user if the username doesn't already exist.
    """
    data = request.json  # Get JSON data from the request body
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists in the database
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400  # Return an error if the username is taken

    # Create a new User object and hash the password
    new_user = User(username=username)
    new_user.set_password(password)

    # Save the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Return success message
    return jsonify({"msg": "User registered successfully"}), 201

# -------------------------------------------
# Login Route: To authenticate a user
# -------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    """
    Handles user login. Expects a JSON object with 'username' and 'password'.
    If valid credentials are provided, returns a JWT token for the user.
    """
    data = request.json  # Get JSON data from the request
    username = data.get('username')
    password = data.get('password')

    # Find the user in the database by username
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and if the password matches the hashed password
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401  # Return an error if the login fails

    # Generate a JWT token for the user (identity is user_id)
    access_token = create_access_token(identity=user.user_id)

    # Return the token
    return jsonify(access_token=access_token), 200

# -------------------------------------------
# Add Quote Route: To add a quote (Authenticated)
# -------------------------------------------

@app.route('/quotes', methods=['POST'])
@jwt_required()  # Requires the user to be logged in (JWT token required)
def add_quote():
    """
    Adds a new quote for the logged-in user.
    Expects a JSON object with 'quote' text.
    """
    user_id = get_jwt_identity()  # Get the ID of the logged-in user from the JWT token
    data = request.json
    quote_text = data.get('quote')

    # Create a new Quote object and associate it with the logged-in user
    new_quote = Quote(user_id=user_id, quote=quote_text)

    # Save the new quote to the database
    db.session.add(new_quote)
    db.session.commit()

    # Return success message
    return jsonify({"msg": "Quote added successfully"}), 201

# -------------------------------------------
# Get Quotes Route: Fetch all quotes for the logged-in user (Authenticated)
# -------------------------------------------
@app.route('/quotes', methods=['GET'])
@jwt_required()  # Requires the user to be logged in (JWT token required)
def get_quotes():
    """
    Fetches all quotes for the logged-in user.
    Returns the list of quotes in JSON format.
    """
    user_id = get_jwt_identity()  # Get the ID of the logged-in user from the JWT token
    quotes = Quote.query.filter_by(user_id=user_id).all()  # Fetch quotes for the logged-in user

    # Return the quotes as a list of dictionaries (quote ID and text)
    return jsonify([{"id": q.quote_id, "quote": q.quote} for q in quotes]), 200

# -------------------------------------------
# Run the Flask application
# -------------------------------------------
if __name__ == '__main__':
    """
    Starts the Flask app in debug mode. Debug mode provides helpful error messages.
    """
    app.run(debug=True)
