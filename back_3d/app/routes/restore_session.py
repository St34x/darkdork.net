from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, jsonify, session
from ..models import User
from ..requests import *

restore_session_blueprint = Blueprint('re_session', __name__)

@restore_session_blueprint.route('/user')
@login_required
def get_user():
    user_id = current_user.get_id()
    user = User.query.get(user_id)
    if user:
        # Fetch token pricing information and calculate total cost
        incoming_pricing, outgoing_pricing = fetch_token_pricing()
        total_cost = calculate_total_cost(
                session['incoming_tokens'], 
                session['outgoing_tokens'], 
                incoming_pricing, 
                outgoing_pricing
        )

        user_data = {
            "id": user.id,
            "username": user.username,
            "incoming_tokens": session.get('incoming_tokens', 0),
            "outgoing_tokens": session.get('outgoing_tokens', 0),
            "total_cost": total_cost,
            "admin": user.admin,
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found"}), 404

