# app/routes/change_username.py

from flask import Blueprint, request, jsonify, session
from flask_login import  login_required, current_user
from ..models import User  # Assuming you have a User model defined

# Create a Blueprint
change_username_blueprint = Blueprint('ch_username', __name__)

@change_username_blueprint.route('/change-username/user/<int:user_id>', methods=['POST'])
@login_required
def change_username(user_id):
    # Check if current user is authorized to change this user's username
    if not current_user.is_admin and user_id != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    new_username = data.get('new_username')
    if not new_username:
        return jsonify({"error": "New username not provided"}), 400

    # Check if the new username is already taken
    if User.query.filter_by(username=new_username).first():
        return jsonify({"error": "Username already taken"}), 409

    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.username = new_username
    db.session.commit()

    return jsonify({"message": "Username changed successfully"}), 200

