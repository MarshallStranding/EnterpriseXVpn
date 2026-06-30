"""Referral Handler - Manage referral system"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN

logger = setup_logger()


async def referral_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show referral information"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        telegram_id = str(update.effective_user.id)
        
        # TODO: Get referral data from database
        referral_code = "ABC123XYZ"
        referral_link = f"https://t.me/bot?start={referral_code}"
        referral_count = 0
        total_earned = 0.0
        
        referral_text = f"""
👥 **Referral System**

{messages['referral_code'].format(code=referral_code)}

{messages['referral_link'].format(link=referral_link)}

{messages['referral_stats'].format(count=referral_count, earned=f"${total_earned}")}

{messages['referral_commission'].format(percentage="15")}
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Copy Link", callback_data="copy_referral_link")],
            [InlineKeyboardButton(messages['referral_withdraw'], callback_data="referral_withdraw")],
            [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query:
            await query.edit_message_text(
                text=referral_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                referral_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        logger.info(f"Referral info shown for user: {telegram_id}")
    
    except Exception as e:
        logger.error(f"Error in referral_handler: {e}")


async def copy_referral_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Copy referral link"""
    try:
        query = update.callback_query
        
        await query.answer("✅ Referral link copied!", show_alert=False)
        
        logger.info("Referral link copied")
    
    except Exception as e:
        logger.error(f"Error in copy_referral_link_handler: {e}")


async def referral_withdraw_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle referral withdrawal"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        
        # TODO: Check minimum balance
        
        await query.answer("Withdrawal system coming soon!", show_alert=True)
        
        logger.info("Withdrawal requested")
    
    except Exception as e:
        logger.error(f"Error in referral_withdraw_handler: {e}")
