"""
Enhanced Telegram Bot with Inline Keyboards and Admin Features
Handles all user interactions and commands with improved UX
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)
from datetime import datetime, timedelta
import pytz
import config
from sheets_manager import SheetsManager
from admin_commands import is_admin
from ux_improvements import (
    browse_items, show_category_items, browse_back, 
    browse_cancel, start_rent_from_browse
)

# Conversation states
WAITING_FOR_ITEM_ID = 1
WAITING_FOR_DURATION = 2
WAITING_FOR_DURATION_CUSTOM = 3
WAITING_FOR_PICKUP_PHOTO = 4
WAITING_FOR_RETURN_CHOICE = 5
WAITING_FOR_RETURN_PHOTO = 6

# Initialize Sheets Manager
sheets = SheetsManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    
    # Create inline keyboard for main menu
    keyboard = [
        [InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")],
        [InlineKeyboardButton("📋 My Rentals", callback_data="main_myrentals")],
        [InlineKeyboardButton("📄 View Equipment List", callback_data="view_sheet")],
        [InlineKeyboardButton("📖 Help", callback_data="main_help")]
    ]
    
    # Add admin button if user is admin
    if is_admin(user.id):
        keyboard.append([InlineKeyboardButton("🔧 Admin Panel", callback_data="main_admin")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
🙏 *Welcome to Church Tech Ministry Equipment Rental Bot!*

Hello {user.first_name}! 👋

Use the buttons below to get started, or try these commands:

📋 *Quick Commands:*
/rent - Rent equipment (enter Item ID)
/list - View all available equipment
/myrentals - View your active rentals
/return - Return equipment early
/help - Get help
    """
    
    if is_admin(user.id):
        welcome_message += "\n🔧 /admin - Admin control panel"
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
📖 *How to Use This Bot*

*Renting Equipment:*
1️⃣ Use /list to view all available equipment
2️⃣ Note the Item ID you want (e.g., CAB001)
3️⃣ Use /rent and enter the Item ID
4️⃣ Choose rental duration
5️⃣ Take a photo of the item you're picking up
6️⃣ Done! Equipment is yours!

*Returning Equipment:*
1️⃣ Use /return command
2️⃣ Select which item to return
3️⃣ Take a photo of the returned item
4️⃣ Done!

*Other Commands:*
• /list - View equipment list (Google Sheet)
• /myrentals - See your active rentals
• /help - Show this help message

📅 You'll receive a reminder 1 day before your return date!

Need assistance? Contact your tech ministry leader! 🙏
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def rent_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the rental process"""
    keyboard = []
    
    # Add equipment list button if URL is configured
    if config.PUBLIC_SHEET_URL:
        keyboard.append([InlineKeyboardButton("📄 View Equipment List", url=config.PUBLIC_SHEET_URL)])
    
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="rent_cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = "🎯 *Let's rent some equipment!*\n\n"
    
    if config.PUBLIC_SHEET_URL:
        message += "📄 Click the button below to view all available equipment.\n\n"
    
    message += "📝 *Please enter the Item ID* you want to rent (e.g., CAB001, MIC001)\n\n"
    message += "Type /cancel to cancel this operation."
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    
    return WAITING_FOR_ITEM_ID

async def rent_browse_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle browse button in rent flow"""
    query = update.callback_query
    await query.answer()
    
    # Redirect to browse functionality
    await browse_items_inline(query, context)
    return WAITING_FOR_ITEM_ID

async def browse_items_inline(query, context):
    """Browse items inline (for callback)"""
    try:
        all_items = sheets.inventory_sheet.get_all_records()
        
        if not all_items:
            await query.edit_message_text("❌ No items found in inventory.")
            return
        
        # Get unique categories
        categories = {}
        for item in all_items:
            item_type = item.get('Type', 'Other')
            if item_type not in categories:
                categories[item_type] = []
            categories[item_type].append(item)
        
        # Create keyboard with categories
        keyboard = []
        category_emojis = {
            'Cable': '🔌',
            'Microphone': '🎤',
            'Camera': '🎥',
            'Lighting': '💡',
            'Stand': '🎚️',
            'Adapter': '🔄',
            'Monitor': '📺',
            'Recorder': '⏺️',
            'Mixer': '🎛️',
            'Other': '📦'
        }
        
        for category in sorted(categories.keys()):
            emoji = category_emojis.get(category, '📦')
            count = len(categories[category])
            keyboard.append([
                InlineKeyboardButton(
                    f"{emoji} {category} ({count})",
                    callback_data=f"browse_category_{category}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="rent_cancel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📦 *Browse Equipment*\n\n"
            "Select a category to view available items:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    except Exception as e:
        await query.edit_message_text(f"❌ Error loading items: {e}")

async def rent_manual_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle manual Item ID entry"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔍 *Enter Item ID*\n\n"
        "Please type the Item ID (e.g., CAB001, MIC001)\n\n"
        "Type /cancel to cancel this operation.",
        parse_mode='Markdown'
    )
    
    return WAITING_FOR_ITEM_ID

async def receive_item_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the item ID provided by user"""
    item_id = update.message.text.strip().upper()
    
    # Check availability
    available, quantity, item = sheets.check_availability(item_id)
    
    if not item:
        await update.message.reply_text(
            f"❌ Item ID `{item_id}` not found in our inventory.\n\n"
            "Please check the Item ID and try again, or type /cancel to cancel.",
            parse_mode='Markdown'
        )
        return WAITING_FOR_ITEM_ID
    
    if not available:
        await update.message.reply_text(
            f"❌ Sorry, *{item.get('Item Name')}* (ID: `{item_id}`) is currently not available.\n\n"
            f"All units are currently rented out. Please try again later or choose a different item.\n\n"
            "Type /cancel to cancel this operation.",
            parse_mode='Markdown'
        )
        return WAITING_FOR_ITEM_ID
    
    # Store item details in context
    context.user_data['rental_item_id'] = item_id
    context.user_data['rental_item_name'] = item.get('Item Name')
    context.user_data['rental_item_type'] = item.get('Type')
    context.user_data['rental_item_brand'] = item.get('Brand')
    context.user_data['rental_item_model'] = item.get('Model')
    context.user_data['rental_item_location'] = item.get('Location')
    
    # Create duration selection keyboard
    keyboard = [
        [
            InlineKeyboardButton("1 day", callback_data="duration_1"),
            InlineKeyboardButton("3 days", callback_data="duration_3"),
            InlineKeyboardButton("7 days", callback_data="duration_7")
        ],
        [
            InlineKeyboardButton("14 days", callback_data="duration_14"),
            InlineKeyboardButton("30 days", callback_data="duration_30")
        ],
        [InlineKeyboardButton("📝 Custom", callback_data="duration_custom")],
        [InlineKeyboardButton("❌ Cancel", callback_data="rent_cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Show item details and ask for duration
    item_details = f"""
✅ *Item Found!*

📦 *Item Details:*
• ID: `{item_id}`
• Name: {item.get('Item Name')}
• Type: {item.get('Type')}
• Brand: {item.get('Brand', 'N/A')}
• Model: {item.get('Model', 'N/A')}
• Available Units: {quantity}

⏱️ *How long do you need this item?*
Select a duration:
    """
    
    await update.message.reply_text(item_details, parse_mode='Markdown', reply_markup=reply_markup)
    return WAITING_FOR_DURATION

async def handle_duration_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle duration button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "duration_custom":
        await query.edit_message_text(
            "📝 *Custom Duration*\n\n"
            "Please enter the number of days you need (e.g., 5 for 5 days):\n\n"
            "Type /cancel to cancel.",
            parse_mode='Markdown'
        )
        return WAITING_FOR_DURATION_CUSTOM
    
    # Extract duration from callback data
    duration = int(query.data.replace("duration_", ""))
    
    return await process_duration(query, context, duration, is_callback=True)

async def receive_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process custom duration text input"""
    try:
        duration = int(update.message.text.strip())
        
        if duration <= 0:
            await update.message.reply_text(
                "❌ Please enter a valid number of days (greater than 0).\n"
                "Type /cancel to cancel this operation."
            )
            return WAITING_FOR_DURATION_CUSTOM
        
        return await process_duration(update, context, duration, is_callback=False)
        
    except ValueError:
        await update.message.reply_text(
            "❌ Please enter a valid number (e.g., 3 for 3 days).\n"
            "Type /cancel to cancel this operation."
        )
        return WAITING_FOR_DURATION_CUSTOM

async def process_duration(update_or_query, context, duration, is_callback=True):
    """Process the rental duration and ask for photo"""
    # Calculate dates
    tz = pytz.timezone(config.TIMEZONE)
    start_date = datetime.now(tz)
    return_date = start_date + timedelta(days=duration)
    
    # Store in context
    context.user_data['rental_duration'] = duration
    context.user_data['rental_start'] = start_date.strftime('%Y-%m-%d %H:%M:%S')
    context.user_data['rental_return'] = return_date.strftime('%Y-%m-%d')
    
    # Ask for photo
    location_msg = f"""
📍 *Location: {context.user_data['rental_item_location']}*

📅 Rental Period: {duration} day(s)
🗓️ Return by: {return_date.strftime('%B %d, %Y')}

📸 *Please take a photo of the item you're picking up.*
This confirms you have collected the item.

Type /cancel to cancel this operation.
    """
    
    if is_callback:
        await update_or_query.edit_message_text(location_msg, parse_mode='Markdown')
    else:
        await update_or_query.message.reply_text(location_msg, parse_mode='Markdown')
    
    return WAITING_FOR_PICKUP_PHOTO

async def receive_pickup_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the pickup photo"""
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Please send a photo of the item.\n"
            "Type /cancel to cancel this operation."
        )
        return WAITING_FOR_PICKUP_PHOTO
    
    # Get the photo (highest resolution)
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    photo_url = photo_file.file_path
    
    # Get user details
    user = update.effective_user
    borrower_name = user.first_name + (' ' + user.last_name if user.last_name else '')
    telegram_username = f"@{user.username}" if user.username else f"ID:{user.id}"
    
    # Log the rental in Google Sheets
    success = sheets.log_rental(
        borrower_name=borrower_name,
        telegram_username=telegram_username,
        user_id=user.id,
        item_id=context.user_data['rental_item_id'],
        item_name=context.user_data['rental_item_name'],
        rental_start=context.user_data['rental_start'],
        expected_return=context.user_data['rental_return'],
        pickup_photo_url=photo_url
    )
    
    if success:
        # Create keyboard for quick actions
        keyboard = [
            [InlineKeyboardButton("📋 My Rentals", callback_data="main_myrentals")],
            [InlineKeyboardButton("🎯 Rent Another", callback_data="quick_rent")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        confirmation_msg = f"""
✅ *Rental Confirmed!*

📦 Item: {context.user_data['rental_item_name']}
🆔 Item ID: `{context.user_data['rental_item_id']}`
📅 Duration: {context.user_data['rental_duration']} day(s)
🗓️ Return by: {context.user_data['rental_return']}
📍 Location: {context.user_data['rental_item_location']}

🔔 You'll receive a reminder 1 day before the return date.

To return early, use /return command.
Thank you! 🙏
        """
        await update.message.reply_text(
            confirmation_msg, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "❌ There was an error processing your rental. Please contact an admin."
        )
    
    # Clear context
    context.user_data.clear()
    return ConversationHandler.END

async def my_rentals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's active rentals with inline keyboard"""
    user = update.effective_user
    
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        keyboard = [
            [InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")],
            [InlineKeyboardButton("📦 Browse", callback_data="main_browse")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📭 You have no active rentals.\n\n"
            "Ready to rent some equipment?",
            reply_markup=reply_markup
        )
        return
    
    message = "📦 *Your Active Rentals:*\n\n"
    
    for idx, rental in enumerate(rentals, 1):
        message += f"""
{idx}. *{rental.get('Item Name')}*
   • ID: `{rental.get('Item ID')}`
   • Rented: {rental.get('Rental Start Date')}
   • Due: {rental.get('Expected Return Date')}
   
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Return Item", callback_data="main_return")],
        [InlineKeyboardButton("🎯 Rent More", callback_data="quick_rent")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        message, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def return_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the return process with inline keyboard"""
    user = update.effective_user
    
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        keyboard = [[InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📭 You have no active rentals to return.",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    
    # Store rentals in context
    context.user_data['return_rentals'] = rentals
    
    # Create inline keyboard for rental selection
    keyboard = []
    for idx, rental in enumerate(rentals):
        keyboard.append([
            InlineKeyboardButton(
                f"{rental.get('Item Name')} ({rental.get('Item ID')})",
                callback_data=f"return_select_{idx}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="return_cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📦 *Select which item to return:*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    
    return WAITING_FOR_RETURN_CHOICE

async def receive_return_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the return item choice"""
    query = update.callback_query
    await query.answer()
    
    # Extract index from callback data
    idx = int(query.data.replace("return_select_", ""))
    rentals = context.user_data.get('return_rentals', [])
    
    if idx < 0 or idx >= len(rentals):
        await query.edit_message_text("❌ Invalid selection. Please try again.")
        return ConversationHandler.END
    
    # Store selected rental
    selected_rental = rentals[idx]
    context.user_data['return_rental'] = selected_rental
    
    await query.edit_message_text(
        f"📸 *Returning: {selected_rental.get('Item Name')}*\n\n"
        f"Please take a photo of the item to confirm return.\n\n"
        "Type /cancel to cancel this operation.",
        parse_mode='Markdown'
    )
    
    return WAITING_FOR_RETURN_PHOTO

async def receive_return_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the return photo"""
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Please send a photo of the returned item.\n"
            "Type /cancel to cancel this operation."
        )
        return WAITING_FOR_RETURN_PHOTO
    
    # Get the photo
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    photo_url = photo_file.file_path
    
    # Get rental details
    rental = context.user_data['return_rental']
    row_number = rental['_row_number']
    
    # Complete the return in Google Sheets
    success = sheets.complete_return(row_number, photo_url)
    
    if success:
        # Create quick action keyboard
        keyboard = [
            [InlineKeyboardButton("📋 My Rentals", callback_data="main_myrentals")],
            [InlineKeyboardButton("🎯 Rent Again", callback_data="quick_rent")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"✅ *Return Confirmed!*\n\n"
            f"📦 Item: {rental.get('Item Name')}\n"
            f"🆔 Item ID: `{rental.get('Item ID')}`\n\n"
            f"Thank you for returning the equipment! 🙏",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "❌ There was an error processing your return. Please contact an admin."
        )
    
    # Clear context
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current operation"""
    context.user_data.clear()
    
    keyboard = [
        [InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")],
        [InlineKeyboardButton("📦 Browse", callback_data="main_browse")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "❌ Operation cancelled.\n\n"
        "What would you like to do?",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def rent_cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel rental from callback"""
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    
    keyboard = [
        [InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")],
        [InlineKeyboardButton("📦 Browse", callback_data="main_browse")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "❌ Rental cancelled.\n\n"
        "What would you like to do?",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def return_cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel return from callback"""
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    
    await query.edit_message_text("❌ Return cancelled.")
    return ConversationHandler.END

# Main menu callback handlers
async def main_browse_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle browse from main menu"""
    query = update.callback_query
    await query.answer()
    await browse_items_inline(query, context)

async def main_myrentals_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle my rentals from main menu"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        keyboard = [
            [InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")],
            [InlineKeyboardButton("📦 Browse", callback_data="main_browse")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📭 You have no active rentals.\n\n"
            "Ready to rent some equipment?",
            reply_markup=reply_markup
        )
        return
    
    message = "📦 *Your Active Rentals:*\n\n"
    
    for idx, rental in enumerate(rentals, 1):
        message += f"""
{idx}. *{rental.get('Item Name')}*
   • ID: `{rental.get('Item ID')}`
   • Rented: {rental.get('Rental Start Date')}
   • Due: {rental.get('Expected Return Date')}
   
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Return Item", callback_data="main_return")],
        [InlineKeyboardButton("🎯 Rent More", callback_data="quick_rent")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def main_help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle help from main menu"""
    query = update.callback_query
    await query.answer()
    
    help_text = """
📖 *How to Use This Bot*

*Renting Equipment:*
1️⃣ Use /rent or /browse
2️⃣ Select item or enter Item ID
3️⃣ Choose rental duration
4️⃣ Take a photo of the item
5️⃣ Done! Equipment is yours!

*Returning Equipment:*
1️⃣ Use /return command
2️⃣ Select which item to return
3️⃣ Take a photo of the returned item
4️⃣ Done!

*Other Commands:*
• /browse - Browse items by category
• /myrentals - See your active rentals
• /help - Show this help message

📅 You'll receive a reminder 1 day before your return date!

Need assistance? Contact your tech ministry leader! 🙏
    """
    await query.edit_message_text(help_text, parse_mode='Markdown')

async def quick_rent_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick rent button handler"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📦 Browse by Category", callback_data="rent_browse")],
        [InlineKeyboardButton("🔍 I know the Item ID", callback_data="rent_manual")],
        [InlineKeyboardButton("❌ Cancel", callback_data="rent_cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎯 *Let's rent some equipment!*\n\n"
        "How would you like to find your item?",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def main_return_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle return from main menu"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        keyboard = [[InlineKeyboardButton("🎯 Rent Equipment", callback_data="quick_rent")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📭 You have no active rentals to return.",
            reply_markup=reply_markup
        )
        return
    
    # Store rentals in context
    context.user_data['return_rentals'] = rentals
    
    # Create inline keyboard for rental selection
    keyboard = []
    for idx, rental in enumerate(rentals):
        keyboard.append([
            InlineKeyboardButton(
                f"{rental.get('Item Name')} ({rental.get('Item ID')})",
                callback_data=f"return_select_{idx}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="return_cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📦 *Select which item to return:*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def main_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin panel from main menu"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        await query.edit_message_text("❌ You don't have permission to access admin commands.")
        return
    
    from admin_commands import admin_panel
    # Create a fake update for admin_panel
    fake_update = type('obj', (object,), {
        'message': type('obj', (object,), {
            'reply_text': query.edit_message_text
        })(),
        'effective_user': query.from_user
    })()
    
    keyboard = [
        [
            InlineKeyboardButton("📊 All Active Rentals", callback_data="admin_all_rentals"),
            InlineKeyboardButton("⏰ Overdue Items", callback_data="admin_overdue")
        ],
        [
            InlineKeyboardButton("📈 Statistics", callback_data="admin_stats"),
            InlineKeyboardButton("❌ Close", callback_data="admin_close")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🔧 *Admin Control Panel*\n\n"
        "Select an option below:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def main():
    """Start the bot"""
    # This function is not used directly in the enhanced version
    # See main.py for the entry point
    pass

# Export handlers for use in main.py
__all__ = [
    'start', 'help_command', 'rent_start', 'my_rentals', 'return_start',
    'receive_item_id', 'receive_duration', 'receive_pickup_photo',
    'receive_return_choice', 'receive_return_photo', 'cancel',
    'WAITING_FOR_ITEM_ID', 'WAITING_FOR_DURATION', 'WAITING_FOR_DURATION_CUSTOM',
    'WAITING_FOR_PICKUP_PHOTO', 'WAITING_FOR_RETURN_CHOICE', 'WAITING_FOR_RETURN_PHOTO'
]

