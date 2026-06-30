"""Subscription Handler - Import external subscriptions"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN
from app.services.subscription_service import SubscriptionService

logger = setup_logger()
subscription_service = SubscriptionService()

# Conversation states
AWAITING_LINK = 1


async def add_subscription_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start subscription import process"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        text = f"{messages['add_subscription']}\n\n{messages['paste_link']}"
        
        await query.edit_message_text(text=text)
        
        logger.info("Add subscription started")
        return AWAITING_LINK
    
    except Exception as e:
        logger.error(f"Error in add_subscription_handler: {e}")


async def process_subscription_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process subscription link"""
    try:
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        subscription_link = update.message.text
        telegram_id = str(update.effective_user.id)
        
        # Import subscription
        result = await subscription_service.import_subscription(
            telegram_id=telegram_id,
            subscription_link=subscription_link
        )
        
        if result['success']:
            response_text = messages['subscription_added'].format(count=result['configs_found'])
            
            # TODO: Save subscription to database
            
            logger.info(f"Subscription imported: {telegram_id} - {result['configs_found']} configs")
        else:
            response_text = messages['invalid_link']
            logger.warning(f"Invalid subscription link from {telegram_id}")
        
        keyboard = [
            [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response_text,
            reply_markup=reply_markup
        )
        
        return ConversationHandler.END
    
    except Exception as e:
        logger.error(f"Error in process_subscription_link: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")
        return ConversationHandler.END


async def cancel_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel subscription import"""
    try:
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        keyboard = [
            [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            messages['btn_cancel'],
            reply_markup=reply_markup
        )
        
        return ConversationHandler.END
    
    except Exception as e:
        logger.error(f"Error in cancel_subscription: {e}")
