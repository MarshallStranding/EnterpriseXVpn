"""Subscription Service - Handle Imported Subscriptions"""

from typing import Optional, Dict, Any
import hashlib
import aiohttp
from app.services.subscription_parser import SubscriptionParser
from app.utils.logger import setup_logger

logger = setup_logger()


class SubscriptionService:
    """Subscription Management Service"""
    
    def __init__(self):
        self.parser = SubscriptionParser()
    
    async def import_subscription(self, telegram_id: str, subscription_link: str) -> Dict[str, Any]:
        """Import subscription link from external source"""
        try:
            # Validate subscription link
            if not self.parser.validate_subscription_link(subscription_link):
                return {"success": False, "error": "Invalid subscription link"}
            
            # Parse subscription
            parse_result = self.parser.parse_subscription_url(subscription_link)
            if not parse_result["success"]:
                return parse_result
            
            # Get hash of subscription
            link_hash = self.parser.get_config_hash(subscription_link)
            
            # Extract configs
            configs = self.parser.extract_configs_from_content(parse_result["raw_content"])
            
            logger.info(f"Subscription imported for user {telegram_id}: {len(configs)} configs found")
            
            return {
                "success": True,
                "subscription_link": subscription_link,
                "link_hash": link_hash,
                "configs_found": len(configs),
                "configs": configs
            }
        
        except Exception as e:
            logger.error(f"Error importing subscription: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_subscription(self, subscription_id: str, subscription_link: str) -> Dict[str, Any]:
        """Update subscription content"""
        try:
            parse_result = self.parser.parse_subscription_url(subscription_link)
            if not parse_result["success"]:
                return parse_result
            
            configs = self.parser.extract_configs_from_content(parse_result["raw_content"])
            
            logger.info(f"Subscription updated: {subscription_id}")
            
            return {
                "success": True,
                "configs_found": len(configs),
                "configs": configs
            }
        
        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Delete subscription"""
        try:
            logger.info(f"Subscription deleted: {subscription_id}")
            return {"success": True}
        
        except Exception as e:
            logger.error(f"Error deleting subscription: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_subscription_list(self, telegram_id: str) -> Dict[str, Any]:
        """Get all subscriptions for user"""
        try:
            return {
                "success": True,
                "subscriptions": []
            }
        
        except Exception as e:
            logger.error(f"Error getting subscription list: {e}")
            return {"success": False, "error": str(e)}
