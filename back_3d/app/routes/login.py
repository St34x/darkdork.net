# app/routes/login.py

from flask_login import current_user, login_required, login_user
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from marshmallow import ValidationError
from ..schema import LoginSchema
from ..models import User  
from ..requests import *

# Create a Blueprint
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        # Deserialize and validate the request data
        schema = LoginSchema()
        data = schema.load(request.json)

        # Get username and password from request
        username = data['username']
        password = data['password']

        # Find user in the database
        user = User.query.filter_by(username=username).first()

        # Check user and password
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # User authenticated successfully
            session['user_id'] = user.id  # Set user ID in session
            # Fetch token information
            session['incoming_tokens'] = user.incoming_tokens
            session['outgoing_tokens'] = user.outgoing_tokens
            
            # Fetch token pricing information and calculate total cost
            incoming_pricing, outgoing_pricing = fetch_token_pricing()
            total_cost = calculate_total_cost(user.incoming_tokens, user.outgoing_tokens, incoming_pricing, outgoing_pricing)

            # Include total cost in session and user data
            session['total_cost'] = total_cost

            # Convert user data to a JSON-serializable format
            user_data = {
                "id": user.id,
                "username": user.username,
                "incoming_tokens": user.incoming_tokens,
                "outgoing_tokens": user.outgoing_tokens,
                "total_cost": total_cost,
            }

            return jsonify({"message": "Login successful", "user": user_data, "authenticated": True}), 200

    except ValidationError as err:
        # Return validation errors
        return jsonify(err.messages), 400

    # Return a generic error message for failed login (not revealing which part failed)
    return jsonify({"message": "Invalid username or password"}), 401


