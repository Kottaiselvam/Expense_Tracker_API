"""
User Controller
Handles logged-in user profile actions (GET, PUT, DELETE)
All actions are JWT protected and user-id based
"""

import logging
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from app.extensions.db import db
from app.models.user_model import User
from app.utils.jwt_helper import jwt_user_required, get_current_user_id



# Get Logged-in User Profile

@jwt_user_required
def get_user_profile():
    """
    Fetch the profile details of the currently logged-in user
    """

    try:
        user_id = get_current_user_id()

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            "message": "User profile fetched successfully",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "created_at": user.created_at
            }
        }), 200

    except SQLAlchemyError as e:
        logging.error(f"Database error while fetching user profile: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while fetching user profile: {e}")
        return jsonify({"message": "Internal server error"}), 500



# Update Logged-in User Profile

@jwt_user_required
def update_user_profile():
    """
    Update profile details of the currently logged-in user
    """

    try:
        user_id = get_current_user_id()
        data = request.get_json() or {}

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Allowed fields for update
        full_name = data.get("full_name")
        email = data.get("email")

        if not full_name and not email:
            return jsonify({"message": "No data provided for update"}), 400

        # Update fields if provided
        if full_name:
            user.full_name = full_name.strip()

        if email:
            user.email = email.strip().lower()

        db.session.commit()

        return jsonify({
            "message": "User profile updated successfully",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error while updating user profile: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while updating user profile: {e}")
        return jsonify({"message": "Internal server error"}), 500



# Delete Logged-in User Account

@jwt_user_required
def delete_user_account():
    """
    Delete the currently logged-in user account
    """

    try:
        user_id = get_current_user_id()

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            "message": "User account deleted successfully"
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error while deleting user account: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while deleting user account: {e}")
        return jsonify({"message": "Internal server error"}), 500
