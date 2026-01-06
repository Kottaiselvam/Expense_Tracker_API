"""
User Routes
Defines API endpoints for user profile actions
"""

from flask import Blueprint
from app.controllers.user_controller import (
    get_user_profile,
    update_user_profile,
    delete_user_account
)

user_bp = Blueprint("user", __name__, url_prefix="/user")

# Get logged-in user's profile
user_bp.route("/profile", methods=["GET"])(get_user_profile)

# Update logged-in user's profile
user_bp.route("/profile", methods=["PUT"])(update_user_profile)

# Delete logged-in user's account
user_bp.route("/profile", methods=["DELETE"])(delete_user_account)
