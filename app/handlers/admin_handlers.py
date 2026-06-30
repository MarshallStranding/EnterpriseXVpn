#!/usr/bin/env python3
"""EnterpriseXVpn Bot - Admin Handlers"""

from aiogram import Router, types, F
from aiogram.filters import Command
from app.utils.logger import setup_logger
from app.config import settings
from app.messages.fa import MESSAGES_FA
from app.services.admin_service import AdminService
from app.keyboards.admin_kb import get_admin_menu_keyboard

logger = setup_logger()
router = Router()

admin_service = AdminService()


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == settings.TELEGRAM_ADMIN_ID


@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Handle /admin command"""
    try:
        if not is_admin(message.from_user.id):
            await message.answer("❌ دسترسی رد شد!")
            logger.warning(f"Unauthorized admin access attempt: {message.from_user.id}")
            return
        
        keyboard = get_admin_menu_keyboard()
        await message.answer(
            MESSAGES_FA["admin_title"],
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in admin command: {e}")
        await message.answer("❌ خطا رخ داد")


@router.callback_query(F.data == "admin_stats")
async def admin_stats_callback(query: types.CallbackQuery):
    """Handle admin stats callback"""
    try:
        if not is_admin(query.from_user.id):
            await query.answer("❌ دسترسی رد شد!", show_alert=True)
            return
        
        # Get stats
        stats_result = await admin_service.get_dashboard_stats()
        stats = stats_result.get("stats", {})
        
        text = f"""
📊 آمار کل:

👥 کاربران: {stats.get('total_users', 0)}
📦 سفارشات: {stats.get('total_orders', 0)}
💰 درآمد: {stats.get('total_revenue', 0):,} تومان
🎯 کانفیگ‌های فعال: {stats.get('active_configs', 0)}

امروز:
📈 درآمد امروز: {stats.get('today_revenue', 0):,} تومان
📦 سفارشات امروز: {stats.get('today_orders', 0)}
        """
        
        keyboard = get_admin_menu_keyboard()
        await query.message.edit_text(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))
    
    except Exception as e:
        logger.error(f"Error in admin stats: {e}")
        await query.answer(f"❌ خطا: {str(e)[:50]}", show_alert=True)


@router.callback_query(F.data == "admin_users")
async def admin_users_callback(query: types.CallbackQuery):
    """Handle admin users management"""
    try:
        if not is_admin(query.from_user.id):
            await query.answer("❌ دسترسی رد شد!", show_alert=True)
            return
        
        text = "🔧 مدیریت کاربران\n\nبرای جستجو ID کاربر را وارد کنید:"
        keyboard = [[types.InlineKeyboardButton(text="← بازگشت", callback_data="admin_menu")]]
        
        await query.message.edit_text(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))
    
    except Exception as e:
        logger.error(f"Error in admin users: {e}")
        await query.answer(f"❌ خطا: {str(e)[:50]}", show_alert=True)
