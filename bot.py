"""
Main Telegram Bot
Handles all user interactions and commands
"""
from telegram import Update, ForceReply
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes,
    ConversationHandler
)
from datetime import datetime, timedelta
import pytz
import config
from sheets_manager import SheetsManager

# Conversation states
WAITING_FOR_ITEM_ID = 1
WAITING_FOR_DURATION = 2
WAITING_FOR_PICKUP_PHOTO = 3
WAITING_FOR_RETURN_CHOICE = 4
WAITING_FOR_RETURN_PHOTO = 5

# Initialize Sheets Manager
sheets = SheetsManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = f"""
🙏 Welcome to Church Tech Ministry Equipment Rental Bot, {user.first_name}!

📋 Available Commands:
/rent - Rent an equipment
/myrentals - View your active rentals
/return - Return an equipment early
/help - Show this help message

To get started, use /rent followed by an Item ID or just type /rent and follow the prompts!
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
📖 *How to Use This Bot*

*Renting Equipment:*
1️⃣ Use /rent command
2️⃣ Enter the Item ID (e.g., CAB001)
3️⃣ Specify rental duration in days
4️⃣ Take a photo of the item you're picking up
5️⃣ Done! You'll get location details

*Returning Equipment:*
1️⃣ Use /return command
2️⃣ Select which item to return
3️⃣ Take a photo of the returned item
4️⃣ Done!

*Other Commands:*
• /myrentals - See all your active rentals
• /help - Show this help message

📅 You'll receive a reminder 1 day before your return date!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def rent_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the rental process"""
    await update.message.reply_text(
        "🔍 Please enter the *Item ID* you want to rent:\n"
        "(e.g., CAB001, SDI005)\n\n"
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

📅 *How many days do you need this item?*
(Enter a number, e.g., 3 for 3 days)

Type /cancel to cancel this operation.
    """
    
    await update.message.reply_text(item_details, parse_mode='Markdown')
    return WAITING_FOR_DURATION

async def receive_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the rental duration"""
    try:
        duration = int(update.message.text.strip())
        
        if duration <= 0:
            await update.message.reply_text(
                "❌ Please enter a valid number of days (greater than 0).\n"
                "Type /cancel to cancel this operation."
            )
            return WAITING_FOR_DURATION
        
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
        
        await update.message.reply_text(location_msg, parse_mode='Markdown')
        return WAITING_FOR_PICKUP_PHOTO
        
    except ValueError:
        await update.message.reply_text(
            "❌ Please enter a valid number (e.g., 3 for 3 days).\n"
            "Type /cancel to cancel this operation."
        )
        return WAITING_FOR_DURATION

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
        user_id=user.id,  # Store user ID for reminders
        item_id=context.user_data['rental_item_id'],
        item_name=context.user_data['rental_item_name'],
        rental_start=context.user_data['rental_start'],
        expected_return=context.user_data['rental_return'],
        pickup_photo_url=photo_url
    )
    
    if success:
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
        await update.message.reply_text(confirmation_msg, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "❌ There was an error processing your rental. Please contact an admin."
        )
    
    # Clear context
    context.user_data.clear()
    return ConversationHandler.END

async def my_rentals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's active rentals"""
    user = update.effective_user
    
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        await update.message.reply_text(
            "📭 You have no active rentals.\n\n"
            "Use /rent to rent equipment!"
        )
        return
    
    message = "📦 *Your Active Rentals:*\n\n"
    
    for idx, rental in enumerate(rentals, 1):
        message += f"""
{idx}. *{rental.get('Item Name')}*
   • ID: `{rental.get('Item ID')}`
   • Rented on: {rental.get('Rental Start Date')}
   • Return by: {rental.get('Expected Return Date')}
   
"""
    
    message += "\nUse /return to return an item early."
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def return_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the return process"""
    user = update.effective_user
    
    rentals = sheets.get_active_rentals_by_user(user.id)
    
    if not rentals:
        await update.message.reply_text(
            "📭 You have no active rentals to return.\n\n"
            "Use /myrentals to check your rentals."
        )
        return ConversationHandler.END
    
    # Store rentals in context
    context.user_data['return_rentals'] = rentals
    
    message = "📦 *Select which item to return:*\n\n"
    
    for idx, rental in enumerate(rentals, 1):
        message += f"{idx}. {rental.get('Item Name')} (ID: `{rental.get('Item ID')}`)\n"
    
    message += "\n*Reply with the number* (e.g., 1) or type /cancel to cancel."
    
    await update.message.reply_text(message, parse_mode='Markdown')
    return WAITING_FOR_RETURN_CHOICE

async def receive_return_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the return item choice"""
    try:
        choice = int(update.message.text.strip())
        rentals = context.user_data.get('return_rentals', [])
        
        if choice < 1 or choice > len(rentals):
            await update.message.reply_text(
                f"❌ Please enter a valid number between 1 and {len(rentals)}.\n"
                "Type /cancel to cancel this operation."
            )
            return WAITING_FOR_RETURN_CHOICE
        
        # Store selected rental
        selected_rental = rentals[choice - 1]
        context.user_data['return_rental'] = selected_rental
        
        await update.message.reply_text(
            f"📸 *Returning: {selected_rental.get('Item Name')}*\n\n"
            f"Please take a photo of the item to confirm return.\n\n"
            "Type /cancel to cancel this operation.",
            parse_mode='Markdown'
        )
        return WAITING_FOR_RETURN_PHOTO
        
    except ValueError:
        await update.message.reply_text(
            "❌ Please enter a valid number.\n"
            "Type /cancel to cancel this operation."
        )
        return WAITING_FOR_RETURN_CHOICE

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
        await update.message.reply_text(
            f"✅ *Return Confirmed!*\n\n"
            f"📦 Item: {rental.get('Item Name')}\n"
            f"🆔 Item ID: `{rental.get('Item ID')}`\n\n"
            f"Thank you for returning the equipment! 🙏",
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
        "Use /help to see available commands."
    )
    return ConversationHandler.END

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myrentals", my_rentals))
    
    # Rental conversation handler
    rental_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('rent', rent_start)],
        states={
            WAITING_FOR_ITEM_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_item_id)
            ],
            WAITING_FOR_DURATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_duration)
            ],
            WAITING_FOR_PICKUP_PHOTO: [
                MessageHandler(filters.PHOTO, receive_pickup_photo)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Return conversation handler
    return_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('return', return_start)],
        states={
            WAITING_FOR_RETURN_CHOICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_return_choice)
            ],
            WAITING_FOR_RETURN_PHOTO: [
                MessageHandler(filters.PHOTO, receive_return_photo)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    application.add_handler(rental_conv_handler)
    application.add_handler(return_conv_handler)
    
    # Start the Bot
    print("🤖 Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

