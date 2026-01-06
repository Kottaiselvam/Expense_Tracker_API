"""
Application Configuration
Expense Tracker API
"""

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    
    # Core Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", "expense-tracker-secret-key")


    # Database Configuration (MySQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:kottai%401310@localhost:3306/expense_tracker"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY", "expense-tracker-jwt-secret"
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 30))
    )

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 30))
    )

    JWT_ID_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ID_TOKEN_EXPIRES", 60))
    )


    # Environment
    ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = ENV == "development"
