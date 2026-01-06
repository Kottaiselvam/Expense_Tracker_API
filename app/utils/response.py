"""
Response Utility
Provides standard API response structure
"""

from flask import jsonify


def success_response(message, data=None, status_code=200):
    """
    Return standardized success response
    """
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data

    return jsonify(response), status_code


def error_response(message, status_code=400):
    """
    Return standardized error response
    """
    return jsonify({
        "success": False,
        "message": message
    }), status_code
