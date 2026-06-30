"""Payment Model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Payment(Base):
    """Payment Transaction Database Model"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Customer Info
    telegram_id = Column(String(255), index=True, nullable=False)
    username = Column(String(255), nullable=True)
    
    # Payment Info
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="IRR")  # IRR, USDT, ETH, BTC, TON
    payment_method = Column(String(50), nullable=False)  # telegram, nowpayment, cryptopay, gateway
    
    # Gateway Info
    gateway_transaction_id = Column(String(255), nullable=True, unique=True)
    gateway_response = Column(Text, nullable=True)  # JSON response from gateway
    
    # Status
    status = Column(String(50), nullable=False, index=True)  # pending, completed, failed, refunded
    is_verified = Column(Boolean, default=False)
    
    # Related Order
    order_id = Column(String(100), nullable=True, index=True)
    
    # Crypto Info (for crypto payments)
    wallet_address = Column(String(255), nullable=True)
    crypto_amount = Column(Float, nullable=True)
    confirmation_count = Column(Integer, default=0)
    
    # Refund Info
    is_refunded = Column(Boolean, default=False)
    refund_amount = Column(Float, nullable=True)
    refund_reason = Column(Text, nullable=True)
    refund_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    verified_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional
    notes = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<Payment {self.transaction_id} - {self.status}>"
