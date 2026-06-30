"""Admin Keyboards"""

from typing import List, Dict


def get_admin_menu_keyboard() -> List[List[Dict]]:
    """Get admin menu keyboard"""
    return [
        [{"text": "📊 آمار", "callback_data": "admin_stats"}],
        [{"text": "👥 مدیریت کاربران", "callback_data": "admin_users"}],
        [{"text": "📦 مدیریت محصولات", "callback_data": "admin_products"}],
        [{"text": "🖥️ مدیریت پنل‌ها", "callback_data": "admin_panels"}],
        [{"text": "💳 مدیریت پرداخت‌ها", "callback_data": "admin_payments"}],
        [{"text": "📢 پخش پیام", "callback_data": "admin_broadcast"}],
        [{"text": "📋 لاگ‌ها", "callback_data": "admin_logs"}],
        [{"text": "🔧 وضعیت سیستم", "callback_data": "admin_health"}],
        [{"text": "📥 صادر کردن", "callback_data": "admin_export"}],
        [{"text": "◀️ بازگشت", "callback_data": "back"}]
    ]


def get_user_management_keyboard() -> List[List[Dict]]:
    """Get user management keyboard"""
    return [
        [{"text": "👁️ مشاهده کاربران", "callback_data": "users_list"}],
        [{"text": "🔍 جستجو", "callback_data": "users_search"}],
        [{"text": "⛔ انسداد", "callback_data": "users_ban"}],
        [{"text": "✅ رفع انسداد", "callback_data": "users_unban"}],
        [{"text": "📝 ارسال پیام", "callback_data": "users_message"}],
        [{"text": "◀️ بازگشت", "callback_data": "admin_menu"}]
    ]
