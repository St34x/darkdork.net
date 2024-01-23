# app/routes/change_token_price.py

from flask import Blueprint, jsonify, session
from flask_login import  login_required
from ..models import TokenPricing  # Assuming you have a User model defined

# Create a Blueprint
change_token_price_blueprint = Blueprint('change_token_price', __name__)

@change_token_price_blueprint.route('/token-pricing/<token_type>', methods=['PUT'])
@login_required
def update_token_price(token_type):
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    new_price = data.get('price_per_million')

    token_pricing = TokenPricing.query.filter_by(type=token_type).first()
    if token_pricing:
        token_pricing.price_per_million = new_price
        db.session.commit()
        return jsonify({"message": "Price updated successfully"}), 200
    else:
        return jsonify({"error": "Token type not found"}), 404

