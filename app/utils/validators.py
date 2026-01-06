import re
import logging


# Validates email format using regular expression
def valid_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    try:
        # Checks standard email pattern (name@domain.ext)
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))
    except Exception as e:
        # Logs any unexpected regex error
        logging.error(f"Email validation error: {e}")
        return False


# Validates password strength rules
def valid_password(password: str) -> bool:
    if not password or not isinstance(password, str):
        return False
    try:
        # Requires 8+ chars, one letter, one number, one special character
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', password))
    except Exception as e:
        # Logs validation failures
        logging.error(f"Password validation error: {e}")
        return False
