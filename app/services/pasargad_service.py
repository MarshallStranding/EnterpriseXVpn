"""Pasargad Panel API Service"""

import aiohttp
import json
from typing import Optional, Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger()


class PasargadService:
    """Pasargad Panel API Integration"""
    
    def __init__(self):
        self.url = settings.PASARGAD_URL
        self.api_key = settings.PASARGAD_API_KEY
        self.base_url = f"{self.url}/api/v1" if self.url else None
    
    async def create_user(self,
                        username: str,
                        data_limit: int,
                        expiry_time: int,
                        **kwargs) -> Dict[str, Any]:
        """Create a new user on Pasargad panel"""
        if not self.base_url:
            return {"success": False, "error": "Pasargad URL not configured"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "username": username,
                "data_limit": data_limit,
                "expiry_time": expiry_time,
                **kwargs
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/user/create",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status in [200, 201]:
                        data = await response.json()
                        logger.info(f"Pasargad user created: {username}")
                        return {"success": True, "data": data}
                    else:
                        error = await response.text()
                        logger.error(f"Pasargad error: {error}")
                        return {"success": False, "error": error}
        
        except Exception as e:
            logger.error(f"Error creating Pasargad user: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user_config(self, username: str) -> Dict[str, Any]:
        """Get user configuration link"""
        if not self.base_url:
            return {"success": False, "error": "Pasargad URL not configured"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/user/{username}/config",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"success": True, "config_url": data.get("subscribe_url")}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error getting Pasargad config: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_user(self, username: str) -> Dict[str, Any]:
        """Delete user from Pasargad panel"""
        if not self.base_url:
            return {"success": False, "error": "Pasargad URL not configured"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{self.base_url}/user/{username}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status in [200, 204]:
                        logger.info(f"Pasargad user deleted: {username}")
                        return {"success": True}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error deleting Pasargad user: {e}")
            return {"success": False, "error": str(e)}
    
    async def extend_user_expiry(self, username: str, expiry_days: int) -> Dict[str, Any]:
        """Extend user expiry"""
        if not self.base_url:
            return {"success": False, "error": "Pasargad URL not configured"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {"expiry_days": expiry_days}
            
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    f"{self.base_url}/user/{username}/extend",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Pasargad user extended: {username}")
                        return {"success": True, "data": data}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error extending Pasargad user: {e}")
            return {"success": False, "error": str(e)}
