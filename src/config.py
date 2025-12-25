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

# Google Credentials
# For local development: Use credentials.json file in root directory
# For Railway/Cloud deployment: Set GOOGLE_CREDENTIALS environment variable with JSON content
# The SheetsManager will automatically handle both cases

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

# Verification Password
# Users must enter this password to use the bot
VERIFICATION_PASSWORD = os.getenv('VERIFICATION_PASSWORD', 'HOGCgens')

# Google Sheets Columns (0-indexed)
# Inventory Sheet: ItemID, Item Name, Type, Brand, Model, Quantity, Location, Loaned Out, Quantity Current
INVENTORY_COLUMNS = {
    'ITEM_ID': 0,
    'ITEM_NAME': 1,
    'TYPE': 2,
    'BRAND': 3,
    'MODEL': 4,
    'QUANTITY': 5,
    'LOCATION': 6,
    'LOANED_OUT': 7,
    'QUANTITY_CURRENT': 8
}

# Log Sheet: Date & Time, Borrower Name, Telegram Username, User ID, Item ID, Quantity,
# Rental Start Date, Expected Return Date, Actual Return Date, Status, Pickup Photo, Return Photo
# NOTE: Each row is ONE rental. Multiple different items = multiple rows
LOG_COLUMNS = {
    'DATE_TIME': 0,
    'BORROWER_NAME': 1,
    'TELEGRAM_USERNAME': 2,
    'USER_ID': 3,
    'ITEM_ID': 4,
    'QUANTITY': 5,
    'RENTAL_START': 6,
    'EXPECTED_RETURN': 7,
    'ACTUAL_RETURN': 8,
    'STATUS': 9,
    'PICKUP_PHOTO': 10,
    'RETURN_PHOTO': 11
}

