#!/usr/bin/env python3
"""EnterpriseXVpn Bot - Main Handler"""

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger()

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher()


async def process_update(update: Update):
    """Process incoming updates"""
    try:
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error(f"Error processing update: {e}")


async def on_startup():
    """Called when bot starts"""
    try:
        logger.info("🚀 Bot startup")
        # Initialize database
        # await init_db()
        # Register handlers
        # register_handlers(dp)
    except Exception as e:
        logger.error(f"Startup error: {e}")


async def on_shutdown():
    """Called when bot stops"""
    try:
        logger.info("⛔ Bot shutdown")
        await bot.session.close()
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
