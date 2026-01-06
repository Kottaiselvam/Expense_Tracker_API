"""
Auth Controller
Handles user authentication for Expense Tracker API
Includes signup, login, refresh token and logout
"""

import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.extensions.db import db
from app.extensions.bcrypt import bcrypt
from app.models.user_model import User
from app.utils.jwt_helper import (
    create_tokens_for_user,
    create_access_token_for_refresh,
    revoke_current_token
)


# User Signup

def signup():
    """
    Register a new user with hashed password
    """

    try:
        data = request.get_json() or {}

        full_name = data.get("full_name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")

        # Required field validation
        if not all([full_name, email, password, confirm_password]):
            return jsonify({"message": "All fields are required"}), 400

        # Password match check
        if password != confirm_password:
            return jsonify({"message": "Passwords do not match"}), 400

        # Check existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 409

        # Hash password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create user object
        user = User(
            full_name=full_name,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "User already exists"}), 409

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error during signup: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error during signup: {e}")
        return jsonify({"message": "Internal server error"}), 500



# User Login

def login():
    """
    Authenticate user and generate JWT access, refresh and id tokens
    """

    try:
        data = request.get_json() or {}

        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        # Input validation
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        # Fetch user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Invalid email or password"}), 401

        # Verify password
        if not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({"message": "Invalid email or password"}), 401

        # Create JWT tokens
        tokens = create_tokens_for_user(user)

        return jsonify({
            "message": "Login successful",
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "id_token": tokens["id_token"],
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        }), 200

    except SQLAlchemyError as e:
        logging.error(f"Database error during login: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error during login: {e}")
        return jsonify({"message": "Internal server error"}), 500



# Refresh Access Token

@jwt_required(refresh=True)
def refresh_token():
    """
    Generate a new access token using refresh token
    """

    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "Invalid refresh token"}), 401

        # Fetch user
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Create new access token
        new_access_token = create_access_token_for_refresh(user)

        return jsonify({
            "message": "Access token refreshed successfully",
            "access_token": new_access_token
        }), 200

    except SQLAlchemyError as e:
        logging.error(f"Database error during token refresh: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error during token refresh: {e}")
        return jsonify({"message": "Internal server error"}), 500



# User Logout

@jwt_required()
def logout():
    """
    Logout user by revoking current JWT token (jti based)
    """

    try:
        revoked = revoke_current_token()
        if not revoked:
            return jsonify({"message": "Failed to revoke token"}), 500

        return jsonify({
            "message": "Logout successful"
        }), 200

    except Exception as e:
        logging.error(f"Unexpected error during logout: {e}")
        return jsonify({"message": "Internal server error"}), 500
