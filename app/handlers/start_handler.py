#!/usr/bin/env python3
"""EnterpriseXVpn Bot - Start Handler"""

from aiogram import Router, types
from aiogram.filters import CommandStart
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN
from app.keyboards.user_kb import get_main_keyboard
from app.services.user_service import UserService

logger = setup_logger()
router = Router()

user_service = UserService()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handle /start command"""
    try:
        telegram_id = str(message.from_user.id)
        username = message.from_user.username
        language = "fa"  # Default to Farsi
        
        # Get messages based on language
        messages = MESSAGES_FA if language == "fa" else MESSAGES_EN
        
        # Create user if not exists
        # await user_service.create_user(telegram_id, username, language=language)
        
        # Send welcome message
        keyboard = get_main_keyboard(language)
        
        await message.answer(
            f"{messages['start_welcome']}\n\n{messages['start_text']}",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
        
        logger.info(f"User started bot: {telegram_id}")
    
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await message.answer("❌ An error occurred. Please try again.")
