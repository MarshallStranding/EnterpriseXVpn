"""X-UI Panel API Service"""

import aiohttp
import json
from typing import Optional, Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger()


class XUIService:
    """X-UI Panel API Integration"""
    
    def __init__(self):
        self.url = settings.XUI_URL
        self.username = settings.XUI_USERNAME
        self.password = settings.XUI_PASSWORD
        self.base_url = f"{self.url}/api" if self.url else None
        self.session_id = None
    
    async def login(self) -> Dict[str, Any]:
        """Login to X-UI panel"""
        if not self.base_url:
            return {"success": False, "error": "X-UI URL not configured"}
        
        try:
            payload = {
                "username": self.username,
                "password": self.password
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/login",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.session_id = response.cookies.get('JSESSIONID', '').value
                        logger.info("X-UI login successful")
                        return {"success": True, "session_id": self.session_id}
                    else:
                        error = await response.text()
                        logger.error(f"X-UI login failed: {error}")
                        return {"success": False, "error": error}
        
        except Exception as e:
            logger.error(f"Error logging in to X-UI: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_user(self,
                        username: str,
                        data_limit: int,
                        expiry_time: int,
                        **kwargs) -> Dict[str, Any]:
        """Create a new user on X-UI"""
        if not self.base_url:
            return {"success": False, "error": "X-UI URL not configured"}
        
        # Login if not already logged in
        if not self.session_id:
            login_result = await self.login()
            if not login_result["success"]:
                return login_result
        
        try:
            cookies = {"JSESSIONID": self.session_id}
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "username": username,
                "dataLimit": data_limit,
                "expiryTime": expiry_time * 1000,  # X-UI uses milliseconds
                **kwargs
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/user/add",
                    json=payload,
                    cookies=cookies,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"X-UI user created: {username}")
                        return {"success": True, "data": data}
                    else:
                        error = await response.text()
                        logger.error(f"X-UI error: {error}")
                        return {"success": False, "error": error}
        
        except Exception as e:
            logger.error(f"Error creating X-UI user: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user_config(self, username: str) -> Dict[str, Any]:
        """Get user configuration link"""
        if not self.base_url:
            return {"success": False, "error": "X-UI URL not configured"}
        
        try:
            # X-UI subscription URL format
            subscribe_url = f"{self.url}/api/inbound/config/{username}"
            return {"success": True, "config_url": subscribe_url}
        
        except Exception as e:
            logger.error(f"Error getting X-UI config: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_user(self, username: str) -> Dict[str, Any]:
        """Delete user from X-UI"""
        if not self.base_url:
            return {"success": False, "error": "X-UI URL not configured"}
        
        if not self.session_id:
            login_result = await self.login()
            if not login_result["success"]:
                return login_result
        
        try:
            cookies = {"JSESSIONID": self.session_id}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/user/delete/{username}",
                    cookies=cookies,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        logger.info(f"X-UI user deleted: {username}")
                        return {"success": True}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error deleting X-UI user: {e}")
            return {"success": False, "error": str(e)}
