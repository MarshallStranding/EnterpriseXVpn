"""Payment Service - Handle All Payment Operations"""

from datetime import datetime
from typing import Optional, Dict, Any
import uuid
from app.config import settings
from app.services.nowpayment_service import NOWpaymentService
from app.utils.logger import setup_logger

logger = setup_logger()


class PaymentService:
    """Payment Management Service"""
    
    def __init__(self):
        self.nowpayment = NOWpaymentService() if settings.NOWPAYMENT_ENABLED else None
    
    async def create_order(self,
                          telegram_id: str,
                          product_name: str,
                          price: float,
                          payment_method: str = "nowpayment") -> Dict[str, Any]:
        """Create payment order"""
        try:
            order_id = f"ord_{uuid.uuid4().hex[:8]}"
            
            if payment_method == "nowpayment" and self.nowpayment:
                # Create NOWpayment invoice
                invoice_result = await self.nowpayment.create_payment(
                    price_amount=price,
                    price_currency="USD",
                    pay_currency="USDT",
                    order_id=order_id
                )
                
                if not invoice_result["success"]:
                    return invoice_result
                
                return {
                    "success": True,
                    "order_id": order_id,
                    "invoice_id": invoice_result.get("invoice_id"),
                    "payment_url": invoice_result.get("invoice_url"),
                    "amount": price
                }
            
            else:
                return {"success": False, "error": "Payment method not configured"}
        
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return {"success": False, "error": str(e)}
    
    async def verify_payment(self, payment_id: str) -> Dict[str, Any]:
        """Verify payment status"""
        try:
            if self.nowpayment:
                result = await self.nowpayment.get_payment_status(payment_id)
                if result["success"]:
                    is_paid = result["status"] == "finished" or result["status"] == "confirmed"
                    return {
                        "success": True,
                        "is_paid": is_paid,
                        "status": result["status"],
                        "amount_received": result.get("amount_received")
                    }
            
            return {"success": False, "error": "Cannot verify payment"}
        
        except Exception as e:
            logger.error(f"Error verifying payment: {e}")
            return {"success": False, "error": str(e)}
    
    async def process_payment(self, order_id: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Process payment"""
        try:
            transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
            
            logger.info(f"Payment processed: {transaction_id} - Amount: {amount}")
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "status": "completed",
                "amount": amount
            }
        
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return {"success": False, "error": str(e)}
    
    async def refund_payment(self, payment_id: str, reason: str = None) -> Dict[str, Any]:
        """Refund a payment"""
        try:
            if self.nowpayment:
                result = await self.nowpayment.refund_payment(payment_id)
                if result["success"]:
                    logger.info(f"Refund requested for payment: {payment_id} - Reason: {reason}")
                    return result
            
            return {"success": False, "error": "Cannot process refund"}
        
        except Exception as e:
            logger.error(f"Error processing refund: {e}")
            return {"success": False, "error": str(e)}
