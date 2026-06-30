#!/usr/bin/env python3
"""EnterpriseXVpn Bot - User Handlers"""

from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN
from app.keyboards.user_kb import get_main_keyboard, get_back_keyboard
from app.services.config_service import ConfigService
from app.services.subscription_service import SubscriptionService
from app.services.payment_service import PaymentService

logger = setup_logger()
router = Router()

config_service = ConfigService()
subscription_service = SubscriptionService()
payment_service = PaymentService()


@router.callback_query(F.data == "shop")
async def shop_callback(query: CallbackQuery):
    """Handle shop callback"""
    try:
        language = "fa"  # Get from user preferences
        messages = MESSAGES_FA if language == "fa" else MESSAGES_EN
        
        # TODO: Get products from database
        products = [
            {"id": "1", "name": "30 روزه", "duration": 30, "bandwidth": 100, "price": 50000},
            {"id": "2", "name": "90 روزه", "duration": 90, "bandwidth": 300, "price": 120000},
        ]
        
        keyboard = []
        for product in products:
            keyboard.append([
                types.InlineKeyboardButton(
                    text=f"{product['name']} - {product['price']:,}",
                    callback_data=f"buy_{product['id']}"
                )
            ])
        keyboard.append([types.InlineKeyboardButton(text="← بازگشت", callback_data="back")])
        
        await query.message.edit_text(
            messages["shop_title"],
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in shop: {e}")
        await query.answer("❌ خطا رخ داد", show_alert=True)


@router.callback_query(F.data == "my_configs")
async def my_configs_callback(query: CallbackQuery):
    """Handle my configs callback"""
    try:
        language = "fa"
        messages = MESSAGES_FA if language == "fa" else MESSAGES_EN
        
        # TODO: Get user configs from database
        text = messages["no_configs"]
        keyboard = [[types.InlineKeyboardButton(text="← بازگشت", callback_data="back")]]
        
        await query.message.edit_text(
            text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in my_configs: {e}")
        await query.answer("❌ خطا رخ داد", show_alert=True)


@router.callback_query(F.data == "trial")
async def trial_callback(query: CallbackQuery):
    """Handle trial callback"""
    try:
        language = "fa"
        messages = MESSAGES_FA if language == "fa" else MESSAGES_EN
        
        # TODO: Check if user already claimed trial
        text = messages["trial_available"]
        keyboard = [
            [types.InlineKeyboardButton(text="✅ دریافت تریال", callback_data="claim_trial")],
            [types.InlineKeyboardButton(text="← بازگشت", callback_data="back")]
        ]
        
        await query.message.edit_text(
            text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in trial: {e}")
        await query.answer("❌ خطا رخ داد", show_alert=True)


@router.callback_query(F.data == "referral")
async def referral_callback(query: CallbackQuery):
    """Handle referral callback"""
    try:
        language = "fa"
        messages = MESSAGES_FA if language == "fa" else MESSAGES_EN
        telegram_id = str(query.from_user.id)
        
        # TODO: Get referral info from database
        text = messages["referral_title"]
        keyboard = [[types.InlineKeyboardButton(text="← بازگشت", callback_data="back")]]
        
        await query.message.edit_text(
            text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in referral: {e}")
        await query.answer("❌ خطا رخ داد", show_alert=True)


@router.callback_query(F.data == "add_subscription")
async def add_subscription_callback(query: CallbackQuery):
    """Handle add subscription callback"""
    try:
        language = "fa"
        messages = MESSAGES_FA if language == "fa" else MESSAGES_EN
        
        text = messages["paste_link"]
        keyboard = [[types.InlineKeyboardButton(text="← بازگشت", callback_data="back")]]
        
        await query.message.edit_text(
            text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in add_subscription: {e}")
        await query.answer("❌ خطا رخ داد", show_alert=True)


@router.callback_query(F.data == "support")
async def support_callback(query: CallbackQuery):
    """Handle support callback"""
    try:
        language = "fa"
        messages = MESSAGES_FA if language == "fa" else MESSAGES_EN
        
        text = messages["support_text"]
        keyboard = [[types.InlineKeyboardButton(text="← بازگشت", callback_data="back")]]
        
        await query.message.edit_text(
            text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in support: {e}")
        await query.answer("❌ خطا رخ داد", show_alert=True)


@router.callback_query(F.data == "back")
async def back_callback(query: CallbackQuery):
    """Handle back callback"""
    try:
        language = "fa"
        messages = MESSAGES_FA if language == "fa" else MESSAGES_EN
        keyboard = get_main_keyboard(language)
        
        await query.message.edit_text(
            f"{messages['start_welcome']}\n\n{messages['start_text']}",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    
    except Exception as e:
        logger.error(f"Error in back: {e}")
