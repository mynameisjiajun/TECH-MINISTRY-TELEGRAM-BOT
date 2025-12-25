"""
Main entry point for the bot
Combines bot functionality with reminder scheduler
"""
import asyncio
from telegram.ext import Application
from bot import (
    start, help_command, my_rentals, rent_start, receive_item_id,
    receive_duration, receive_pickup_photo, return_start, receive_return_choice,
    receive_return_photo, cancel,
    WAITING_FOR_ITEM_ID, WAITING_FOR_DURATION, WAITING_FOR_PICKUP_PHOTO,
    WAITING_FOR_RETURN_CHOICE, WAITING_FOR_RETURN_PHOTO
)
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler
from telegram import Update
from reminder_scheduler import ReminderScheduler
import config

def main():
    """Start the bot with reminder scheduler"""
    print("=" * 50)
    print("🙏 Church Tech Ministry Equipment Rental Bot")
    print("=" * 50)
    
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
    
    # Initialize and start reminder scheduler
    scheduler = ReminderScheduler(config.TELEGRAM_BOT_TOKEN)
    scheduler.start()
    
    # Start the Bot
    print("🤖 Bot is running...")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n⏹️ Stopping bot...")
        scheduler.stop()
        print("✅ Bot stopped successfully")

if __name__ == '__main__':
    main()

