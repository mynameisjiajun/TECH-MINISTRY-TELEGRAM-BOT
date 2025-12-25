# 📋 Quick Setup Guide

## Step-by-Step Setup (15 minutes)

### Step 1: Create Telegram Bot (5 minutes)

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Name your bot (e.g., "Church Tech Rental Bot")
4. Choose a username (e.g., "churchtechrental_bot")
5. **Copy and save the token** that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Step 2: Set Up Google Sheets (5 minutes)

1. **Create a new Google Sheet**
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new spreadsheet
   - Name it "Tech Ministry Rentals" (or any name you prefer)

2. **Create Sheet 1: "Available Items"**
   - Rename "Sheet1" to "Available Items"
   - Add these column headers in row 1:
     ```
     ItemID | Item Name | Type | Brand | Model | Quantity | Location
     ```
   - Add your equipment (example):
     ```
     CAB001 | XLR Cable 3m | Cable | Neutrik | NC3MXX | 5 | Shelf A1
     CAB002 | SDI Cable 10m | Cable | Canare | L-5CFW | 3 | Shelf A2
     ```

3. **Create Sheet 2: "Rental Log"**
   - Click the "+" at the bottom to add a new sheet
   - Name it "Rental Log"
   - Add these column headers in row 1:
     ```
     Borrower Name | Telegram Username | User ID | Item ID | Item Name | Rental Start Date | Expected Return Date | Actual Return Date | Status | Pickup Photo | Return Photo
     ```
   - Leave the rest empty (bot will fill this automatically)

4. **Get Spreadsheet ID**
   - Look at your browser URL:
     ```
     https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J_EXAMPLE_ID/edit
     ```
   - Copy the ID part (between `/d/` and `/edit`)

### Step 3: Set Up Google Cloud (5 minutes)

1. **Go to Google Cloud Console**
   - Visit [console.cloud.google.com](https://console.cloud.google.com)
   - Sign in with your Google account

2. **Create a Project**
   - Click the project dropdown at the top
   - Click "New Project"
   - Name it "Church Tech Bot"
   - Click "Create"

3. **Enable APIs**
   - Click "Enable APIs and Services"
   - Search for "Google Sheets API" → Enable it
   - Search for "Google Drive API" → Enable it

4. **Create Service Account**
   - Go to "Credentials" (left sidebar)
   - Click "Create Credentials" → "Service Account"
   - Name: "telegram-bot"
   - Click "Create and Continue"
   - Skip the optional steps → "Done"

5. **Create JSON Key**
   - Click on your service account email
   - Go to "Keys" tab
   - "Add Key" → "Create New Key" → "JSON"
   - Save the downloaded file as `credentials.json`

6. **Share Google Sheet with Service Account**
   - Open the downloaded `credentials.json`
   - Find the `client_email` (looks like: `telegram-bot@project-name.iam.gserviceaccount.com`)
   - Copy that email
   - Go back to your Google Sheet
   - Click "Share" button
   - Paste the service account email
   - Give it "Editor" permission
   - Uncheck "Notify people"
   - Click "Share"

### Step 4: Install and Configure Bot

1. **Install Python** (if you don't have it)
   - Download from [python.org](https://python.org) (version 3.8 or higher)

2. **Download the Bot Code**
   - Download this repository or clone it

3. **Open Terminal/Command Prompt**
   - Navigate to the bot folder:
     ```bash
     cd path/to/TECH-MINISTRY-TELEGRAM-BOT
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   - Open the `.env` file in a text editor
   - Fill in your details:
     ```env
     TELEGRAM_BOT_TOKEN=paste_your_bot_token_here
     GOOGLE_SHEETS_ID=paste_your_spreadsheet_id_here
     INVENTORY_SHEET_NAME=Available Items
     LOG_SHEET_NAME=Rental Log
     TIMEZONE=Asia/Singapore
     ```
   - Save the file

6. **Place Credentials File**
   - Put `credentials.json` (from Step 3.5) in the same folder as the bot code

### Step 5: Run the Bot

```bash
python main.py
```

You should see:
```
==================================================
🙏 Church Tech Ministry Equipment Rental Bot
==================================================
✅ Successfully connected to Google Sheets
✅ Reminder scheduler started (runs daily at 9:00 AM)
🤖 Bot is running...
```

### Step 6: Test Your Bot

1. Open Telegram
2. Search for your bot username (e.g., @churchtechrental_bot)
3. Send `/start`
4. Try renting an item with `/rent`

## 🎉 You're Done!

Your bot is now ready to use. Keep the terminal window open to keep the bot running.

## 🚀 Next Steps

- **Deploy to cloud** (Railway, Heroku, etc.) so it runs 24/7
- **Add more equipment** to your Google Sheet
- **Share bot username** with your church members
- **Test all features** (rent, return, reminders)

## ⚠️ Important Files (Do NOT share publicly)

- `credentials.json` - Your Google Cloud credentials
- `.env` - Your bot token and configuration

Add these to `.gitignore` if using Git!

## 🆘 Common Issues

**"Bot doesn't respond"**
- Make sure `python main.py` is still running
- Check if bot token is correct in `.env`

**"Can't connect to Google Sheets"**
- Verify service account has Editor access to sheet
- Check if `credentials.json` is in the correct folder
- Make sure APIs are enabled in Google Cloud

**"Invalid Sheet Name"**
- Check sheet names match exactly (case-sensitive)
- Default names: "Available Items" and "Rental Log"

---

Need help? Check the main README.md for detailed documentation!

