"""User Model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from app.constants import USER_STATUS_ACTIVE, PERMISSION_USER

Base = declarative_base()


class User(Base):
    """User Database Model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    
    # Account Status
    status = Column(String(50), default=USER_STATUS_ACTIVE, index=True)
    is_banned = Column(Boolean, default=False)
    ban_reason = Column(Text, nullable=True)
    ban_until = Column(DateTime, nullable=True)
    
    # Permission Level
    permission_level = Column(Integer, default=PERMISSION_USER)
    
    # Financial
    balance = Column(Float, default=0.0)  # Wallet balance
    referral_balance = Column(Float, default=0.0)  # Referral earnings
    total_spent = Column(Float, default=0.0)
    total_referral_earned = Column(Float, default=0.0)
    
    # Referral System
    referral_code = Column(String(50), unique=True, nullable=True, index=True)
    referred_by = Column(String(255), nullable=True)  # Referrer's telegram_id
    referral_count = Column(Integer, default=0)
    
    # Language Preference
    language = Column(String(10), default="fa")
    
    # Preferences
    notifications_enabled = Column(Boolean, default=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Additional Info
    ip_address = Column(String(50), nullable=True)
    device_info = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<User {self.telegram_id} - {self.username}>"
