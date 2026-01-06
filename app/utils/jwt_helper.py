"""
JWT Helper Utility
Handles JWT creation, validation, decoding and revocation
for Expense Tracker API (User-based only)
"""

from functools import wraps
from datetime import timedelta
import logging

from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)

# Token expiry configuration

ACCESS_EXPIRES = timedelta(minutes=30)
REFRESH_EXPIRES = timedelta(days=30)
ID_TOKEN_EXPIRES = timedelta(minutes=60)


# In-memory token blocklist (logout revoke)

_BLOCKLIST = set()




# Build claims to embed inside token

def build_claims(user, token_type: str):
    """
    Common claims added inside JWT payload
    """
    return {
        "user_id": str(user.user_id),
        "name": user.full_name,
        "email": user.email,
        "token_type": token_type
    }





# Create Access, Refresh and ID Tokens

def create_tokens_for_user(user):
    """
    Generates access, refresh and id tokens for authenticated user
    """

    if not user or not user.user_id:
        raise ValueError("Invalid user data")

    try:
        access_token = create_access_token(
            identity=str(user.user_id),
            additional_claims=build_claims(user, "access"),
            expires_delta=ACCESS_EXPIRES
        )

        refresh_token = create_refresh_token(
            identity=str(user.user_id),
            additional_claims={
                "user_id": str(user.user_id),
                "token_type": "refresh"
            },
            expires_delta=REFRESH_EXPIRES
        )

        id_token = create_access_token(
            identity=str(user.user_id),
            additional_claims=build_claims(user, "id"),
            expires_delta=ID_TOKEN_EXPIRES
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "id_token": id_token
        }

    except Exception as e:
        logging.error(f"Token creation failed: {e}")
        raise





# Create new access token using refresh token

def create_access_token_for_refresh(user):
    """
    Generates a new access token using valid refresh token
    """

    if not user or not user.user_id:
        raise ValueError("Invalid user data for refresh")

    try:
        return create_access_token(
            identity=str(user.user_id),
            additional_claims=build_claims(user, "access"),
            expires_delta=ACCESS_EXPIRES
        )

    except Exception as e:
        logging.error(f"Access token refresh failed: {e}")
        raise




# Token revocation helpers (Logout)

def revoke_jti(jti: str):
    """
    Store revoked token jti in blocklist
    """
    _BLOCKLIST.add(jti)


def revoke_current_token():
    """
    Revoke currently used JWT token
    """
    try:
        payload = get_jwt()
        jti = payload.get("jti")

        if jti:
            revoke_jti(jti)
            return True

    except Exception as e:
        logging.error(f"Token revoke failed: {e}")

    return False


def is_token_revoked(jwt_payload):
    """
    Check whether token is revoked
    """
    return jwt_payload.get("jti") in _BLOCKLIST




# JWT protected route decorator (Access token only)

def jwt_user_required(fn):
    """
    Protect routes using access token + revoke validation
    """

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        try:
            payload = get_jwt()

            # Revoke check
            if is_token_revoked(payload):
                return jsonify({"message": "Token revoked"}), 401

            # Token type validation
            if payload.get("token_type") != "access":
                return jsonify({"message": "Invalid token type"}), 401

            return fn(*args, **kwargs)

        except Exception as e:
            logging.error(f"JWT validation error: {e}")
            return jsonify({"message": "Unauthorized"}), 401

    return wrapper




# Helper functions to extract user info from token

def get_current_user_id():
    """
    Get logged-in user id from JWT
    """
    return get_jwt_identity()


def get_current_user_claims():
    """
    Get full decoded JWT payload (claims)
    """
    return get_jwt()
