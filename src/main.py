"""
Main entry point for the bot
Combines bot functionality with reminder scheduler and all features
"""
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from telegram import Update
from reminder_scheduler import ReminderScheduler
import config

# Import from bot
from bot import (
    start, help_command, my_rentals, rent_start, receive_item_id, receive_quantity,
    receive_duration, receive_pickup_photo, return_start, receive_return_choice,
    receive_return_photo, cancel, receive_password,
    WAITING_FOR_PASSWORD, WAITING_FOR_ITEM_ID, WAITING_FOR_QUANTITY, WAITING_FOR_DURATION, WAITING_FOR_DURATION_CUSTOM,
    WAITING_FOR_PICKUP_PHOTO, WAITING_FOR_RETURN_CHOICE, WAITING_FOR_RETURN_PHOTO,
    handle_duration_selection,
    rent_cancel_callback, return_cancel_callback,
    main_myrentals_callback, main_help_callback,
    quick_rent_callback, main_return_callback, main_admin_callback
)

# Import list command
from list_command import send_equipment_list, view_sheet_callback

# Import admin commands
from admin_commands import (
    admin_panel, view_all_rentals, view_overdue_items, view_statistics,
    admin_back, admin_close, notify_overdue_users
)

def main():
    """Start the bot"""
    print("=" * 50)
    print("🙏 Church Tech Ministry Equipment Rental Bot")
    print("   Version 2.1.0")
    print("=" * 50)
    
    # Create the Application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Verification conversation handler for /start
    verification_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_FOR_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
    )
    
    # Command handlers
    application.add_handler(verification_conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myrentals", my_rentals))
    application.add_handler(CommandHandler("list", send_equipment_list))
    
    # Admin commands
    application.add_handler(CommandHandler("admin", admin_panel))
    
    # Rental conversation handler with inline keyboards and password verification
    rental_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('rent', rent_start),
            CallbackQueryHandler(quick_rent_callback, pattern='^quick_rent$')
        ],
        states={
            WAITING_FOR_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password),
            ],
            WAITING_FOR_ITEM_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_item_id),
            ],
            WAITING_FOR_QUANTITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_quantity),
            ],
            WAITING_FOR_DURATION: [
                CallbackQueryHandler(handle_duration_selection, pattern='^duration_'),
            ],
            WAITING_FOR_DURATION_CUSTOM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_duration),
            ],
            WAITING_FOR_PICKUP_PHOTO: [
                MessageHandler(filters.PHOTO, receive_pickup_photo),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('rent', rent_start),  # Allow /rent to restart anytime
            CallbackQueryHandler(rent_cancel_callback, pattern='^rent_cancel$')
        ],
        allow_reentry=True,  # Allow /rent to work even during an active conversation
    )
    
    # Return conversation handler with inline keyboards
    return_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('return', return_start),
            CallbackQueryHandler(main_return_callback, pattern='^main_return$')
        ],
        states={
            WAITING_FOR_RETURN_CHOICE: [
                CallbackQueryHandler(receive_return_choice, pattern='^return_select_'),
            ],
            WAITING_FOR_RETURN_PHOTO: [
                MessageHandler(filters.PHOTO, receive_return_photo),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('return', return_start),  # Allow /return to restart anytime
            CallbackQueryHandler(return_cancel_callback, pattern='^return_cancel$')
        ],
        allow_reentry=True,  # Allow /return to work even during an active conversation
    )
    
    application.add_handler(rental_conv_handler)
    application.add_handler(return_conv_handler)
    
    # Main menu callback handlers
    application.add_handler(CallbackQueryHandler(view_sheet_callback, pattern='^view_sheet$'))
    application.add_handler(CallbackQueryHandler(main_myrentals_callback, pattern='^main_myrentals$'))
    application.add_handler(CallbackQueryHandler(main_help_callback, pattern='^main_help$'))
    application.add_handler(CallbackQueryHandler(main_admin_callback, pattern='^main_admin$'))
    
    # Admin callback handlers
    application.add_handler(CallbackQueryHandler(view_all_rentals, pattern='^admin_all_rentals$'))
    application.add_handler(CallbackQueryHandler(view_overdue_items, pattern='^admin_overdue$'))
    application.add_handler(CallbackQueryHandler(view_statistics, pattern='^admin_stats$'))
    application.add_handler(CallbackQueryHandler(admin_back, pattern='^admin_back$'))
    application.add_handler(CallbackQueryHandler(admin_close, pattern='^admin_close$'))
    application.add_handler(CallbackQueryHandler(notify_overdue_users, pattern='^admin_notify_overdue$'))
    
    # Initialize and start reminder scheduler
    scheduler = ReminderScheduler(config.TELEGRAM_BOT_TOKEN)
    scheduler.start()
    
    # Print admin info if configured
    if config.ADMIN_USER_IDS:
        print(f"✅ Admin users configured: {len(config.ADMIN_USER_IDS)}")
    else:
        print("⚠️  No admin users configured. Add ADMIN_USER_IDS to .env")
        print("   Get your user ID from @userinfobot on Telegram")
    
    # Print equipment list info
    if config.PUBLIC_SHEET_URL:
        print(f"✅ Equipment list URL configured")
    else:
        print("⚠️  No equipment list URL configured. Add PUBLIC_SHEET_URL to .env")
    
    # Start the Bot
    print("🤖 Bot is running with enhanced features...")
    print("   • Inline keyboards enabled")
    print("   • Equipment list link enabled")
    print("   • Admin panel enabled")
    print("   • Overdue tracking enabled")
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

