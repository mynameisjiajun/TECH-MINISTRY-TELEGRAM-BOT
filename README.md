# 🙏 Church Tech Ministry Equipment Rental Bot

A Telegram bot that helps church members rent and return equipment from your tech ministry. The bot integrates with Google Sheets to track inventory and log all transactions.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)

**Version 2.1.0** - Enhanced with Admin Features & Simplified UX

## ✨ Features

- 📦 **Easy Equipment Rental** - Users can rent items by providing an Item ID
- 📸 **Photo Verification** - Requires pickup and return photos for accountability
- 📊 **Google Sheets Integration** - Real-time inventory tracking and transaction logging
- 🔔 **Automated Reminders** - Sends reminders 1 day before return date
- ⏰ **Early Returns** - Users can return items before the due date
- 📱 **User-Friendly** - Simple conversation-based interface

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- A Telegram account
- A Google Account with access to Google Sheets
- Google Cloud Project with Sheets API enabled

### 2. Create Your Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the prompts to name your bot
4. Save the **Bot Token** - you'll need this later

### 3. Set Up Google Sheets

#### A. Create Your Spreadsheet

Create a new Google Sheet with **two sheets**:

**Sheet 1: "Available Items"** (or your preferred name)
- Column headers: `ItemID | Item Name | Type | Brand | Model | Quantity | Location`
- Example row: `CAB001 | XLR Cable 3m | Cable | Neutrik | NC3MXX | 5 | Shelf A1`

**Sheet 2: "Rental Log"** (or your preferred name)
- Column headers: `Borrower Name | Telegram Username | User ID | Item ID | Item Name | Rental Start Date | Expected Return Date | Actual Return Date | Status | Pickup Photo | Return Photo`
- This will be auto-populated by the bot

#### B. Enable Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Sheets API** and **Google Drive API**
4. Go to **Credentials** → **Create Credentials** → **Service Account**
5. Create a service account with a name (e.g., "telegram-bot")
6. Click on the created service account
7. Go to **Keys** tab → **Add Key** → **Create New Key** → **JSON**
8. Download the JSON file and save it as `credentials.json` in your project folder

#### C. Share Your Spreadsheet

1. Open your Google Sheet
2. Click **Share**
3. Add the service account email (found in `credentials.json` as `client_email`)
4. Give it **Editor** permissions

#### D. Get Your Spreadsheet ID

From your Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit
```
Copy the `YOUR_SPREADSHEET_ID` part

### 4. Install Dependencies

```bash
# Clone or download this repository
cd TECH-MINISTRY-TELEGRAM-BOT

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 5. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your details:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
GOOGLE_SHEETS_ID=your_spreadsheet_id
INVENTORY_SHEET_NAME=Available Items
LOG_SHEET_NAME=Rental Log
TIMEZONE=Asia/Singapore
```

### 6. Place Your Credentials File

Make sure `credentials.json` (downloaded from Google Cloud) is in the project root directory.

### 7. Run the Bot

```bash
# Option 1: Using run.py (recommended)
python run.py

# Option 2: Direct execution
python src/main.py
```

You should see:
```
==================================================
🙏 Church Tech Ministry Equipment Rental Bot
==================================================
✅ Successfully connected to Google Sheets
✅ Reminder scheduler started (runs daily at 9:00 AM)
🤖 Bot is running...
Press Ctrl+C to stop
==================================================
```

## 📱 How to Use (For Church Members)

### Renting Equipment

1. Start a chat with your bot on Telegram
2. Send `/start` to see available commands
3. Send `/rent` to begin renting
4. Enter the **Item ID** (e.g., `CAB001`)
5. Enter the **duration** in days (e.g., `3`)
6. Take a **photo** of the item you're picking up
7. Done! You'll receive confirmation with location details

### Viewing Active Rentals

- Send `/myrentals` to see all your active rentals

### Returning Equipment

1. Send `/return` command
2. Select which item you want to return (by number)
3. Take a **photo** of the returned item
4. Done! The system will update automatically

### Getting Help

- Send `/help` to see all available commands

## 🔧 Configuration

### Changing Reminder Time

Edit `reminder_scheduler.py` and modify the schedule:

```python
self.scheduler.add_job(
    self.send_reminders,
    'cron',
    hour=9,  # Change this to your preferred hour (0-23)
    minute=0,  # Change this to your preferred minute (0-59)
    timezone=config.TIMEZONE
)
```

### Changing Sheet Column Names

If your Google Sheet has different column names, update `config.py`:

```python
INVENTORY_COLUMNS = {
    'ITEM_ID': 0,
    'ITEM_NAME': 1,
    'TYPE': 2,
    # ... adjust as needed
}
```

## 🚀 Deployment Options

### Option 1: Run on Your Computer

- Simple: Just run `python main.py`
- Limitation: Bot stops when computer is off

### Option 2: Railway (Recommended - Free Tier Available)

1. Create account at [railway.app](https://railway.app)
2. Create new project from GitHub
3. Add environment variables in Railway dashboard
4. Add `credentials.json` content as an environment variable
5. Deploy!

### Option 3: Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
worker: python main.py
```
3. Deploy:
```bash
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
# ... set other env vars
git push heroku main
heroku ps:scale worker=1
```

### Option 4: Raspberry Pi / Home Server

- Install Python 3.8+
- Clone repo and follow setup steps
- Use `systemd` or `supervisor` to run as service
- Keep it running 24/7

## 📋 Google Sheets Structure Example

### Available Items Sheet

| ItemID | Item Name | Type | Brand | Model | Quantity | Location |
|--------|-----------|------|-------|-------|----------|----------|
| CAB001 | XLR Cable 3m | Cable | Neutrik | NC3MXX | 5 | Shelf A1 |
| CAB002 | SDI Cable 10m | Cable | Canare | L-5CFW | 3 | Shelf A2 |
| MIC001 | Wireless Mic | Microphone | Shure | SM58 | 2 | Drawer B1 |
| CAM001 | HDMI Camera | Camera | Sony | Alpha | 1 | Cabinet C1 |

### Rental Log Sheet (Auto-populated)

| Borrower Name | Telegram Username | User ID | Item ID | Item Name | Rental Start Date | Expected Return Date | Actual Return Date | Status | Pickup Photo | Return Photo |
|--------------|-------------------|---------|---------|-----------|-------------------|---------------------|-------------------|--------|--------------|--------------|
| John Doe | @johndoe | 123456789 | CAB001 | XLR Cable 3m | 2024-01-15 10:30:00 | 2024-01-18 | | ACTIVE | https://... | |
| Jane Smith | @janesmith | 987654321 | MIC001 | Wireless Mic | 2024-01-14 09:00:00 | 2024-01-17 | 2024-01-16 14:30:00 | RETURNED | https://... | https://... |

## 🛠️ Troubleshooting

### Bot doesn't respond
- Check if bot is running: `python main.py`
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Make sure you've started the bot with `/start`

### Can't connect to Google Sheets
- Verify `credentials.json` is in the project folder
- Check if service account email has Editor access to the sheet
- Verify `GOOGLE_SHEETS_ID` is correct
- Ensure Google Sheets API and Drive API are enabled

### Reminders not sending
- Check timezone setting in `.env`
- Verify user IDs are being stored (format: `ID:123456`)
- Check bot logs for errors

### Photos not saving
- Photos are stored as Telegram file URLs
- They remain accessible through Telegram's servers
- Make sure bot has storage permissions

## 📝 Notes

- The bot stores photo URLs from Telegram in the Google Sheet
- Users need to have started a chat with the bot before they can receive reminders
- Item IDs are case-insensitive (CAB001 = cab001)
- Make sure to keep `credentials.json` secure and never commit it to Git

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Google Sheets column names match configuration
3. Check bot logs for error messages
4. Ensure all dependencies are installed correctly

## 📄 License

This project is open source and available for church and ministry use.

---

**Made with ❤️ for Church Tech Ministry**
