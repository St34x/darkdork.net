# app/routes/change_password.py

from werkzeug.security import check_password_hash
from flask import Blueprint, jsonify, session
from flask_login import  login_required
from ..models import User  # Assuming you have a User model defined

# Create a Blueprint
change_passwd_blueprint = Blueprint('ch_passwd', __name__)

@change_passwd_blueprint.route('/user/<int:user_id>', methods=['POST'])
@login_required
def change_password(user_id):
    # Check if current user is authorized to change this user's username
    if not current_user.is_admin and user_id != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    user = User.query.get(user_id)

    if not user or not user.verify_password(data['old_password']):
        return jsonify({"error": "Invalid user or password"}), 400

    user.set_password(data['new_password'])
    db.session.commit()

    return jsonify({"message": "Password changed successfully"}), 200

