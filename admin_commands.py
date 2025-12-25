"""
Admin Commands Module
Provides administrative functions for bot management
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
import pytz
import config
from sheets_manager import SheetsManager

sheets = SheetsManager()

def is_admin(user_id: int) -> bool:
    """Check if user is an admin"""
    return user_id in config.ADMIN_USER_IDS

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display admin control panel"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text(
            "❌ You don't have permission to access admin commands."
        )
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📊 All Active Rentals", callback_data="admin_all_rentals"),
            InlineKeyboardButton("⏰ Overdue Items", callback_data="admin_overdue")
        ],
        [
            InlineKeyboardButton("📈 Statistics", callback_data="admin_stats"),
            InlineKeyboardButton("👥 User Activity", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton("🔄 Force Return", callback_data="admin_force_return"),
            InlineKeyboardButton("🔍 Search User", callback_data="admin_search_user")
        ],
        [
            InlineKeyboardButton("📢 Broadcast Message", callback_data="admin_broadcast"),
            InlineKeyboardButton("❌ Close", callback_data="admin_close")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔧 *Admin Control Panel*\n\n"
        "Select an option below:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def view_all_rentals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all active rentals"""
    query = update.callback_query
    await query.answer()
    
    try:
        all_logs = sheets.log_sheet.get_all_records()
        active_rentals = [log for log in all_logs if log.get('Status', '').upper() == 'ACTIVE']
        
        if not active_rentals:
            await query.edit_message_text("✅ No active rentals at the moment!")
            return
        
        message = f"📦 *Active Rentals ({len(active_rentals)})*\n\n"
        
        for idx, rental in enumerate(active_rentals[:20], 1):  # Limit to 20 for message length
            message += f"{idx}. *{rental.get('Item Name')}* (`{rental.get('Item ID')}`)\n"
            message += f"   👤 {rental.get('Borrower Name')} ({rental.get('Telegram Username')})\n"
            message += f"   📅 Due: {rental.get('Expected Return Date')}\n"
            message += f"\n"
        
        if len(active_rentals) > 20:
            message += f"\n_...and {len(active_rentals) - 20} more_"
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Admin Panel", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        await query.edit_message_text(f"❌ Error fetching rentals: {e}")

async def view_overdue_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all overdue rentals"""
    query = update.callback_query
    await query.answer()
    
    try:
        tz = pytz.timezone(config.TIMEZONE)
        today = datetime.now(tz).date()
        
        all_logs = sheets.log_sheet.get_all_records()
        overdue_rentals = []
        
        for log in all_logs:
            if log.get('Status', '').upper() == 'ACTIVE':
                expected_return = log.get('Expected Return Date', '')
                try:
                    return_date = datetime.strptime(expected_return, '%Y-%m-%d').date()
                    if return_date < today:
                        days_overdue = (today - return_date).days
                        log['_days_overdue'] = days_overdue
                        overdue_rentals.append(log)
                except:
                    continue
        
        if not overdue_rentals:
            await query.edit_message_text(
                "✅ No overdue items! Everyone is on time. 🎉",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Back", callback_data="admin_back")
                ]])
            )
            return
        
        # Sort by days overdue (most overdue first)
        overdue_rentals.sort(key=lambda x: x['_days_overdue'], reverse=True)
        
        message = f"⚠️ *Overdue Items ({len(overdue_rentals)})*\n\n"
        
        for idx, rental in enumerate(overdue_rentals[:15], 1):
            days = rental['_days_overdue']
            message += f"{idx}. *{rental.get('Item Name')}* (`{rental.get('Item ID')}`)\n"
            message += f"   👤 {rental.get('Borrower Name')} ({rental.get('Telegram Username')})\n"
            message += f"   📅 Due: {rental.get('Expected Return Date')}\n"
            message += f"   🚨 *{days} day{'s' if days > 1 else ''} overdue*\n\n"
        
        if len(overdue_rentals) > 15:
            message += f"\n_...and {len(overdue_rentals) - 15} more_"
        
        keyboard = [
            [InlineKeyboardButton("📢 Notify All Overdue", callback_data="admin_notify_overdue")],
            [InlineKeyboardButton("🔙 Back to Admin Panel", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        await query.edit_message_text(f"❌ Error fetching overdue items: {e}")

async def view_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View usage statistics"""
    query = update.callback_query
    await query.answer()
    
    try:
        all_logs = sheets.log_sheet.get_all_records()
        
        total_rentals = len(all_logs)
        active_rentals = len([log for log in all_logs if log.get('Status', '').upper() == 'ACTIVE'])
        completed_rentals = len([log for log in all_logs if log.get('Status', '').upper() == 'RETURNED'])
        
        # Count unique users
        unique_users = len(set(log.get('User ID', '') for log in all_logs if log.get('User ID')))
        
        # Most rented items
        item_counts = {}
        for log in all_logs:
            item_id = log.get('Item ID', '')
            if item_id:
                item_counts[item_id] = item_counts.get(item_id, 0) + 1
        
        top_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate on-time return rate
        on_time_returns = 0
        late_returns = 0
        
        for log in all_logs:
            if log.get('Status', '').upper() == 'RETURNED':
                try:
                    expected = datetime.strptime(log.get('Expected Return Date', ''), '%Y-%m-%d')
                    actual = datetime.strptime(log.get('Actual Return Date', ''), '%Y-%m-%d %H:%M:%S')
                    
                    if actual.date() <= expected.date():
                        on_time_returns += 1
                    else:
                        late_returns += 1
                except:
                    continue
        
        total_completed = on_time_returns + late_returns
        on_time_rate = (on_time_returns / total_completed * 100) if total_completed > 0 else 0
        
        message = "📊 *Usage Statistics*\n\n"
        message += f"📦 Total Rentals: *{total_rentals}*\n"
        message += f"🟢 Active: *{active_rentals}*\n"
        message += f"✅ Completed: *{completed_rentals}*\n"
        message += f"👥 Unique Users: *{unique_users}*\n"
        message += f"⏱️ On-Time Return Rate: *{on_time_rate:.1f}%*\n\n"
        
        if top_items:
            message += "🔥 *Most Rented Items:*\n"
            for idx, (item_id, count) in enumerate(top_items, 1):
                message += f"{idx}. `{item_id}` - {count} rental{'s' if count > 1 else ''}\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Admin Panel", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        await query.edit_message_text(f"❌ Error generating statistics: {e}")

async def admin_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to admin panel"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📊 All Active Rentals", callback_data="admin_all_rentals"),
            InlineKeyboardButton("⏰ Overdue Items", callback_data="admin_overdue")
        ],
        [
            InlineKeyboardButton("📈 Statistics", callback_data="admin_stats"),
            InlineKeyboardButton("👥 User Activity", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton("🔄 Force Return", callback_data="admin_force_return"),
            InlineKeyboardButton("🔍 Search User", callback_data="admin_search_user")
        ],
        [
            InlineKeyboardButton("📢 Broadcast Message", callback_data="admin_broadcast"),
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

async def admin_close(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Close admin panel"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Admin panel closed.")

async def notify_overdue_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send notifications to all overdue users"""
    query = update.callback_query
    await query.answer("Sending notifications to overdue users...")
    
    try:
        from telegram import Bot
        bot = context.bot
        
        tz = pytz.timezone(config.TIMEZONE)
        today = datetime.now(tz).date()
        
        all_logs = sheets.log_sheet.get_all_records()
        overdue_rentals = []
        
        for log in all_logs:
            if log.get('Status', '').upper() == 'ACTIVE':
                expected_return = log.get('Expected Return Date', '')
                try:
                    return_date = datetime.strptime(expected_return, '%Y-%m-%d').date()
                    if return_date < today:
                        days_overdue = (today - return_date).days
                        log['_days_overdue'] = days_overdue
                        overdue_rentals.append(log)
                except:
                    continue
        
        sent_count = 0
        for rental in overdue_rentals:
            try:
                user_id = int(rental.get('User ID', 0))
                if user_id:
                    days = rental['_days_overdue']
                    message = f"""
🚨 *OVERDUE EQUIPMENT REMINDER*

📦 Item: {rental.get('Item Name')}
🆔 Item ID: `{rental.get('Item ID')}`
📅 Was due: {rental.get('Expected Return Date')}
⚠️ *{days} day{'s' if days > 1 else ''} overdue*

Please return this item as soon as possible!
Use /return to complete the return process.

Thank you! 🙏
                    """
                    await bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                    sent_count += 1
            except Exception as e:
                print(f"Failed to notify user {user_id}: {e}")
                continue
        
        await query.edit_message_text(
            f"✅ Sent {sent_count} overdue notification(s)!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back", callback_data="admin_back")
            ]])
        )
        
    except Exception as e:
        await query.edit_message_text(f"❌ Error sending notifications: {e}")

