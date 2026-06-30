"""Trial Handler - Free trial system"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN

logger = setup_logger()


async def trial_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show trial information"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        telegram_id = str(update.effective_user.id)
        
        # TODO: Check if user already claimed trial
        trial_claimed = False
        
        if trial_claimed:
            trial_text = messages['trial_claimed']
            keyboard = [
                [InlineKeyboardButton(messages['btn_shop'], callback_data="shop")],
                [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
            ]
        else:
            trial_text = f"{messages['trial_available']}\n\n{messages['trial_success']}"
            keyboard = [
                [InlineKeyboardButton("✅ Get Trial", callback_data="claim_trial")],
                [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query:
            await query.edit_message_text(
                text=trial_text,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                trial_text,
                reply_markup=reply_markup
            )
        
        logger.info(f"Trial info shown for user: {telegram_id}")
    
    except Exception as e:
        logger.error(f"Error in trial_handler: {e}")


async def claim_trial_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Claim free trial"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        telegram_id = str(update.effective_user.id)
        
        # TODO: Create trial config
        # trial_config = await config_service.create_config(
        #     telegram_id=telegram_id,
        #     panel_type="marzban",
        #     username=f"trial_{telegram_id}",
        #     product_name="Trial",
        #     bandwidth_gb=0.5,
        #     duration_days=1,
        #     is_trial=True
        # )
        
        trial_text = messages['trial_success']
        keyboard = [
            [InlineKeyboardButton(messages['btn_shop'], callback_data="shop")],
            [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=trial_text,
            reply_markup=reply_markup
        )
        
        logger.info(f"Trial claimed for user: {telegram_id}")
    
    except Exception as e:
        logger.error(f"Error in claim_trial_handler: {e}")
