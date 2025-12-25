"""
Reminder Scheduler
Sends reminders to users 1 day before their return date
"""
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
import asyncio
from sheets_manager import SheetsManager
import config

class ReminderScheduler:
    def __init__(self, bot_token):
        self.bot = Bot(token=bot_token)
        self.sheets = SheetsManager()
        self.scheduler = BackgroundScheduler()
        
    def send_reminders(self):
        """Check for rentals due tomorrow and send reminders"""
        print("🔔 Checking for rentals due tomorrow...")
        
        try:
            due_rentals = self.sheets.get_all_due_tomorrow()
            
            if not due_rentals:
                print("No rentals due tomorrow.")
                return
            
            print(f"Found {len(due_rentals)} rental(s) due tomorrow. Sending reminders...")
            
            for rental in due_rentals:
                asyncio.run(self.send_reminder(rental))
                
        except Exception as e:
            print(f"Error in send_reminders: {e}")
    
    async def send_reminder(self, rental):
        """Send a reminder message to a user"""
        try:
            user_id = rental.get('User ID', '')
            
            if not user_id:
                print(f"Cannot send reminder - no user ID for rental {rental.get('Item ID')}")
                return
            
            user_id = int(user_id)
            
            message = f"""
🔔 *Rental Return Reminder*

📦 Item: {rental.get('Item Name')}
🆔 Item ID: `{rental.get('Item ID')}`
📅 Rented on: {rental.get('Rental Start Date')}
⚠️ *Due tomorrow:* {rental.get('Expected Return Date')}

Please remember to return the item to its location.

If you're returning it now, use /return command.

Thank you! 🙏
            """
            
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            print(f"✅ Sent reminder to user {user_id} for item {rental.get('Item ID')}")
            
        except Exception as e:
            print(f"Error sending reminder: {e}")
    
    def start(self):
        """Start the scheduler"""
        # Run reminder check every day at 9:00 AM
        self.scheduler.add_job(
            self.send_reminders,
            'cron',
            hour=9,
            minute=0,
            timezone=config.TIMEZONE
        )
        
        self.scheduler.start()
        print("✅ Reminder scheduler started (runs daily at 9:00 AM)")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        print("⏹️ Reminder scheduler stopped")

