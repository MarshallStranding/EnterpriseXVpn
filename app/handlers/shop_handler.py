"""Shop Handler - Product listing and purchase"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from app.utils.logger import setup_logger
from app.messages.fa import MESSAGES_FA
from app.messages.en import MESSAGES_EN

logger = setup_logger()

# Sample products - TODO: Load from database
PRODUCTS = {
    "prod_1": {
        "name": "30 Days 10GB",
        "bandwidth": 10,
        "duration": 30,
        "price": 5.0,
        "description": "30 روز / 10 گیگابایت"
    },
    "prod_2": {
        "name": "90 Days 50GB",
        "bandwidth": 50,
        "duration": 90,
        "price": 12.0,
        "description": "90 روز / 50 گیگابایت"
    },
    "prod_3": {
        "name": "180 Days 150GB",
        "bandwidth": 150,
        "duration": 180,
        "price": 25.0,
        "description": "180 روز / 150 گیگابایت"
    },
    "prod_4": {
        "name": "365 Days 500GB",
        "bandwidth": 500,
        "duration": 365,
        "price": 50.0,
        "description": "365 روز / 500 گیگابایت"
    }
}


async def shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle shop command"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        # Create product buttons
        keyboard = []
        for prod_id, product in PRODUCTS.items():
            button_text = f"{product['name']} - ${product['price']}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"select_product_{prod_id}")])
        
        keyboard.append([InlineKeyboardButton(messages['btn_back'], callback_data='main_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query:
            await query.edit_message_text(
                text=messages['shop_select_product'],
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                messages['shop_select_product'],
                reply_markup=reply_markup
            )
        
        logger.info(f"Shop opened for user")
    
    except Exception as e:
        logger.error(f"Error in shop_handler: {e}")


async def select_product_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle product selection"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        # Extract product ID
        product_id = query.data.replace('select_product_', '')
        product = PRODUCTS.get(product_id)
        
        if not product:
            await query.answer("❌ Product not found", show_alert=True)
            return
        
        # Store selected product
        context.user_data['selected_product'] = product_id
        
        # Create product info text
        product_text = f"""
{messages['product_info'].format(
    name=product['name'],
    bandwidth=product['bandwidth'],
    duration=product['duration'],
    price=f"${product['price']}"
)}

{messages['product_confirm']}
        """
        
        keyboard = [
            [InlineKeyboardButton("✅ " + messages['btn_confirm'], callback_data=f"confirm_purchase_{product_id}"),
             InlineKeyboardButton("❌ " + messages['btn_cancel'], callback_data="shop")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=product_text,
            reply_markup=reply_markup
        )
        
        logger.info(f"Product selected: {product_id}")
    
    except Exception as e:
        logger.error(f"Error in select_product_handler: {e}")


async def confirm_purchase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle purchase confirmation"""
    try:
        query = update.callback_query
        language = context.user_data.get('language', 'fa')
        messages = MESSAGES_FA if language == 'fa' else MESSAGES_EN
        
        product_id = query.data.replace('confirm_purchase_', '')
        product = PRODUCTS.get(product_id)
        
        if not product:
            await query.answer("❌ Product not found", show_alert=True)
            return
        
        # Redirect to payment
        context.user_data['purchase_product'] = product_id
        context.user_data['purchase_amount'] = product['price']
        
        # Import payment handler
        from app.handlers.payment_handler import show_payment_methods
        await show_payment_methods(update, context)
        
        logger.info(f"Purchase confirmed for product: {product_id}")
    
    except Exception as e:
        logger.error(f"Error in confirm_purchase_handler: {e}")
