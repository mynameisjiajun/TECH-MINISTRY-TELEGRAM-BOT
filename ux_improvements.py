"""
UX Improvements Module
Provides enhanced user experience features with inline keyboards and browsing
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sheets_manager import SheetsManager

sheets = SheetsManager()

async def browse_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Browse available items by category"""
    # Get all items from inventory
    try:
        all_items = sheets.inventory_sheet.get_all_records()
        
        if not all_items:
            await update.message.reply_text("❌ No items found in inventory.")
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
        
        keyboard.append([InlineKeyboardButton("🔍 Search by Name", callback_data="browse_search")])
        keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="browse_cancel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📦 *Browse Equipment*\n\n"
            "Select a category to view available items:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error loading items: {e}")

async def show_category_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show items in a specific category"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.replace("browse_category_", "")
    
    try:
        all_items = sheets.inventory_sheet.get_all_records()
        category_items = [item for item in all_items if item.get('Type', '') == category]
        
        if not category_items:
            await query.edit_message_text(
                f"❌ No items found in category: {category}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Back to Categories", callback_data="browse_back")
                ]])
            )
            return
        
        message = f"📦 *{category}*\n\n"
        keyboard = []
        
        for item in category_items[:20]:  # Limit to 20 items
            item_id = item.get('ItemID', '')
            item_name = item.get('Item Name', '')
            quantity = item.get('Quantity', 0)
            
            # Check availability
            available, avail_qty, _ = sheets.check_availability(item_id)
            
            if available:
                status = f"🟢 {avail_qty} available"
            else:
                status = "🔴 All rented"
            
            message += f"• *{item_name}* (`{item_id}`)\n"
            message += f"  {status} | {item.get('Brand', 'N/A')} {item.get('Model', '')}\n\n"
            
            # Add button for this item
            keyboard.append([
                InlineKeyboardButton(
                    f"Rent {item_id} - {item_name[:20]}",
                    callback_data=f"rent_item_{item_id}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Categories", callback_data="browse_back")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    except Exception as e:
        await query.edit_message_text(f"❌ Error loading category: {e}")

async def browse_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to category selection"""
    query = update.callback_query
    await query.answer()
    
    try:
        all_items = sheets.inventory_sheet.get_all_records()
        
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
        
        keyboard.append([InlineKeyboardButton("🔍 Search by Name", callback_data="browse_search")])
        keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="browse_cancel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📦 *Browse Equipment*\n\n"
            "Select a category to view available items:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    except Exception as e:
        await query.edit_message_text(f"❌ Error: {e}")

async def browse_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel browsing"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Browse cancelled. Use /browse to browse again!")

async def start_rent_from_browse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start rental process from browse selection"""
    query = update.callback_query
    await query.answer()
    
    item_id = query.data.replace("rent_item_", "")
    
    # Check availability
    available, quantity, item = sheets.check_availability(item_id)
    
    if not item:
        await query.edit_message_text(f"❌ Item `{item_id}` not found.")
        return
    
    if not available:
        await query.edit_message_text(
            f"❌ Sorry, *{item.get('Item Name')}* is currently not available.\n\n"
            f"All units are rented out. Please try again later.",
            parse_mode='Markdown'
        )
        return
    
    # Store item details in context
    context.user_data['rental_item_id'] = item_id
    context.user_data['rental_item_name'] = item.get('Item Name')
    context.user_data['rental_item_type'] = item.get('Type')
    context.user_data['rental_item_brand'] = item.get('Brand')
    context.user_data['rental_item_model'] = item.get('Model')
    context.user_data['rental_item_location'] = item.get('Location')
    context.user_data['from_browse'] = True
    
    # Show item details with duration options
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
        [InlineKeyboardButton("📝 Custom duration", callback_data="duration_custom")],
        [InlineKeyboardButton("❌ Cancel", callback_data="rent_cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    item_details = f"""
✅ *Selected: {item.get('Item Name')}*

📦 *Item Details:*
• ID: `{item_id}`
• Type: {item.get('Type')}
• Brand: {item.get('Brand', 'N/A')}
• Model: {item.get('Model', 'N/A')}
• Available: {quantity} unit(s)
• Location: {item.get('Location')}

⏱️ *How long do you need it?*
Select a duration or choose custom:
    """
    
    await query.edit_message_text(item_details, parse_mode='Markdown', reply_markup=reply_markup)
    
    return "WAITING_FOR_DURATION_SELECTION"

