"""User Configs Handler - Manage user VPN configurations"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN
from app.utils.helpers import Helpers

logger = setup_logger()


async def my_configs_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's VPN configs"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        telegram_id = str(update.effective_user.id)
        
        # TODO: Get user configs from database
        user_configs = []
        
        if not user_configs:
            keyboard = [
                [InlineKeyboardButton(messages['btn_shop'], callback_data="shop")],
                [InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if query:
                await query.edit_message_text(
                    text=messages['no_configs'],
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(
                    messages['no_configs'],
                    reply_markup=reply_markup
                )
            return
        
        # Show configs
        config_text = messages['configs_title'] + "\n\n"
        keyboard = []
        
        for idx, config in enumerate(user_configs, 1):
            config_text += f"{idx}. {config['name']}\n"
            config_text += f"   مصرف: {config['used']}/{config['total']} GB\n"
            config_text += f"   انقضا: {config['expires']}\n\n"
            
            keyboard.append([
                InlineKeyboardButton(f"📋 {idx}", callback_data=f"config_details_{config['id']}"),
                InlineKeyboardButton("🔄", callback_data=f"config_renew_{config['id']}"),
                InlineKeyboardButton("🗑️", callback_data=f"config_delete_{config['id']}")
            ])
        
        keyboard.append([InlineKeyboardButton(messages['btn_back'], callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query:
            await query.edit_message_text(
                text=config_text,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                config_text,
                reply_markup=reply_markup
            )
        
        logger.info(f"My configs shown for user: {telegram_id}")
    
    except Exception as e:
        logger.error(f"Error in my_configs_handler: {e}")


async def config_details_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show config details"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        config_id = query.data.replace('config_details_', '')
        
        # TODO: Get config details from database
        config = {
            "id": config_id,
            "name": "30 Days 10GB",
            "subscription_link": "vmess://...",
            "expires": "5 days",
            "status": "Active"
        }
        
        detail_text = f"""
📋 **Config Details**

Name: {config['name']}
Status: {config['status']}
Expires: {config['expires']}

📋 Subscription Link:
`{config['subscription_link']}`
        """
        
        keyboard = [
            [InlineKeyboardButton(messages['copy_config'], callback_data=f"copy_config_{config_id}")],
            [InlineKeyboardButton(messages['renew_config'], callback_data=f"config_renew_{config_id}"),
             InlineKeyboardButton(messages['delete_config'], callback_data=f"config_delete_{config_id}")],
            [InlineKeyboardButton(messages['btn_back'], callback_data="my_configs")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=detail_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        logger.info(f"Config details shown: {config_id}")
    
    except Exception as e:
        logger.error(f"Error in config_details_handler: {e}")


async def copy_config_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Copy config to clipboard"""
    try:
        query = update.callback_query
        
        config_id = query.data.replace('copy_config_', '')
        
        # TODO: Get config from database
        config_link = "vmess://..."
        
        await query.answer("✅ Config copied to clipboard!", show_alert=False)
        
        logger.info(f"Config copied: {config_id}")
    
    except Exception as e:
        logger.error(f"Error in copy_config_handler: {e}")


async def renew_config_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle config renewal"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        config_id = query.data.replace('config_renew_', '')
        context.user_data['renew_config_id'] = config_id
        
        # TODO: Show renewal options
        renewal_text = "Select renewal period:"
        keyboard = [
            [InlineKeyboardButton("30 Days - $5", callback_data="renew_30_5")],
            [InlineKeyboardButton("90 Days - $12", callback_data="renew_90_12")],
            [InlineKeyboardButton("180 Days - $25", callback_data="renew_180_25")],
            [InlineKeyboardButton("365 Days - $50", callback_data="renew_365_50")],
            [InlineKeyboardButton(messages['btn_back'], callback_data="my_configs")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=renewal_text,
            reply_markup=reply_markup
        )
        
        logger.info(f"Config renewal initiated: {config_id}")
    
    except Exception as e:
        logger.error(f"Error in renew_config_handler: {e}")


async def delete_config_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle config deletion"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        config_id = query.data.replace('config_delete_', '')
        
        confirm_text = "آیا مطمئن هستید؟ این کاتفیگ حذف می‌شود."
        keyboard = [
            [InlineKeyboardButton("✅ بله", callback_data=f"confirm_delete_{config_id}"),
             InlineKeyboardButton("❌ خیر", callback_data="my_configs")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=confirm_text,
            reply_markup=reply_markup
        )
        
        logger.info(f"Config deletion initiated: {config_id}")
    
    except Exception as e:
        logger.error(f"Error in delete_config_handler: {e}")


async def confirm_delete_config_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm config deletion"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        config_id = query.data.replace('confirm_delete_', '')
        
        # TODO: Delete config from database and panel
        
        await query.answer("✅ Config deleted!", show_alert=True)
        await my_configs_handler(update, context)
        
        logger.info(f"Config deleted: {config_id}")
    
    except Exception as e:
        logger.error(f"Error in confirm_delete_config_handler: {e}")
