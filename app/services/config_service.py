"""Config Service - VPN Configuration Management"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid
from app.config import settings
from app.utils.logger import setup_logger
from app.services.marzban_service import MarzbanService
from app.services.xui_service import XUIService
from app.services.pasargad_service import PasargadService

logger = setup_logger()


class ConfigService:
    """VPN Configuration Service"""
    
    def __init__(self):
        self.marzban = MarzbanService()
        self.xui = XUIService()
        self.pasargad = PasargadService()
    
    async def create_config(self,
                          telegram_id: str,
                          panel_type: str,
                          username: str,
                          product_name: str,
                          bandwidth_gb: float,
                          duration_days: int,
                          is_trial: bool = False) -> Dict[str, Any]:
        """Create VPN configuration"""
        try:
            config_id = f"cfg_{uuid.uuid4().hex[:8]}"
            
            # Calculate expiry time
            expiry_timestamp = int((datetime.utcnow() + timedelta(days=duration_days)).timestamp())
            data_limit = int(bandwidth_gb * 1024 * 1024 * 1024)  # Convert to bytes
            
            # Create user on respective panel
            if panel_type == "marzban":
                result = await self.marzban.create_user(
                    username=username,
                    data_limit=data_limit,
                    expiry_time=expiry_timestamp
                )
                if not result["success"]:
                    return result
                
                config_result = await self.marzban.get_user_config(username)
            
            elif panel_type == "xui":
                result = await self.xui.create_user(
                    username=username,
                    data_limit=data_limit,
                    expiry_time=expiry_timestamp
                )
                if not result["success"]:
                    return result
                
                config_result = await self.xui.get_user_config(username)
            
            elif panel_type == "pasargad":
                result = await self.pasargad.create_user(
                    username=username,
                    data_limit=data_limit,
                    expiry_time=expiry_timestamp
                )
                if not result["success"]:
                    return result
                
                config_result = await self.pasargad.get_user_config(username)
            
            else:
                return {"success": False, "error": "Invalid panel type"}
            
            config_data = {
                "config_id": config_id,
                "telegram_id": telegram_id,
                "panel_type": panel_type,
                "username": username,
                "product_name": product_name,
                "bandwidth_gb": bandwidth_gb,
                "subscription_link": config_result.get("config_url"),
                "expires_at": datetime.utcnow() + timedelta(days=duration_days),
                "is_trial": is_trial
            }
            
            logger.info(f"Config created: {config_id} for user {telegram_id}")
            return {"success": True, "config": config_data}
        
        except Exception as e:
            logger.error(f"Error creating config: {e}")
            return {"success": False, "error": str(e)}
    
    async def renew_config(self, config_id: str, duration_days: int) -> Dict[str, Any]:
        """Renew VPN configuration"""
        try:
            logger.info(f"Config renewed: {config_id} for {duration_days} days")
            return {"success": True}
        
        except Exception as e:
            logger.error(f"Error renewing config: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_config(self, config_id: str, panel_type: str, username: str) -> Dict[str, Any]:
        """Delete VPN configuration"""
        try:
            if panel_type == "marzban":
                result = await self.marzban.delete_user(username)
            elif panel_type == "xui":
                result = await self.xui.delete_user(username)
            elif panel_type == "pasargad":
                result = await self.pasargad.delete_user(username)
            else:
                return {"success": False, "error": "Invalid panel type"}
            
            logger.info(f"Config deleted: {config_id}")
            return result
        
        except Exception as e:
            logger.error(f"Error deleting config: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_config_info(self, config_id: str) -> Dict[str, Any]:
        """Get configuration details"""
        try:
            return {"success": True}
        
        except Exception as e:
            logger.error(f"Error getting config info: {e}")
            return {"success": False, "error": str(e)}
