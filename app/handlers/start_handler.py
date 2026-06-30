"""Start Handler - Bot initialization and main menu"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN
from app.keyboards.user_kb import get_main_keyboard

logger = setup_logger()


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    try:
        user = update.effective_user
        telegram_id = str(user.id)
        username = user.username or user.first_name
        
        # Get language (default: fa)
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        # TODO: Save/get user from database
        
        welcome_text = f"{messages['start_welcome']}\n\n{messages['start_text']}"
        
        keyboard = get_main_keyboard(language)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup
        )
        
        logger.info(f"User started bot: {telegram_id} - {username}")
    
    except Exception as e:
        logger.error(f"Error in start_handler: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    try:
        language = context.user_data.get('language', 'fa')
        
        help_text = "📖 **Help & FAQ**\n\n"
        if language == 'fa':
            help_text += """
🛍️ **فروشگاه**: می‌تونید کاتفیگ‌های مختلف رو خریداری کنید
💾 **کاتفیگ‌های من**: تمام کاتفیگ‌های شما رو مشاهده کنید
🎁 **تریال رایگان**: 24 ساعت رایگان امتحان کنید
👥 **سیستم دعوت**: دوستان رو دعوت کنید و درآمد بسازید
📥 **اضافه کردن اشتراک**: اشتراک از جاهای دیگه رو اضافه کنید
🎧 **پشتیبانی**: اگه مشکلی داشتید، ما کمکتون می‌کنیم
            """
        else:
            help_text += """
🛍️ **Shop**: Buy different configs
💾 **My Configs**: View all your configs
🎁 **Free Trial**: Try for 24 hours free
👥 **Referral**: Invite friends and earn
📥 **Add Subscription**: Import configs from elsewhere
🎧 **Support**: Get help if you need
            """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    except Exception as e:
        logger.error(f"Error in help_handler: {e}")


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    try:
        language = context.user_data.get('language', 'fa')
        
        if language == 'fa':
            about_text = """
🤖 **EnterpriseXVpn Bot v1.0**

یک ربات حرفه‌ای برای فروش خودکار کاتفیگ‌های VPN

✨ **امکانات**:
• فروش خودکار و فوری
• اتصال به چند پنل (Marzban, X-UI, Pasargad)
• سیستم رفرال و کمیسیون
• درگاه‌های پرداخت متعدد
• اضافه کردن اشتراک‌های خارجی
• پنل ادمین کامل
• آنالیتیکس و گزارشات

📧 **تماس**: @support
🌐 **وب‌سایت**: https://example.com
            """
        else:
            about_text = """
🤖 **EnterpriseXVpn Bot v1.0**

A professional bot for automated VPN config selling

✨ **Features**:
• Automatic instant selling
• Multi-panel support (Marzban, X-UI, Pasargad)
• Referral & commission system
• Multiple payment gateways
• Import external subscriptions
• Full admin panel
• Analytics & reporting

📧 **Contact**: @support
🌐 **Website**: https://example.com
            """
        
        await update.message.reply_text(about_text, parse_mode='Markdown')
    
    except Exception as e:
        logger.error(f"Error in about_handler: {e}")
