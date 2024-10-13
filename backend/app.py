from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from models import db, User, Quote

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config.Config')

# Initialize database with app
db.init_app(app)

# Initialize JWT for handling tokens
jwt = JWTManager(app)

# Enable CORS for frontend interaction (React)
CORS(app)

@app.route('/')
def testing():
    return "Routes is Working."

# -------------------------------------------
# Register Route: To create a new user
# -------------------------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json  # Get JSON data from the request
    username = data.get('username')
    password = data.get('password')

    # Check if the username is already taken
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    # Create a new user
    new_user = User(username=username)
    new_user.set_password(password)

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

# -------------------------------------------
# Login Route: To authenticate a user
# -------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Get the JSON data sent from the frontend
    username = data.get('username')
    password = data.get('password')

    # Find the user in the database
    user = User.query.filter_by(username=username).first()

    # If the user doesn't exist or the password is incorrect, return an error
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    # Print the hashed password stored in the database
    print(f"Stored password (hashed): {user.password}")
    print(f"Provided password: {password}")

    # Check if the provided password matches the hashed password
    if not user.check_password(password):
        print("Password check failed")
        return jsonify({"msg": "Bad username or password"}), 401

    # If the credentials are correct, create a JWT token for the user
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# -------------------------------------------
# Add Quote Route: To add a quote (Authenticated)
# -------------------------------------------
@app.route('/quotes', methods=['POST'])
@jwt_required()
def add_quote():
    user_id = get_jwt_identity()  # Get current user's ID from the token
    data = request.json
    quote_text = data.get('quote')

    # Create a new quote
    new_quote = Quote(user_id=user_id, quote=quote_text)

    # Save the quote in the database
    db.session.add(new_quote)
    db.session.commit()

    return jsonify({"msg": "Quote added successfully"}), 201

# -------------------------------------------
# Get Quotes Route: Fetch all quotes for logged-in user (Authenticated)
# -------------------------------------------
@app.route('/quotes', methods=['GET'])
@jwt_required()
def get_quotes():
    user_id = get_jwt_identity()  # Get current user's ID from token
    quotes = Quote.query.filter_by(user_id=user_id).all()

    # Return the quotes as a JSON list
    return jsonify([{"id": q.id, "quote": q.quote} for q in quotes]), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
