"""Admin Action Log Model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AdminLog(Base):
    """Admin Action Logging for Audit Trail"""
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True)
    log_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Admin Info
    admin_telegram_id = Column(String(255), index=True, nullable=False)
    admin_username = Column(String(255), nullable=True)
    
    # Action Info
    action_type = Column(String(100), nullable=False, index=True)  # user_ban, user_unban, product_edit, etc
    action_description = Column(Text, nullable=False)
    
    # Target Info
    target_type = Column(String(50), nullable=True)  # user, product, order, etc
    target_id = Column(String(255), nullable=True, index=True)
    target_name = Column(String(255), nullable=True)
    
    # Details
    old_value = Column(Text, nullable=True)  # Previous value (JSON)
    new_value = Column(Text, nullable=True)  # New value (JSON)
    
    # Metadata
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<AdminLog {self.action_type} by {self.admin_username}>"
