"""Subscription Model for Imported Configs"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from app.constants import CONFIG_STATUS_ACTIVE

Base = declarative_base()


class ImportedSubscription(Base):
    """Imported Subscription from External Source"""
    __tablename__ = "imported_subscriptions"
    
    id = Column(Integer, primary_key=True)
    subscription_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # User Info
    telegram_id = Column(String(255), index=True, nullable=False)
    username = Column(String(255), nullable=True)
    
    # Subscription Link
    subscription_link = Column(Text, nullable=False)  # Base64 encoded link
    link_hash = Column(String(255), unique=True, nullable=False, index=True)  # Hash of the link
    
    # Subscription Details (parsed from link)
    name = Column(String(255), nullable=True)  # Subscription name
    source = Column(String(100), nullable=True)  # Source of subscription (bot name, URL, etc)
    
    # Status
    status = Column(String(50), default=CONFIG_STATUS_ACTIVE, index=True)
    
    # Usage
    last_updated = Column(DateTime, nullable=True)
    last_used = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ImportedSubscription {self.subscription_id} - {self.name}>"
