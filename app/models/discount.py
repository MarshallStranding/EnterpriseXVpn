"""Discount Code Model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DiscountCode(Base):
    """Discount Code Database Model"""
    __tablename__ = "discount_codes"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Discount Type
    discount_type = Column(String(20), nullable=False)  # percentage, fixed_amount
    discount_value = Column(Float, nullable=False)  # Percentage (0-100) or amount
    
    # Limitations
    max_uses = Column(Integer, nullable=True)  # None = unlimited
    used_count = Column(Integer, default=0)
    
    max_per_user = Column(Integer, default=1)  # Max times per user
    min_order_amount = Column(Float, default=0.0)  # Minimum order amount
    max_discount_amount = Column(Float, nullable=True)  # Max discount amount
    
    # Expiry
    active_from = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    description = Column(Text, nullable=True)
    created_by = Column(String(255), nullable=True)  # Admin username
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DiscountCode {self.code}>"
