"""Referral Model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Referral(Base):
    """Referral Transaction Database Model"""
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True)
    referral_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Referrer Info
    referrer_telegram_id = Column(String(255), index=True, nullable=False)
    referrer_username = Column(String(255), nullable=True)
    
    # Referred User Info
    referred_telegram_id = Column(String(255), index=True, nullable=False)
    referred_username = Column(String(255), nullable=True)
    
    # Commission Info
    order_id = Column(String(100), nullable=False, index=True)  # Order that generated commission
    original_amount = Column(Float, nullable=False)  # Original order amount
    commission_percentage = Column(Float, nullable=False)  # Commission %
    commission_amount = Column(Float, nullable=False)  # Commission amount
    
    # Status
    is_paid = Column(Boolean, default=False)
    is_cancelled = Column(Boolean, default=False)
    
    # Withdrawal
    withdrawal_id = Column(String(100), nullable=True)  # If withdrawn
    withdrawal_date = Column(DateTime, nullable=True)
    withdrawal_method = Column(String(50), nullable=True)  # wallet, crypto, etc
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    paid_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Referral {self.referral_id} - {self.commission_amount}>"
