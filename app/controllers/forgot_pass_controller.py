import logging, random
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.extensions.db import db
from app.extensions.bcrypt import bcrypt
from app.models.user_model import User
from app.utils.validators import valid_email, valid_password

# In-memory OTP store (for demo)
reset_codes = {}

# Sends OTP to user email for password reset

def forgot_password():
    """
    Purpose:
    1. Accept email from user
    2. Validate email
    3. Check user exists
    4. Generate OTP and send (console(Terminal) for demo)
    """
    try:
        data = request.get_json() or {}
        email = (data.get("email") or "").strip().lower()

        if not email:
            return jsonify({"field": "email", "message": "Email is required"}), 400
        if not valid_email(email):
            return jsonify({"field": "email", "message": "Invalid email format"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Email not found"}), 404

        code = random.randint(100000, 999999)
        reset_codes[email] = code
        print(f"[RESET] OTP for {email}: {code}")

        return jsonify({"message": "OTP sent to your email"}), 200

    except SQLAlchemyError as e:
        logging.error(f"DB error in forgot_password: {e}")
        return jsonify({"message": "Database error"}), 500
    except Exception as e:
        logging.error(f"Unexpected error in forgot_password: {e}")
        return jsonify({"message": "Server error"}), 500


# Verifies the OTP entered by the user

def verify_otp():
    """
    Purpose:
    1. Accept email from user
    2. Validate email
    3. Check user exists
    4. Generate OTP and send (console for demo)
    """
    try:
        data = request.get_json() or {}
        email = (data.get("email") or "").strip().lower()
        code = str(data.get("code") or "").strip()

        if not email or not code:
            return jsonify({"message": "Email and OTP are required"}), 400

        if email not in reset_codes:
            return jsonify({"message": "No OTP request found for this email"}), 404
        if str(reset_codes[email]) != code:
            return jsonify({"message": "Invalid OTP"}), 400

        return jsonify({"message": "OTP verified"}), 200

    except Exception as e:
        logging.error(f"Unexpected error in verify_otp: {e}")
        return jsonify({"message": "Server error"}), 500


# Updates user password after OTP verification

def reset_password():
    """
    Purpose:
    1. Reset user password after OTP verification
    2. Hash password before saving
    """
    try:
        data = request.get_json() or {}
        email = (data.get("email") or "").strip().lower()
        new_password = data.get("new_password") or ""

        if not email or not new_password:
            return jsonify({"message": "Email and new password are required"}), 400

        if email not in reset_codes:
            return jsonify({"message": "OTP not verified for this email"}), 403

        if not valid_password(new_password):
            return jsonify({
                "message": "Password must contain letters, numbers, special chars and be 6+ chars"
            }), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        hashed_pw = bcrypt.generate_password_hash(new_password).decode("utf-8")
        user.password_hash = hashed_pw
        db.session.commit()

        del reset_codes[email]

        return jsonify({"message": "Password reset successful. Please login."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"DB error in reset_password: {e}")
        return jsonify({"message": "Database error"}), 500
    except Exception as e:
        logging.error(f"Unexpected error in reset_password: {e}")
        return jsonify({"message": "Server error"}), 500
