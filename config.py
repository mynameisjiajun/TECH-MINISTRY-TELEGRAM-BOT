"""
Configuration module for the Telegram Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Google Sheets Configuration
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
INVENTORY_SHEET_NAME = os.getenv('INVENTORY_SHEET_NAME', 'Available Items')
LOG_SHEET_NAME = os.getenv('LOG_SHEET_NAME', 'Rental Log')

# Timezone
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Singapore')

# Admin Configuration
# Add admin Telegram User IDs (comma-separated)
# To get your User ID, message @userinfobot on Telegram
ADMIN_USER_IDS = os.getenv('ADMIN_USER_IDS', '').split(',')
ADMIN_USER_IDS = [int(uid.strip()) for uid in ADMIN_USER_IDS if uid.strip().isdigit()]

# Public Google Sheet Link (for users to browse equipment)
# Make a view-only link to your "Available Items" sheet
PUBLIC_SHEET_URL = os.getenv('PUBLIC_SHEET_URL', '')

# Google Sheets Columns (0-indexed)
# Inventory Sheet: ItemID, Item Name, Type, Brand, Model, Quantity, Location
INVENTORY_COLUMNS = {
    'ITEM_ID': 0,
    'ITEM_NAME': 1,
    'TYPE': 2,
    'BRAND': 3,
    'MODEL': 4,
    'QUANTITY': 5,
    'LOCATION': 6
}

# Log Sheet: Borrower Name, Telegram Username, User ID, Item ID, Item Name, Rental Start Date, 
# Expected Return Date, Actual Return Date, Status, Pickup Photo, Return Photo
LOG_COLUMNS = {
    'BORROWER_NAME': 0,
    'TELEGRAM_USERNAME': 1,
    'USER_ID': 2,
    'ITEM_ID': 3,
    'ITEM_NAME': 4,
    'RENTAL_START': 5,
    'EXPECTED_RETURN': 6,
    'ACTUAL_RETURN': 7,
    'STATUS': 8,
    'PICKUP_PHOTO': 9,
    'RETURN_PHOTO': 10
}

