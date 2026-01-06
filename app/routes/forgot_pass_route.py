from flask import Blueprint
from app.controllers.forgot_pass_controller import (
    forgot_password,
    verify_otp,
    reset_password
)

forget_bp = Blueprint("forget", __name__, url_prefix="/auth")

# Sends OTP to user email for password reset
forget_bp.route("/forgot_password", methods=["POST"])(forgot_password)

# Verifies the OTP entered by the user
forget_bp.route("/verify_otp", methods=["POST"])(verify_otp)

# Updates user password after OTP verification
forget_bp.route("/reset_password", methods=["POST"])(reset_password)
