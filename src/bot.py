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

# Conversation states
WAITING_FOR_PASSWORD = 0
WAITING_FOR_ITEM_ID = 1
WAITING_FOR_QUANTITY = 2
WAITING_FOR_DURATION = 3
WAITING_FOR_DURATION_CUSTOM = 4
WAITING_FOR_PICKUP_PHOTO = 5
WAITING_FOR_RETURN_CHOICE = 6
WAITING_FOR_RETURN_PHOTO = 7

# Initialize Sheets Manager
sheets = SheetsManager()

# Password for verification (from config/env)
VERIFICATION_PASSWORD = config.VERIFICATION_PASSWORD

# Store verified users (in-memory, resets when bot restarts)
verified_users = set()

# Helper Functions for Validation
def validate_quantity_input(quantity_str, max_available):
    """
    Validate quantity input from user
    Returns: (quantity: int, error_message: str or None)
    """
    try:
        qty = int(quantity_str)
        
        if qty < 1:
            return None, "❌ Quantity must be at least 1."
        
        if qty > max_available:
            return None, f"❌ Only {max_available} unit(s) available."
        
        if qty > 50:
            return None, "❌ Maximum 50 units per rental. For bulk orders, contact @mynameisjiajun"
        
        return qty, None
    except ValueError:
        return None, "❌ Please enter a valid number (e.g., 1, 2, 3)"

def validate_duration_input(days_str):
    """
    Validate duration input from user
    Returns: (days: int, error_message: str or None)
    """
    try:
        days = int(days_str)
        
        if days < 1:
            return None, "❌ Duration must be at least 1 day."
        
        if days > 90:
            return None, "❌ Maximum rental period is 90 days. Contact @mynameisjiajun for longer rentals."
        
        return days, None
    except ValueError:
        return None, "❌ Please enter a valid number of days (e.g., 7, 14, 30)"

def is_user_verified(user_id):
    """Check if user has entered correct password"""
    return user_id in verified_users

def verify_user(user_id):
    """Mark user as verified"""
    verified_users.add(user_id)

async def check_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if user is verified, if not ask for password"""
    user = update.effective_user
    
    if not is_user_verified(user.id):
        await update.message.reply_text(
            "🔒 *Verification Required*\n\n"
            "Please enter the password to use this bot:\n\n"
            "Type /cancel to cancel.",
            parse_mode='Markdown'
        )
        return WAITING_FOR_PASSWORD
    
    return None

async def receive_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process password input"""
    user = update.effective_user
    password = update.message.text.strip()
    
    if password == VERIFICATION_PASSWORD:
        verify_user(user.id)
        
        # Check if user was trying to rent before verification
        after_verify = context.user_data.get('after_verify')
        
        if after_verify == 'rent':
            # Clear the after_verify flag
            context.user_data.pop('after_verify', None)
            
            # Check if user has overdue items
            has_overdue, overdue_rental = sheets.user_has_overdue_items(user.id)
            if has_overdue:
                await update.message.reply_text(
                    "✅ *Verification Successful!*\n\n"
                    f"However, you have an overdue item that must be returned first:\n\n"
                    f"📦 Item: {overdue_rental.get('Item Name', 'Unknown')}\n"
                    f"🆔 ID: `{overdue_rental.get('Item ID', 'N/A')}`\n"
                    f"🗓️ Was due: {overdue_rental.get('Expected Return Date', 'N/A')}\n\n"
                    "⚠️ Please return this item before renting more equipment.\n\n"
                    "Use /return to return your overdue item.",
                    parse_mode='Markdown'
                )
                return ConversationHandler.END
            
            # Continue to rental process
            await update.message.reply_text(
                "✅ *Verification Successful!*\n\n"
                "🎯 *Let's rent some equipment!*\n\n"
                "Enter the *Item ID* (e.g., CAB001)\n\n"
                "💡 Use /list for equipment list\n"
                "Type /cancel to cancel.",
                parse_mode='Markdown'
            )
            return WAITING_FOR_ITEM_ID
        else:
            # Just verified via /start, show welcome message  
            user = update.effective_user
            welcome_message = f"""
✅ *Verification Successful!*

Welcome {user.first_name}! 👋

I help you rent and return tech equipment easily!

*📋 Available Commands:*

🎯 *Main Commands:*
• /rent - Rent equipment
• /return - Return equipment
• /myrentals - View your active rentals
• /list - Get equipment list link

ℹ️ *Information:*
• /help - Detailed help guide
• /cancel - Cancel current operation

*✨ Quick Start:*
1️⃣ Use /list to see available items
2️⃣ Use /rent to start renting
3️⃣ I'll guide you through the rest!

💡 You can rent the same item multiple times!

📦 *Need to loan items in bulk?*
Contact @mynameisjiajun for bulk loan arrangements.
            """
            
            if is_admin(user.id):
                welcome_message += "\n\n🔧 *Admin:* /admin - Admin panel"
            
            await update.message.reply_text(
                welcome_message,
                parse_mode='Markdown'
            )
            return ConversationHandler.END
    else:
        await update.message.reply_text(
            "❌ *Incorrect Password*\n\n"
            "Please try again or type /cancel to cancel.",
            parse_mode='Markdown'
        )
        return WAITING_FOR_PASSWORD

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    
    # Check if user is verified
    if not is_user_verified(user.id):
        await update.message.reply_text(
            "🔒 *Verification Required*\n\n"
            "Welcome to Church Tech Ministry Equipment Rental Bot!\n\n"
            "Please enter the password to continue:\n\n"
            "Type /cancel if you don't have the password.",
            parse_mode='Markdown'
        )
        return WAITING_FOR_PASSWORD
    
    welcome_message = f"""
🙏 *Welcome to Church Tech Ministry Equipment Rental Bot!*

Hello {user.first_name}! 👋

I help you rent and return tech equipment easily!

*📋 Available Commands:*

🎯 *Main Commands:*
• /rent - Rent equipment
• /return - Return equipment
• /myrentals - View your active rentals
• /list - Get equipment list link

ℹ️ *Information:*
• /help - Detailed help guide
• /cancel - Cancel current operation

*✨ Quick Start:*
1️⃣ Use /list to see available items
2️⃣ Use /rent to start renting
3️⃣ I'll guide you through the rest!

💡 You can rent the same item multiple times!

📦 *Need to loan items in bulk?*
Contact @mynameisjiajun for bulk loan arrangements.
    """
    
    if is_admin(user.id):
        welcome_message += "\n\n🔧 *Admin:* /admin - Admin panel"
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    user = update.effective_user
    
    # Check if user is verified
    if not is_user_verified(user.id):
        await update.message.reply_text(
            "🔒 *Verification Required*\n\n"
            "Please use /start and enter the password first.",
            parse_mode='Markdown'
        )
        return
    
    help_text = """
📖 *Equipment Rental Guide*

*🎯 How to Rent Equipment:*

1️⃣ View available items: /list
2️⃣ Start rental process: /rent
3️⃣ Enter Item ID (e.g., CAB001)
   • Item IDs are not case sensitive!
4️⃣ Select rental duration
5️⃣ Take a photo of the item
6️⃣ Done! Rental logged ✅

*🔄 How to Return Equipment:*

1️⃣ Start return process: /return
2️⃣ Select item from your rentals
3️⃣ Take a photo of the returned item
4️⃣ Remember to return to the correct location!
5️⃣ Done! Return logged ✅

*📦 Managing Your Rentals:*

• /myrentals - See all your active rentals
• You can rent the same item multiple times
• Each rental is tracked separately
• You'll get a reminder 1 day before due date

*💬 Commands List:*

• /rent - Rent equipment
• /return - Return equipment  
• /myrentals - View active rentals
• /list - Get equipment list
• /cancel - Cancel current action
• /help - Show this guide

*📞 Need Help?*

For bulk requests or special arrangements, contact:
👤 @mynameisjiajun

🙏 Thank you for serving!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def rent_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the rental process"""
    user = update.effective_user
    
    # Check if user is verified
    if not is_user_verified(user.id):
        # Store that user wants to rent after verification
        context.user_data['after_verify'] = 'rent'
        await update.message.reply_text(
            "🔒 *Verification Required*\n\n"
            "Please enter the password to use this bot:\n\n"
            "Type /cancel to cancel.",
            parse_mode='Markdown'
        )
        return WAITING_FOR_PASSWORD
    
    # Check if user has overdue items
    has_overdue, overdue_rental = sheets.user_has_overdue_items(user.id)
    if has_overdue:
        await update.message.reply_text(
            f"❌ *You have an overdue item that must be returned first:*\n\n"
            f"📦 Item: {overdue_rental.get('Item Name', 'Unknown')}\n"
            f"🆔 ID: `{overdue_rental.get('Item ID', 'N/A')}`\n"
            f"🗓️ Was due: {overdue_rental.get('Expected Return Date', 'N/A')}\n\n"
            "⚠️ Please return this item before renting more equipment.\n\n"
            "Use /return to return your overdue item.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        "🎯 *Let's rent some equipment!*\n\n"
        "Enter the *Item ID* (e.g., CAB001)\n\n"
        "💡 Use /list for equipment list\n"
        "Type /cancel to cancel.",
        parse_mode='Markdown'
    )
    
    return WAITING_FOR_ITEM_ID

# Removed broken browse functions - use /list command instead

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
        # Item is out of stock - check Quantity Current
        quantity_current = int(item.get('Quantity Current', 0))
        
        await update.message.reply_text(
            f"❌ Sorry, *{item.get('Item Name')}* (ID: `{item_id}`) is currently OUT OF STOCK.\n\n"
            f"📊 Current Stock: {quantity_current}\n\n"
            "This item cannot be rented at the moment. Please choose a different item or try again later.\n\n"
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
    context.user_data['rental_item_max_quantity'] = quantity
    
    # Ask for quantity
    quantity_msg = f"""
✅ *Item Found!*

📦 *Item Details:*
• ID: `{item_id}`
• Name: {item.get('Item Name')}
• Type: {item.get('Type')}
• Brand: {item.get('Brand', 'N/A')}
• Model: {item.get('Model', 'N/A')}
• Available Units: {quantity}

🔢 *How many units do you need?*

Enter a number between 1 and {quantity}

Type /cancel to cancel this operation.
    """
    
    await update.message.reply_text(quantity_msg, parse_mode='Markdown')
    return WAITING_FOR_QUANTITY

async def receive_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the quantity provided by user"""
    quantity_input = update.message.text.strip()
    max_quantity = context.user_data.get('rental_item_max_quantity', 1)
    
    # Validate quantity using helper function
    quantity, error_msg = validate_quantity_input(quantity_input, max_quantity)
    
    if error_msg:
        await update.message.reply_text(
            f"{error_msg}\n\n"
            f"Please enter a number between 1 and {max_quantity}\n\n"
            "Type /cancel to cancel this operation."
        )
        return WAITING_FOR_QUANTITY
    
    # Store quantity
    context.user_data['rental_quantity'] = quantity
    
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
    
    # Show duration selection
    duration_msg = f"""
✅ *Quantity: {quantity} unit(s)*

⏱️ *How long do you need {'this item' if quantity == 1 else 'these items'}?*
Select a rental duration:
    """
    
    await update.message.reply_text(duration_msg, parse_mode='Markdown', reply_markup=reply_markup)
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
    duration_input = update.message.text.strip()
    
    # Validate duration using helper function
    duration, error_msg = validate_duration_input(duration_input)
    
    if error_msg:
        await update.message.reply_text(
            f"{error_msg}\n\n"
            "Please enter a valid number of days (e.g., 7, 14, 30).\n\n"
            "Type /cancel to cancel this operation."
        )
        return WAITING_FOR_DURATION_CUSTOM
    
    return await process_duration(update, context, duration, is_callback=False)

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
    
    # DOUBLE-CHECK availability before finalizing (prevent race conditions)
    item_id = context.user_data['rental_item_id']
    requested_qty = context.user_data.get('rental_quantity', 1)
    
    available, current_qty, item = sheets.check_availability(item_id)
    
    if not available or current_qty < requested_qty:
        await update.message.reply_text(
            f"❌ *Sorry, this item is no longer available!*\n\n"
            f"Someone else may have rented it while you were completing your request.\n\n"
            f"📊 Current Stock: {current_qty}\n"
            f"📦 You requested: {requested_qty}\n\n"
            "Please start over with /rent and check current availability.",
            parse_mode='Markdown'
        )
        context.user_data.clear()
        return ConversationHandler.END
    
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
        pickup_photo_url=photo_url,
        quantity=context.user_data.get('rental_quantity', 1)
    )
    
    if success:
        rental_quantity = context.user_data.get('rental_quantity', 1)
        confirmation_msg = f"""
✅ *Rental Confirmed!*

📦 Item: {context.user_data['rental_item_name']}
🆔 Item ID: `{context.user_data['rental_item_id']}`
📦 Quantity: {rental_quantity}
📅 Duration: {context.user_data['rental_duration']} day(s)
🗓️ Return by: {context.user_data['rental_return']}
📍 Location: {context.user_data['rental_item_location']}

🔔 You'll receive a reminder 1 day before the return date.

*What's next?*
• To view all your rentals: /myrentals
• To rent another item: /rent
• To return this item early: /return

Thank you! 🙏
        """
        await update.message.reply_text(
            confirmation_msg, 
            parse_mode='Markdown'
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
    
    # Check if user is verified
    if not is_user_verified(user.id):
        await update.message.reply_text(
            "🔒 *Verification Required*\n\n"
            "Please use /start and enter the password first.",
            parse_mode='Markdown'
        )
        return
    
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        await update.message.reply_text(
            "📭 You have no active rentals.\n\n"
            "Ready to rent some equipment?\n\n"
            "• Use /list to see equipment list\n"
            "• Use /rent to start renting",
            parse_mode='Markdown'
        )
        return
    
    message = f"📦 *Your Active Rentals ({len(rentals)} item{'s' if len(rentals) > 1 else ''}):*\n\n"
    
    for idx, rental in enumerate(rentals, 1):
        item_name = rental.get('Item Name', 'Unknown Item')
        item_id = rental.get('Item ID', 'N/A')
        quantity = rental.get('Quantity', 1)
        rental_start = rental.get('Rental Start Date', 'N/A')
        expected_return = rental.get('Expected Return Date', 'N/A')
        location = rental.get('Location', 'Unknown')
        
        message += f"{idx}. *{item_name}*\n"
        message += f"   🆔 ID: `{item_id}`\n"
        message += f"   📦 Quantity: {quantity}\n"
        message += f"   📍 Location: {location}\n"
        message += f"   📅 Rented: {rental_start}\n"
        message += f"   🗓️ Due: {expected_return}\n"
        message += f"\n"
    
    message += "─────────────────\n"
    message += "*💡 Tips:*\n"
    message += "• You can rent the same item multiple times\n"
    message += "• Each rental is tracked separately\n"
    message += "• Use /return when you're ready to return\n"
    message += "• Use /rent to rent more items"
    
    await update.message.reply_text(
        message, 
        parse_mode='Markdown'
    )

async def return_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the return process"""
    user = update.effective_user
    
    # Check if user is verified
    if not is_user_verified(user.id):
        await update.message.reply_text(
            "🔒 *Verification Required*\n\n"
            "Please use /start and enter the password first.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        await update.message.reply_text(
            "📭 You have no active rentals to return."
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
    
    location = selected_rental.get('Location', 'the designated area')
    quantity = selected_rental.get('Quantity', 1)
    
    await query.edit_message_text(
        f"📸 *Returning: {selected_rental.get('Item Name')}*\n"
        f"🆔 Item ID: `{selected_rental.get('Item ID')}`\n"
        f"📦 Quantity: {quantity}\n"
        f"📍 Return to: *{location}*\n\n"
        f"⚠️ Please return {'the item' if quantity == 1 else 'all items'} to *{location}* and take a photo to confirm.\n\n"
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
        location = rental.get('Location', 'the designated area')
        quantity = rental.get('Quantity', 1)
        
        await update.message.reply_text(
            f"✅ *Return Confirmed!*\n\n"
            f"📦 Item: {rental.get('Item Name')}\n"
            f"🆔 Item ID: `{rental.get('Item ID')}`\n"
            f"📦 Quantity: {quantity}\n"
            f"📍 Location: *{location}*\n\n"
            f"⚠️ *Please return {'the item' if quantity == 1 else 'all items'} to: {location}*\n\n"
            f"Thank you for returning the equipment! 🙏\n\n"
            f"*What's next?*\n"
            f"• To rent another item: /rent\n"
            f"• To view your rentals: /myrentals",
            parse_mode='Markdown'
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
    
    await update.message.reply_text(
        "❌ Operation cancelled.\n\n"
        "*What would you like to do?*\n"
        "• Use /rent to rent equipment\n"
        "• Use /return to return items\n"
        "• Use /myrentals to view your rentals\n"
        "• Use /list to see equipment list",
        parse_mode='Markdown'
    )
    return ConversationHandler.END

async def rent_cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel rental from callback"""
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    
    await query.edit_message_text(
        "❌ Rental cancelled.\n\n"
        "*What would you like to do?*\n"
        "• Use /rent to rent equipment\n"
        "• Use /return to return items\n"
        "• Use /myrentals to view your rentals\n"
        "• Use /list to see equipment list",
        parse_mode='Markdown'
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
async def main_myrentals_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle my rentals from main menu - simplified"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        await query.edit_message_text(
            "📭 You have no active rentals.\n\n"
            "Ready to rent some equipment?\n\n"
            "• Use /list to see equipment list\n"
            "• Use /rent to start renting",
            parse_mode='Markdown'
        )
        return
    
    message = f"📦 *Your Active Rentals ({len(rentals)} item{'s' if len(rentals) > 1 else ''}):*\n\n"
    
    for idx, rental in enumerate(rentals, 1):
        item_name = rental.get('Item Name', 'Unknown Item')
        item_id = rental.get('Item ID', 'N/A')
        rental_start = rental.get('Rental Start Date', 'N/A')
        expected_return = rental.get('Expected Return Date', 'N/A')
        location = rental.get('Location', 'Unknown')
        
        message += f"{idx}. *{item_name}*\n"
        message += f"   🆔 ID: `{item_id}`\n"
        message += f"   📍 Location: {location}\n"
        message += f"   📅 Rented: {rental_start}\n"
        message += f"   🗓️ Due: {expected_return}\n"
        message += f"\n"
    
    message += "─────────────────\n"
    message += "*💡 Tips:*\n"
    message += "• You can rent the same item multiple times\n"
    message += "• Each rental is tracked separately\n"
    message += "• Use /return when you're ready to return\n"
    message += "• Use /rent to rent more items"
    
    await query.edit_message_text(
        message, 
        parse_mode='Markdown'
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
    """Quick rent button handler - starts rental process"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    # Check if user is verified
    if not is_user_verified(user.id):
        await query.message.reply_text(
            "🔒 *Verification Required*\n\n"
            "Please use /start and enter the password first.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    # Check if user has overdue items
    has_overdue, overdue_rental = sheets.user_has_overdue_items(user.id)
    if has_overdue:
        await query.message.reply_text(
            f"❌ *You have an overdue item that must be returned first:*\n\n"
            f"📦 Item: {overdue_rental.get('Item Name', 'Unknown')}\n"
            f"🆔 ID: `{overdue_rental.get('Item ID', 'N/A')}`\n"
            f"🗓️ Was due: {overdue_rental.get('Expected Return Date', 'N/A')}\n\n"
            "⚠️ Please return this item before renting more equipment.\n\n"
            "Use /return to return your overdue item.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    await query.message.reply_text(
        "🎯 *Let's rent some equipment!*\n\n"
        "Enter the *Item ID* (e.g., CAB001)\n\n"
        "💡 Use /list for equipment list\n"
        "Type /cancel to cancel.",
        parse_mode='Markdown'
    )
    
    return WAITING_FOR_ITEM_ID

async def main_return_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle return from main menu"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    # Check if user is verified
    if not is_user_verified(user.id):
        await query.message.reply_text(
            "🔒 *Verification Required*\n\n"
            "Please use /start and enter the password first.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
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
    'handle_duration_selection', 'rent_cancel_callback', 'return_cancel_callback',
    'main_myrentals_callback', 'main_help_callback', 'quick_rent_callback',
    'main_return_callback', 'main_admin_callback',
    'WAITING_FOR_ITEM_ID', 'WAITING_FOR_DURATION', 'WAITING_FOR_DURATION_CUSTOM',
    'WAITING_FOR_PICKUP_PHOTO', 'WAITING_FOR_RETURN_CHOICE', 'WAITING_FOR_RETURN_PHOTO'
]

