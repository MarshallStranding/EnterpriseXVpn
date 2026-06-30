#!/usr/bin/env python3
"""EnterpriseXVpn Bot - Payment Handlers"""

from aiogram import Router, types, F
from app.utils.logger import setup_logger
from app.services.payment_service import PaymentService

logger = setup_logger()
router = Router()

payment_service = PaymentService()


@router.callback_query(F.data.startswith("buy_"))
async def buy_product_callback(query: types.CallbackQuery):
    """Handle product purchase"""
    try:
        product_id = query.data.replace("buy_", "")
        
        # TODO: Get product details from database
        product_price = 50000
        product_name = "30 روزه"
        
        text = f"""
✅ تأیید سفارش:

📦 محصول: {product_name}
💰 قیمت: {product_price:,} تومان

آیا می‌خواهید ادامه دهید؟
        """
        
        keyboard = [
            [types.InlineKeyboardButton(text="✅ ادامه", callback_data=f"confirm_buy_{product_id}")],
            [types.InlineKeyboardButton(text="← بازگشت", callback_data="shop")]
        ]
        
        await query.message.edit_text(
            text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in buy product: {e}")
        await query.answer("❌ خطا رخ داد", show_alert=True)


@router.callback_query(F.data.startswith("confirm_buy_"))
async def confirm_buy_callback(query: types.CallbackQuery):
    """Handle payment confirmation"""
    try:
        product_id = query.data.replace("confirm_buy_", "")
        
        # Create payment order
        order_result = await payment_service.create_order(
            telegram_id=str(query.from_user.id),
            product_name="30 روزه",
            price=50000,
            payment_method="nowpayment"
        )
        
        if order_result["success"]:
            payment_url = order_result.get("payment_url")
            order_id = order_result.get("order_id")
            
            text = f"""
💳 انتخاب روش پرداخت:

سفارش: {order_id}
مبلغ: 50,000 تومان
            """
            
            keyboard = [
                [types.InlineKeyboardButton(text="🪙 NOWpayment", url=payment_url)],
                [types.InlineKeyboardButton(text="← بازگشت", callback_data="shop")]
            ]
            
            await query.message.edit_text(
                text,
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
            )
        else:
            await query.answer("❌ خطا در ایجاد سفارش", show_alert=True)
    
    except Exception as e:
        logger.error(f"Error in confirm buy: {e}")
        await query.answer("❌ خطا رخ داد", show_alert=True)
