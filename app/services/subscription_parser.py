"""Subscription Parser Service - Parse and Handle Subscription Links"""

import base64
import json
import re
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs
from app.utils.logger import setup_logger

logger = setup_logger()


class SubscriptionParser:
    """Parse subscription links from various sources"""
    
    @staticmethod
    def parse_subscription_url(url: str) -> Dict[str, Any]:
        """Parse subscription URL"""
        try:
            # Check if URL is base64 encoded
            if url.startswith("http"):
                # It's a direct URL
                return {
                    "success": True,
                    "type": "url",
                    "url": url,
                    "raw_content": url
                }
            
            # Try to decode as base64
            try:
                decoded = base64.b64decode(url).decode('utf-8')
                return {
                    "success": True,
                    "type": "base64",
                    "raw_content": decoded
                }
            except:
                pass
            
            # Return as-is if nothing else works
            return {
                "success": True,
                "type": "raw",
                "raw_content": url
            }
        
        except Exception as e:
            logger.error(f"Error parsing subscription: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def extract_configs_from_content(content: str) -> list:
        """Extract individual configs from subscription content"""
        configs = []
        
        # Extract V2ray/Vmess configs (vmess://)
        vmess_pattern = r'vmess://[a-zA-Z0-9+/=]+'
        vmess_matches = re.findall(vmess_pattern, content)
        for match in vmess_matches:
            configs.append({
                "type": "vmess",
                "url": match,
                "raw": match
            })
        
        # Extract Vless configs (vless://)
        vless_pattern = r'vless://[a-zA-Z0-9+/=@:?&#=-]+'
        vless_matches = re.findall(vless_pattern, content)
        for match in vless_matches:
            configs.append({
                "type": "vless",
                "url": match,
                "raw": match
            })
        
        # Extract Trojan configs (trojan://)
        trojan_pattern = r'trojan://[a-zA-Z0-9+/=@:?&#=-]+'
        trojan_matches = re.findall(trojan_pattern, content)
        for match in trojan_matches:
            configs.append({
                "type": "trojan",
                "url": match,
                "raw": match
            })
        
        # Extract Shadowsocks configs (ss://)
        ss_pattern = r'ss://[a-zA-Z0-9+/=@:?&#=-]+'
        ss_matches = re.findall(ss_pattern, content)
        for match in ss_matches:
            configs.append({
                "type": "ss",
                "url": match,
                "raw": match
            })
        
        return configs
    
    @staticmethod
    def get_config_hash(content: str) -> str:
        """Get hash of subscription content for comparison"""
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()
    
    @staticmethod
    def validate_subscription_link(url: str) -> bool:
        """Validate if URL looks like a subscription link"""
        try:
            # Check if it's a valid URL pattern
            if url.startswith(("http://", "https://", "vmess://", "vless://", "trojan://", "ss://")):
                return True
            
            # Try to decode as base64
            try:
                base64.b64decode(url, validate=True)
                return True
            except:
                pass
            
            return False
        
        except:
            return False
