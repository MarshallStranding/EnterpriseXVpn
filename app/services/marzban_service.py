"""Marzban Panel API Service"""

import aiohttp
import json
from typing import Optional, Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger()


class MarzbanService:
    """Marzban Panel API Integration"""
    
    def __init__(self):
        self.url = settings.MARZBAN_URL
        self.api_key = settings.MARZBAN_API_KEY
        self.base_url = f"{self.url}/api" if self.url else None
    
    async def create_user(self,
                        username: str,
                        data_limit: int,
                        expiry_time: int,
                        **kwargs) -> Dict[str, Any]:
        """Create a new user on Marzban"""
        if not self.base_url:
            return {"success": False, "error": "Marzban URL not configured"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "username": username,
                "data_limit": data_limit,
                "expire": expiry_time,
                **kwargs
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/users",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status in [200, 201]:
                        data = await response.json()
                        logger.info(f"Marzban user created: {username}")
                        return {"success": True, "data": data}
                    else:
                        error = await response.text()
                        logger.error(f"Marzban error: {error}")
                        return {"success": False, "error": error}
        
        except Exception as e:
            logger.error(f"Error creating Marzban user: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user_config(self, username: str) -> Dict[str, Any]:
        """Get user subscription link from Marzban"""
        if not self.base_url:
            return {"success": False, "error": "Marzban URL not configured"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/users/{username}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Marzban returns subscription URL in the response
                        subscribe_url = f"{self.url}/api/user_subscription/{username}"
                        return {"success": True, "config_url": subscribe_url}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error getting Marzban config: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_user(self, username: str) -> Dict[str, Any]:
        """Delete user from Marzban"""
        if not self.base_url:
            return {"success": False, "error": "Marzban URL not configured"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{self.base_url}/users/{username}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status in [200, 204]:
                        logger.info(f"Marzban user deleted: {username}")
                        return {"success": True}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error deleting Marzban user: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get panel statistics"""
        if not self.base_url:
            return {"success": False, "error": "Marzban URL not configured"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/system/stats",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"success": True, "stats": data}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error getting Marzban stats: {e}")
            return {"success": False, "error": str(e)}
