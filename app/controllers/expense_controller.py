"""
Expense Controller
Handles expense CRUD operations and summary reports
All APIs are JWT protected and user-based
"""

import logging
from flask import request, jsonify, send_file
from sqlalchemy.exc import SQLAlchemyError

from app.extensions.db import db
from app.models.expense_model import Expense
from app.utils.jwt_helper import jwt_user_required, get_current_user_id
from app.services.report_service import generate_pdf_report



# Create a New Expense

@jwt_user_required
def create_expense():
    """
    Create a new expense for the logged-in user
    """

    try:
        user_id = get_current_user_id()
        data = request.get_json() or {}

        required_fields = ["expense_date", "category", "amount"]
        if not all(data.get(field) for field in required_fields):
            return jsonify({"message": "Required fields are missing"}), 400

        expense = Expense(
            user_id=user_id,
            expense_date=data.get("expense_date"),
            category=data.get("category"),
            amount=data.get("amount"),
            description=data.get("description"),
            payment_mode=data.get("payment_mode"),
            merchant_name=data.get("merchant_name"),
            location=data.get("location"),
            notes=data.get("notes")
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({
            "message": "Expense created successfully",
            "expense": {
                "expense_id": expense.expense_id,
                "expense_date": expense.expense_date,
                "category": expense.category,
                "amount": float(expense.amount),
                "description": expense.description,
                "payment_mode": expense.payment_mode,
                "merchant_name": expense.merchant_name,
                "location": expense.location,
                "notes": expense.notes,
                "created_at": expense.created_at
            }
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error while creating expense: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while creating expense: {e}")
        return jsonify({"message": "Internal server error"}), 500



# Get All Expenses of Logged-in User

@jwt_user_required
def get_expenses():
    """
    Fetch all expenses of the logged-in user
    """

    try:
        user_id = get_current_user_id()

        expenses = Expense.query.filter_by(user_id=user_id).all()

        result = []
        for exp in expenses:
            result.append({
                "expense_id": exp.expense_id,
                "expense_date": exp.expense_date,
                "category": exp.category,
                "amount": float(exp.amount),
                "description": exp.description,
                "payment_mode": exp.payment_mode,
                "merchant_name": exp.merchant_name,
                "location": exp.location,
                "notes": exp.notes,
                "created_at": exp.created_at
            })

        return jsonify({
            "message": "Expenses fetched successfully",
            "expenses": result
        }), 200

    except SQLAlchemyError as e:
        logging.error(f"Database error while fetching expenses: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while fetching expenses: {e}")
        return jsonify({"message": "Internal server error"}), 500



# Update an Existing Expense

@jwt_user_required
def update_expense(expense_id):
    """
    Update an existing expense of the logged-in user
    """

    try:
        user_id = get_current_user_id()
        data = request.get_json() or {}

        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        if not expense:
            return jsonify({"message": "Expense not found"}), 404

        # Update allowed fields
        for field in [
            "expense_date", "category", "amount", "description",
            "payment_mode", "merchant_name", "location", "notes"
        ]:
            if field in data:
                setattr(expense, field, data[field])

        db.session.commit()

        return jsonify({
            "message": "Expense updated successfully",
            "expense": {
                "expense_id": expense.expense_id,
                "expense_date": expense.expense_date,
                "category": expense.category,
                "amount": float(expense.amount),
                "description": expense.description,
                "payment_mode": expense.payment_mode,
                "merchant_name": expense.merchant_name,
                "location": expense.location,
                "notes": expense.notes,
                "created_at": expense.created_at
            }
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error while updating expense: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while updating expense: {e}")
        return jsonify({"message": "Internal server error"}), 500



# Delete an Expense

@jwt_user_required
def delete_expense(expense_id):
    """
    Delete an expense of the logged-in user
    """

    try:
        user_id = get_current_user_id()

        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        if not expense:
            return jsonify({"message": "Expense not found"}), 404

        db.session.delete(expense)
        db.session.commit()

        return jsonify({
            "message": "Expense deleted successfully"
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error while deleting expense: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while deleting expense: {e}")
        return jsonify({"message": "Internal server error"}), 500



# Category-wise Expense Summary

@jwt_user_required
def expense_summary_by_category():
    """
    Generate total expense amount grouped by category
    """

    try:
        user_id = get_current_user_id()

        summary = (
            db.session.query(
                Expense.category,
                db.func.sum(Expense.amount).label("total_amount")
            )
            .filter(Expense.user_id == user_id)
            .group_by(Expense.category)
            .all()
        )

        result = [
            {"category": row.category, "total_amount": float(row.total_amount)}
            for row in summary
        ]

        return jsonify({
            "message": "Expense summary generated successfully",
            "summary": result
        }), 200

    except SQLAlchemyError as e:
        logging.error(f"Database error while generating summary: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error while generating summary: {e}")
        return jsonify({"message": "Internal server error"}), 500



# Export Expenses as PDF
@jwt_user_required
def export_expenses_pdf():
    """
    Export logged-in user's expenses as PDF
    """

    try:
        user_id = get_current_user_id()

        expenses = Expense.query.filter_by(user_id=user_id).all()

        if not expenses:
            return jsonify({"message": "No expenses found"}), 404

        expense_data = [{
            "expense_date": e.expense_date,
            "category": e.category,
            "amount": float(e.amount),
            "payment_mode": e.payment_mode
        } for e in expenses]

        pdf_file = generate_pdf_report(expense_data)

        return send_file(
            pdf_file,
            download_name="expenses_report.pdf",
            as_attachment=True,
            mimetype="application/pdf"
        )

    except SQLAlchemyError as e:
        logging.error(f"Database error during PDF export: {e}")
        return jsonify({"message": "Database error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error during PDF export: {e}")
        return jsonify({"message": "Internal server error"}), 500