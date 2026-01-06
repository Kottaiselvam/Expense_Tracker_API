"""
Application Entry Point
Expense Tracker API
"""

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions.db import db
from app.extensions.bcrypt import bcrypt
from app.extensions.jwt import jwt

# Import routes (blueprints)
from app.routes.auth_routes import auth_bp
from app.routes.forgot_pass_route import forget_bp
from app.routes.user_routes import user_bp
from app.routes.expense_routes import expense_bp


# Import JWT revoke checker
from app.utils.jwt_helper import is_token_revoked


def create_app():
    """
    Application factory function
    """

    app = Flask(__name__)
    app.config.from_object(Config)


    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True)

    
    # JWT Blocklist (Token Revoke) Handler
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """
        Check whether JWT token is revoked (logout)
        """
        return is_token_revoked(jwt_payload)


    # JWT Error Handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"message": "Token has expired"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"message": "Invalid token"}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {"message": "Authorization token is required"}, 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {"message": "Token has been revoked"}, 401


    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(forget_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(expense_bp)


    # Health Check Endpoint
    @app.route("/home", methods=["GET"])
    def health_check():
        """
        Health check endpoint
        """
        return {
            "status": "OK",
            "message": "Expense Tracker API is running"
        }, 200


    # Create DB Tables (Development Only)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)