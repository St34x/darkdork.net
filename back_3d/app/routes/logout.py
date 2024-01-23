from flask_login import current_user, logout_user, login_required
from flask import Blueprint, jsonify, session
from ..models import User  
from ..requests import *

logout_blueprint = Blueprint('session', __name__)

@logout_blueprint.route('/logout')
@login_required
def logout():
    # Update token transactions in the database
    update_token_transactions_in_db(
        session['user_id'],
        session['incoming_tokens'],
        session['outgoing_tokens']
    )

    # Clear session data
    session.pop('user_id', None)
    session.pop('incoming_tokens', None)
    session.pop('outgoing_tokens', None)
    session.pop('total_cost', None)

    # Log out the user
    logout_user()

    # Redirect to login page or return a response
    return jsonify({"message": "You have been logged out."}), 200
