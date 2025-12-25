"""
Equipment List Command
Sends users a link to view the equipment Google Sheet
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config

async def send_equipment_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the public Google Sheet link to view equipment"""
    
    if not config.PUBLIC_SHEET_URL:
        await update.message.reply_text(
            "📄 *Equipment List*\n\n"
            "Equipment list link not configured yet.\n"
            "Please contact an administrator.\n\n"
            "You can still rent by entering the Item ID directly using /rent",
            parse_mode='Markdown'
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("📄 Open Equipment List", url=config.PUBLIC_SHEET_URL)],
        [InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📄 *Equipment List*\n\n"
        "Click the button below to view all available equipment in Google Sheets.\n\n"
        "You can:\n"
        "• See all items and their details\n"
        "• Check quantities available\n"
        "• Find item locations\n"
        "• Search and filter easily\n\n"
        "Once you know the Item ID, come back and use /rent to rent it!",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def view_sheet_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle view sheet button from inline keyboard"""
    query = update.callback_query
    await query.answer()
    
    if not config.PUBLIC_SHEET_URL:
        await query.edit_message_text(
            "📄 *Equipment List*\n\n"
            "Equipment list link not configured yet.\n"
            "Please contact an administrator.\n\n"
            "You can still rent by entering the Item ID directly using /rent",
            parse_mode='Markdown'
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("📄 Open Equipment List", url=config.PUBLIC_SHEET_URL)],
        [InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📄 *Equipment List*\n\n"
        "Click the button below to view all available equipment in Google Sheets.\n\n"
        "You can:\n"
        "• See all items and their details\n"
        "• Check quantities available\n"
        "• Find item locations\n"
        "• Search and filter easily\n\n"
        "Once you know the Item ID, come back and use /rent to rent it!",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

