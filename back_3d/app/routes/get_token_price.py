# app/routes/get_token_price.py

from flask import Blueprint, jsonify, session
from werkzeug.security import check_password_hash
from flask_login import  login_required
from flask_login import  login_required, current_user
from ..models import TokenPricing  

# Create a Blueprint
get_token_price_blueprint = Blueprint('get_token_prices', __name__)

@get_token_price_blueprint.route('/get-token-prices', methods=['GET'])
@login_required
def get_token_prices():
    # Check if current user is authorized to request this api
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized access"}), 403

    try:
        incoming_price = TokenPricing.query.filter_by(type='incoming').first()
        outgoing_price = TokenPricing.query.filter_by(type='outgoing').first()

        if not incoming_price or not outgoing_price:
            return jsonify({"error": "Token pricing not found"}), 404

        prices = {
            "incomingPrice": incoming_price.price_per_million,
            "outgoingPrice": outgoing_price.price_per_million
        }

        return jsonify(prices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
