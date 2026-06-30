"""User Keyboards"""

from typing import List, Dict


def get_main_keyboard(language: str = "fa") -> List[List[Dict]]:
    """Get main menu keyboard"""
    if language == "fa":
        return [
            [{"text": "🛒 فروشگاه", "callback_data": "shop"}],
            [{"text": "📋 کانفیگ‌های من", "callback_data": "my_configs"}],
            [{"text": "🎁 تریال رایگان", "callback_data": "trial"}],
            [{"text": "👥 سیستم دعوت", "callback_data": "referral"}],
            [{"text": "📥 اضافه کردن اشتراک", "callback_data": "add_subscription"}],
            [{"text": "📞 پشتیبانی", "callback_data": "support"}]
        ]
    else:
        return [
            [{"text": "🛒 Shop", "callback_data": "shop"}],
            [{"text": "📋 My Configs", "callback_data": "my_configs"}],
            [{"text": "🎁 Free Trial", "callback_data": "trial"}],
            [{"text": "👥 Referral", "callback_data": "referral"}],
            [{"text": "📥 Add Subscription", "callback_data": "add_subscription"}],
            [{"text": "📞 Support", "callback_data": "support"}]
        ]


def get_payment_keyboard(language: str = "fa") -> List[List[Dict]]:
    """Get payment method keyboard"""
    if language == "fa":
        return [
            [{"text": "💰 NOWpayment", "callback_data": "pay_nowpayment"}],
            [{"text": "⭐ Telegram Pay", "callback_data": "pay_telegram"}],
            [{"text": "🏦 درگاه ایرانی", "callback_data": "pay_gateway"}],
            [{"text": "◀️ بازگشت", "callback_data": "back"}]
        ]
    else:
        return [
            [{"text": "💰 NOWpayment", "callback_data": "pay_nowpayment"}],
            [{"text": "⭐ Telegram Pay", "callback_data": "pay_telegram"}],
            [{"text": "🏦 Payment Gateway", "callback_data": "pay_gateway"}],
            [{"text": "◀️ Back", "callback_data": "back"}]
        ]


def get_back_keyboard(language: str = "fa") -> List[List[Dict]]:
    """Get back button keyboard"""
    text = "◀️ بازگشت" if language == "fa" else "◀️ Back"
    return [[{"text": text, "callback_data": "back"}]]
