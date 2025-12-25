# ⚡ Quick Start Guide (15 Minutes)

Get your bot running in 15 minutes or less!

---

## 📝 Before You Start

You'll need:
- [ ] A computer with internet
- [ ] A Telegram account
- [ ] A Google account
- [ ] 15 minutes of time

---

## 🚀 Step 1: Create Telegram Bot (2 minutes)

1. Open Telegram
2. Search for `@BotFather`
3. Send: `/newbot`
4. Name your bot: `Church Tech Rental Bot`
5. Username: `your_church_tech_bot` (must be unique)
6. **Copy the token** (looks like: `123456789:ABCdefGHI...`)
7. **Save it somewhere safe!**

---

## 📊 Step 2: Create Google Sheet (3 minutes)

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create new spreadsheet

**First Sheet: "Available Items"**
- Rename Sheet1 to: `Available Items`
- Add headers in Row 1:
  ```
  ItemID | Item Name | Type | Brand | Model | Quantity | Location
  ```
- Add sample item in Row 2:
  ```
  CAB001 | XLR Cable | Cable | Neutrik | NC3MXX | 5 | Shelf A1
  ```

**Second Sheet: "Rental Log"**
- Click `+` to add new sheet
- Name it: `Rental Log`
- Add headers in Row 1:
  ```
  Borrower Name | Telegram Username | User ID | Item ID | Item Name | Rental Start Date | Expected Return Date | Actual Return Date | Status | Pickup Photo | Return Photo
  ```
- Leave other rows empty

3. **Copy the Sheet ID** from URL:
   ```
   https://docs.google.com/spreadsheets/d/COPY_THIS_PART/edit
   ```

---

## 🔑 Step 3: Set Up Google API (5 minutes)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create new project: `Church Tech Bot`
3. Click "Enable APIs and Services"
4. Search and enable: `Google Sheets API`
5. Search and enable: `Google Drive API`
6. Go to "Credentials" → "Create Credentials" → "Service Account"
7. Name: `telegram-bot` → Create
8. Click on the service account email
9. Go to "Keys" → "Add Key" → "Create New Key" → "JSON"
10. **Download the file**
11. **Rename it to:** `credentials.json`

**Share Sheet with Bot:**
1. Open `credentials.json`
2. Find `client_email` (looks like: `telegram-bot@...iam.gserviceaccount.com`)
3. Copy that email
4. Open your Google Sheet
5. Click "Share"
6. Paste the email
7. Give "Editor" permission
8. Uncheck "Notify people"
9. Click "Share"

---

## 💻 Step 4: Download & Setup Bot (3 minutes)

1. **Download this project** to your computer
2. **Move `credentials.json`** into the project folder
3. **Open `.env` file** in a text editor
4. **Fill in your details:**
   ```env
   TELEGRAM_BOT_TOKEN=paste_your_bot_token_here
   GOOGLE_SHEETS_ID=paste_your_sheet_id_here
   INVENTORY_SHEET_NAME=Available Items
   LOG_SHEET_NAME=Rental Log
   TIMEZONE=Asia/Singapore
   ```
5. **Save the file**

---

## ▶️ Step 5: Install & Run (2 minutes)

### macOS / Linux:
```bash
cd path/to/TECH-MINISTRY-TELEGRAM-BOT
pip3 install -r requirements.txt
python3 main.py
```

### Windows:
```cmd
cd path\to\TECH-MINISTRY-TELEGRAM-BOT
pip install -r requirements.txt
python main.py
```

### OR use the quick start script:

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

---

## ✅ Step 6: Test Your Bot (2 minutes)

1. Open Telegram
2. Search for your bot username
3. Click "Start" or send `/start`
4. You should see a welcome message!

**Try renting:**
1. Send: `/rent`
2. Enter: `CAB001`
3. Enter: `3` (days)
4. Send any photo
5. You should get confirmation!

**Check Google Sheet:**
- Go to "Rental Log" sheet
- You should see your test rental logged!

---

## 🎉 Success!

Your bot is now running! 

**Important:** 
- Keep the terminal/command prompt window open
- The bot runs as long as this window is open
- To stop: Press `Ctrl+C`

---

## 🚀 Next Steps

### 1. Keep Bot Running 24/7
Right now, bot only runs when your computer is on. To run 24/7:
- Deploy to Railway (free) - See DEPLOYMENT.md
- Or use a Raspberry Pi
- Or use cloud hosting

### 2. Add Your Equipment
- Open Google Sheet "Available Items"
- Add your actual equipment
- Use the example_inventory.csv as reference

### 3. Share with Team
- Give your bot username to church members
- They can start using it immediately!

### 4. Customize
- Edit reminder time in `reminder_scheduler.py`
- Customize messages in `bot.py`
- Adjust timezone in `.env`

---

## ⚠️ Troubleshooting

### "Bot doesn't respond"
- Is `python main.py` still running?
- Did you start the bot with `/start` first?
- Check the terminal for error messages

### "Can't connect to Google Sheets"
- Did you share the sheet with service account email?
- Is `credentials.json` in the right folder?
- Are both APIs enabled in Google Cloud?

### "Invalid token"
- Check if bot token in `.env` is correct
- Make sure there are no spaces or quotes around it

### "Module not found"
- Run: `pip install -r requirements.txt`
- Make sure you're in the right folder

### Still stuck?
- Run: `python test_connection.py` to diagnose issues
- Check FAQ.md
- Check SETUP_GUIDE.md for detailed help

---

## 📚 Documentation

- **README.md** - Full documentation
- **SETUP_GUIDE.md** - Detailed setup
- **DEPLOYMENT.md** - Hosting options
- **FAQ.md** - Common questions
- **PROJECT_OVERVIEW.md** - Technical overview

---

## 🎯 What You Just Built

✅ A Telegram bot that manages equipment rentals  
✅ Automatic logging to Google Sheets  
✅ Photo verification system  
✅ Automated reminder system  
✅ Easy return process  
✅ Real-time inventory tracking  

**Pretty cool, right?** 😎

---

**Need help?** Check FAQ.md or other documentation files!

**Ready to deploy 24/7?** Check DEPLOYMENT.md!

**Happy renting!** 🙏

