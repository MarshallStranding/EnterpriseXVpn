"""Helper Functions"""

import random
import string
from datetime import datetime
from typing import Dict, Any


class Helpers:
    """Helper utility functions"""
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_order_id() -> str:
        """Generate unique order ID"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_str = Helpers.generate_random_string(6)
        return f"ORD_{timestamp}_{random_str}"
    
    @staticmethod
    def format_bytes(bytes_value: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    @staticmethod
    def format_currency(amount: float, currency: str = "$") -> str:
        """Format amount to currency"""
        return f"{currency} {amount:,.2f}"
    
    @staticmethod
    def get_expiry_status(expires_at: datetime) -> str:
        """Get expiry status"""
        days_left = (expires_at - datetime.utcnow()).days
        
        if days_left < 0:
            return "❌ Expired"
        elif days_left == 0:
            return "⚠️ Expires Today"
        elif days_left <= 7:
            return f"⚠️ {days_left} days left"
        else:
            return f"✅ {days_left} days left"
    
    @staticmethod
    def truncate_string(text: str, length: int = 50) -> str:
        """Truncate string with ellipsis"""
        if len(text) > length:
            return text[:length-3] + "..."
        return text
    
    @staticmethod
    def create_inline_button(text: str, callback_data: str) -> Dict[str, str]:
        """Create inline button for Telegram"""
        return {"text": text, "callback_data": callback_data}
