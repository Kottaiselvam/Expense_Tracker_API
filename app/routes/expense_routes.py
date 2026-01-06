"""
Expense Routes
Defines API endpoints for expense CRUD and reports
"""

from flask import Blueprint
from app.controllers.expense_controller import (
    create_expense,
    get_expenses,
    update_expense,
    delete_expense,
    expense_summary_by_category,
    export_expenses_pdf
)

expense_bp = Blueprint("expense", __name__, url_prefix="/api")

# Create a new expense
expense_bp.route("/expenses", methods=["POST"])(create_expense)

# Get all expenses of logged-in user
expense_bp.route("/expenses", methods=["GET"])(get_expenses)

# Update a specific expense
expense_bp.route("/expenses/<int:expense_id>", methods=["PUT"])(update_expense)

# Delete a specific expense
expense_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])(delete_expense)

# Get category-wise expense summary
expense_bp.route("/expenses/summary", methods=["GET"])(expense_summary_by_category)

# Export expenses as PDF
expense_bp.route("/expenses/export/pdf", methods=["GET"])(export_expenses_pdf)