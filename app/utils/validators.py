"""Input Validators"""

import re
from typing import Tuple


class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_telegram_id(telegram_id: str) -> bool:
        """Validate Telegram ID"""
        try:
            return telegram_id.isdigit() and len(telegram_id) > 5
        except:
            return False
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format"""
        # Username should be alphanumeric, underscore allowed, 3-32 chars
        pattern = r'^[a-zA-Z0-9_]{3,32}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate payment amount"""
        try:
            return amount > 0 and amount < 1000000
        except:
            return False
    
    @staticmethod
    def validate_discount_code(code: str) -> bool:
        """Validate discount code format"""
        pattern = r'^[A-Z0-9]{4,20}$'
        return bool(re.match(pattern, code))
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letters"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letters"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain numbers"
        
        return True, "Password is valid"
