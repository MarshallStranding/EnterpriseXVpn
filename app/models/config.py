"""VPN Config Model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from app.constants import CONFIG_STATUS_ACTIVE

Base = declarative_base()


class VPNConfig(Base):
    """VPN Configuration Database Model"""
    __tablename__ = "vpn_configs"
    
    id = Column(Integer, primary_key=True)
    config_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # User Info
    telegram_id = Column(String(255), index=True, nullable=False)
    username = Column(String(255), nullable=True)
    
    # Panel Info
    panel_type = Column(String(50), nullable=False)  # marzban, xui, pasargad
    panel_username = Column(String(255), nullable=False)  # Username on the panel
    
    # Config Details
    product_name = Column(String(255), nullable=False)
    bandwidth_gb = Column(Float, nullable=False)
    download_speed = Column(Integer, nullable=True)  # Mbps
    upload_speed = Column(Integer, nullable=True)  # Mbps
    
    # Status
    status = Column(String(50), default=CONFIG_STATUS_ACTIVE, index=True)
    is_trial = Column(Boolean, default=False)
    
    # Usage Statistics
    data_used_gb = Column(Float, default=0.0)
    remaining_gb = Column(Float, nullable=True)
    
    # Links & Config
    subscription_link = Column(Text, nullable=True)  # V2ray/Clash subscription link
    config_json = Column(Text, nullable=True)  # JSON config
    
    # Expiry
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    renewal_at = Column(DateTime, nullable=True)
    
    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    
    # Additional
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<VPNConfig {self.config_id} - {self.status}>"
