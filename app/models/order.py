"""Order Model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from app.constants import ORDER_STATUS_PENDING

Base = declarative_base()


class Order(Base):
    """Order Database Model"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Customer Info
    telegram_id = Column(String(255), index=True, nullable=False)
    username = Column(String(255), nullable=True)
    
    # Product Info
    product_name = Column(String(255), nullable=False)
    product_id = Column(String(50), nullable=False)
    duration_days = Column(Integer, nullable=False)  # 30, 90, 180, 365
    bandwidth_gb = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    
    # Discount
    discount_code = Column(String(100), nullable=True)
    discount_amount = Column(Float, default=0.0)
    final_price = Column(Float, nullable=False)
    
    # Status
    status = Column(String(50), default=ORDER_STATUS_PENDING, index=True)
    
    # Payment Info
    payment_method = Column(String(50), nullable=True)  # telegram, crypto, nowpayment, gateway
    payment_transaction_id = Column(String(255), nullable=True, unique=True)
    
    # VPN Config
    panel_type = Column(String(50), nullable=True)  # marzban, xui, pasargad
    username_on_panel = Column(String(255), nullable=True)
    config_link = Column(Text, nullable=True)  # Subscription link
    
    # Referral
    referrer_telegram_id = Column(String(255), nullable=True)
    referral_commission = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    paid_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional Info
    notes = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Order {self.order_id} - {self.status}>"
