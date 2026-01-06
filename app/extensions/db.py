# app/extensions/db.py

from flask_sqlalchemy import SQLAlchemy

# Purpose:
# This db object is a SINGLE database instance
# Used across models, controllers, services
db = SQLAlchemy()
