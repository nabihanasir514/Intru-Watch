# Authentication Utilities for IntruWatch

import hashlib
import re
from typing import Tuple


def hash_password(password: str) -> str:
    """Hash password using SHA-256
    
    In production, consider using bcrypt or argon2 for better security
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against stored hash"""
    return hash_password(password) == password_hash


def is_valid_giki_email(email: str) -> bool:
    """Validate GIKI email format (xxxx@giki.edu.pk)"""
    pattern = r'^[a-zA-Z0-9._%+-]+@giki\.edu\.pk$'
    return re.match(pattern, email) is not None


def validate_registration_number(reg_no: str) -> Tuple[bool, str]:
    """Validate GIKI student registration number format
    
    Expected format: YYYYNNN (e.g., 2024113)
    - First 4 digits: Year (2020-2030)
    - Last 3 digits: Serial number
    """
    if not reg_no:
        return False, "Registration number is required"
    
    if not reg_no.isdigit():
        return False, "Registration number must contain only digits"
    
    if len(reg_no) != 7:
        return False, "Registration number must be 7 digits (YYYYNNN)"
    
    year = int(reg_no[:4])
    if year < 2020 or year > 2030:
        return False, "Invalid year in registration number"
    
    return True, "Valid registration number"


def validate_employee_id(emp_id: str) -> Tuple[bool, str]:
    """Validate employee ID format
    
    Expected format: EMP followed by 3+ digits (e.g., EMP456)
    """
    if not emp_id:
        return False, "Employee ID is required"
    
    pattern = r'^EMP\d{3,}$'
    if not re.match(pattern, emp_id):
        return False, "Employee ID must be in format EMP followed by 3+ digits (e.g., EMP456)"
    
    return True, "Valid employee ID"


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Check password strength
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, "Password meets requirements"


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '\\', ';', '&', '|']
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()
