"""
Auth Routes
Maps auth endpoints to controller functions
"""

from flask import Blueprint
from app.controllers.auth_controller import signup, login, refresh_token, logout

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Register new user
auth_bp.route("/signup", methods=["POST"])(signup)

# Login user and generate JWT tokens
auth_bp.route("/login", methods=["POST"])(login)

# Refresh access token using refresh token
auth_bp.route("/refresh", methods=["POST"])(refresh_token)

# Logout user (client-side token removal)
auth_bp.route("/logout", methods=["POST"])(logout)
