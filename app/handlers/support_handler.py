"""Support Handler - Customer support"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN

logger = setup_logger()

# Conversation states
AWAITING_MESSAGE = 1


async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show support menu"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        text = f"{messages['support_title']}\n\n{messages['support_text']}"
        
        keyboard = [
            [InlineKeyboardButton("📞 Send Message", callback_data="send_support_message")],
            [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query:
            await query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                text=text,
                reply_markup=reply_markup
            )
        
        logger.info("Support menu shown")
    
    except Exception as e:
        logger.error(f"Error in support_handler: {e}")


async def send_support_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start support message process"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        text = f"Please type your message:"
        
        await query.edit_message_text(text=text)
        
        logger.info("Support message input started")
        return AWAITING_MESSAGE
    
    except Exception as e:
        logger.error(f"Error in send_support_message_handler: {e}")


async def process_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process support message"""
    try:
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        message_text = update.message.text
        telegram_id = str(update.effective_user.id)
        
        # TODO: Save support ticket to database
        # TODO: Forward to support team
        
        response_text = messages['support_sent']
        
        keyboard = [
            [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response_text,
            reply_markup=reply_markup
        )
        
        logger.info(f"Support message received from {telegram_id}")
        
        return ConversationHandler.END
    
    except Exception as e:
        logger.error(f"Error in process_support_message: {e}")
        return ConversationHandler.END


async def cancel_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel support"""
    try:
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        keyboard = [
            [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Support cancelled",
            reply_markup=reply_markup
        )
        
        return ConversationHandler.END
    
    except Exception as e:
        logger.error(f"Error in cancel_support: {e}")
