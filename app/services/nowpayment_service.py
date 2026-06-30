"""NOWpayment Service Integration"""

import aiohttp
import json
import hashlib
import hmac
from typing import Optional, Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger()


class NOWpaymentService:
    """NOWpayment Gateway Integration"""
    
    def __init__(self):
        self.api_key = settings.NOWPAYMENT_API_KEY
        self.ipn_key = settings.NOWPAYMENT_IPN_KEY
        self.base_url = "https://api.nowpayments.io/v1"
        self.currencies = settings.NOWPAYMENT_CURRENCIES.split(",")
    
    async def create_payment(self,
                           price_amount: float,
                           price_currency: str = "USD",
                           pay_currency: str = "USDT",
                           order_id: str = None,
                           customer_email: str = None,
                           ipn_callback_url: str = None) -> Dict[str, Any]:
        """Create a new payment invoice"""
        try:
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "price_amount": price_amount,
                "price_currency": price_currency,
                "pay_currency": pay_currency,
                "order_id": order_id,
                "order_description": f"Order #{order_id}",
                "ipn_callback_url": ipn_callback_url,
                "success_url": "https://yourdomain.com/payment/success",
                "cancel_url": "https://yourdomain.com/payment/cancel"
            }
            
            if customer_email:
                payload["customer_email"] = customer_email
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/invoice",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 201:
                        data = await response.json()
                        logger.info(f"NOWpayment invoice created: {order_id}")
                        return {
                            "success": True,
                            "invoice_id": data.get("id"),
                            "invoice_url": data.get("invoice_url"),
                            "pay_address": data.get("pay_address"),
                            "data": data
                        }
                    else:
                        error = await response.text()
                        logger.error(f"NOWpayment error: {error}")
                        return {"success": False, "error": error}
        
        except Exception as e:
            logger.error(f"Error creating NOWpayment invoice: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status from NOWpayment"""
        try:
            headers = {
                "x-api-key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/payment/{payment_id}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "status": data.get("payment_status"),
                            "amount_received": data.get("amount_received"),
                            "data": data
                        }
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error getting payment status: {e}")
            return {"success": False, "error": str(e)}
    
    def verify_ipn(self, data: dict, signature: str) -> bool:
        """Verify IPN callback from NOWpayment"""
        try:
            # Sort data and create JSON
            sorted_data = json.dumps(data, separators=(',', ':'), sort_keys=True)
            
            # Create HMAC signature
            expected_signature = hmac.new(
                self.ipn_key.encode(),
                sorted_data.encode(),
                hashlib.sha512
            ).hexdigest()
            
            return signature == expected_signature
        
        except Exception as e:
            logger.error(f"Error verifying IPN: {e}")
            return False
    
    async def get_currencies(self) -> Dict[str, Any]:
        """Get available currencies"""
        try:
            headers = {
                "x-api-key": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/currencies",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"success": True, "currencies": data}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error getting currencies: {e}")
            return {"success": False, "error": str(e)}
    
    async def refund_payment(self, payment_id: str) -> Dict[str, Any]:
        """Request refund for a payment"""
        try:
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {"payment_id": payment_id}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/payment/{payment_id}/refund",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status in [200, 201]:
                        data = await response.json()
                        logger.info(f"Refund requested for payment: {payment_id}")
                        return {"success": True, "data": data}
                    else:
                        return {"success": False, "error": await response.text()}
        
        except Exception as e:
            logger.error(f"Error requesting refund: {e}")
            return {"success": False, "error": str(e)}
