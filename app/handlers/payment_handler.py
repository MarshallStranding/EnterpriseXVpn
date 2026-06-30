"""Payment Handler - Handle all payment operations"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN
from app.services.payment_service import PaymentService

logger = setup_logger()
payment_service = PaymentService()


async def show_payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show payment method selection"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        keyboard = [
            [InlineKeyboardButton(messages['payment_nowpayment'], callback_data="pay_nowpayment")],
            [InlineKeyboardButton(messages['payment_telegram'], callback_data="pay_telegram")],
            [InlineKeyboardButton(messages['payment_gateway'], callback_data="pay_gateway")],
            [InlineKeyboardButton(messages['btn_back'], callback_data="shop")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query:
            await query.edit_message_text(
                text=messages['payment_method'],
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                messages['payment_method'],
                reply_markup=reply_markup
            )
        
        logger.info("Payment methods shown")
    
    except Exception as e:
        logger.error(f"Error in show_payment_methods: {e}")


async def pay_nowpayment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle NOWpayment payment"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        amount = context.user_data.get('purchase_amount', 0)
        product_id = context.user_data.get('purchase_product')
        
        if not amount or not product_id:
            await query.answer("❌ Invalid purchase", show_alert=True)
            return
        
        await query.edit_message_text(text=messages['payment_creating'])
        
        # Create payment order
        result = await payment_service.create_order(
            telegram_id=str(update.effective_user.id),
            product_name=product_id,
            price=amount,
            payment_method="nowpayment"
        )
        
        if result['success']:
            payment_url = result.get('payment_url')
            order_id = result.get('order_id')
            
            keyboard = [
                [InlineKeyboardButton("💳 Pay Now", url=payment_url)],
                [InlineKeyboardButton(messages['btn_back'], callback_data="shop")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            payment_text = f"{messages['payment_success'].format(order_id=order_id)}\n\n💳 Click 'Pay Now' to complete payment"
            
            await query.edit_message_text(
                text=payment_text,
                reply_markup=reply_markup
            )
            
            logger.info(f"NOWpayment order created: {order_id}")
        else:
            await query.edit_message_text(text=messages['payment_failed'])
            logger.error(f"Payment creation failed: {result.get('error')}")
    
    except Exception as e:
        logger.error(f"Error in pay_nowpayment_handler: {e}")


async def pay_telegram_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Telegram Payments"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        await query.answer("Telegram Payments coming soon!", show_alert=True)
        logger.info("Telegram payment requested")
    
    except Exception as e:
        logger.error(f"Error in pay_telegram_handler: {e}")


async def pay_gateway_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Iranian Gateway Payment"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        await query.answer("Gateway payment coming soon!", show_alert=True)
        logger.info("Gateway payment requested")
    
    except Exception as e:
        logger.error(f"Error in pay_gateway_handler: {e}")
