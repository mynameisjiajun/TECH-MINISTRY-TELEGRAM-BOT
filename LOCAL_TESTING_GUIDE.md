# 🧪 Local Testing Guide

## What You Need Before Testing

### ✅ **1. Telegram Bot Token**
- [ ] Create bot with @BotFather on Telegram
- [ ] Get the token (looks like: `123456789:ABCdefGHI...`)

### ✅ **2. Google Sheets Setup**
- [ ] Create Google Sheet with 2 sheets
- [ ] Get service account credentials (`credentials.json`)
- [ ] Share sheet with service account email
- [ ] Get your spreadsheet ID

### ✅ **3. Your Admin User ID** (Optional but recommended)
- [ ] Message @userinfobot on Telegram
- [ ] Get your User ID number

### ✅ **4. Public Sheet Link** (Optional)
- [ ] Make your "Available Items" sheet view-only
- [ ] Get the public link

---

## 📋 Step-by-Step Local Testing

### **Step 1: Install Python & Dependencies**

```bash
# Check Python version (needs 3.8+)
python3 --version

# Navigate to project folder
cd "/Users/mynameisjiajun/Documents/C Project Repo/https:/github.com/mynameisjiajun/TECH-MINISTRY-TELEGRAM-BOT.git"

# Install dependencies
pip3 install -r requirements.txt
```

---

### **Step 2: Create Your Google Sheet**

#### **Sheet 1: "Available Items"**
Create with these column headers (Row 1):
```
ItemID | Item Name | Type | Brand | Model | Quantity | Location
```

Add some test data (Row 2+):
```
CAB001 | XLR Cable 3m | Cable | Neutrik | NC3MXX | 5 | Shelf A1
MIC001 | Wireless Mic | Microphone | Shure | SM58 | 2 | Cabinet C1
CAM001 | Camera | Camera | Sony | Alpha | 1 | Cabinet D1
```

#### **Sheet 2: "Rental Log"**
Create with these column headers (Row 1):
```
Borrower Name | Telegram Username | User ID | Item ID | Item Name | Rental Start Date | Expected Return Date | Actual Return Date | Status | Pickup Photo | Return Photo
```

Leave the rest empty (bot will fill this automatically).

---

### **Step 3: Get Google Cloud Credentials**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project: "Church Tech Bot Test"
3. Enable APIs:
   - Google Sheets API
   - Google Drive API
4. Create Service Account:
   - Go to "Credentials" → "Create Credentials" → "Service Account"
   - Name: "telegram-bot"
   - Create a JSON key
   - Download and save as `credentials.json`
5. Share your Google Sheet:
   - Open the `credentials.json` file
   - Find `client_email` (looks like: `telegram-bot@...iam.gserviceaccount.com`)
   - Copy that email
   - Go to your Google Sheet → Share → Paste email → Give "Editor" access

---

### **Step 4: Create Telegram Bot**

1. Open Telegram
2. Search for `@BotFather`
3. Send: `/newbot`
4. Name: "Church Tech Test Bot"
5. Username: "your_church_tech_test_bot"
6. Copy the token

---

### **Step 5: Configure .env File**

Create/edit the `.env` file:

```env
# Telegram Bot Token (REQUIRED)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI-your-actual-token-here

# Google Sheets ID (REQUIRED)
# From URL: https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit
GOOGLE_SHEETS_ID=1A2B3C4D5E6F7G8H9I0J_your-actual-sheet-id

# Sheet Names (must match exactly!)
INVENTORY_SHEET_NAME=Available Items
LOG_SHEET_NAME=Rental Log

# Your Timezone
TIMEZONE=Asia/Singapore

# Your Admin User ID (get from @userinfobot)
ADMIN_USER_IDS=123456789

# Public Sheet URL (optional - for /list command)
PUBLIC_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0
```

---

### **Step 6: Place credentials.json**

Make sure `credentials.json` is in your project folder:
```
/Users/mynameisjiajun/Documents/C Project Repo/.../
  ├── credentials.json  ← Should be here
  ├── .env
  ├── main_enhanced.py
  └── ...
```

---

### **Step 7: Test Connections**

```bash
python3 test_connection.py
```

**Expected output:**
```
🧪 Church Tech Ministry Bot - Connection Test
==================================================
🔍 Checking Python version...
✅ Python 3.11.x (Compatible)

🔍 Checking dependencies...
✅ telegram
✅ gspread
✅ oauth2client
...

🔍 Checking .env configuration...
✅ TELEGRAM_BOT_TOKEN is set
✅ GOOGLE_SHEETS_ID is set

🔍 Checking Google credentials...
✅ credentials.json found

🔍 Testing Google Sheets connection...
✅ Successfully connected to Google Sheets
✅ Inventory sheet accessible (columns: 7)
✅ Log sheet accessible (columns: 11)

🔍 Testing Telegram bot token...
✅ Bot token is valid
   Bot name: @your_bot_username
   Bot ID: 123456789

==================================================
📊 Test Results Summary
==================================================
Python Version                ✅ PASS
Dependencies                  ✅ PASS
Environment File              ✅ PASS
Google Credentials            ✅ PASS
Google Sheets                 ✅ PASS
Telegram Bot Token            ✅ PASS
==================================================

🎉 All tests passed! You're ready to run the bot.
Run: python main_enhanced.py
==================================================
```

If any test fails, fix it before continuing!

---

### **Step 8: Run the Bot**

```bash
python3 main_enhanced.py
```

**Expected output:**
```
==================================================
🙏 Church Tech Ministry Equipment Rental Bot
   ENHANCED VERSION with Admin & UX Features
==================================================
🔑 Using credentials from file
✅ Successfully connected to Google Sheets
✅ Admin users configured: 1
✅ Equipment list URL configured
🤖 Bot is running with enhanced features...
   • Inline keyboards enabled
   • Equipment list link enabled
   • Admin panel enabled
   • Overdue tracking enabled
Press Ctrl+C to stop
==================================================
```

**Leave this terminal running!**

---

### **Step 9: Test on Telegram**

1. **Open Telegram**
2. **Find your bot** - Search for the username you created
3. **Start chatting** - Click "Start" or send `/start`

---

## 🧪 **Testing Checklist**

### **Basic Tests:**
- [ ] `/start` - Shows main menu with buttons
- [ ] `/list` - Shows equipment list button (if configured)
- [ ] `/help` - Shows help message
- [ ] Buttons work (click them)

### **Rental Flow:**
- [ ] `/rent` - Enter "CAB001"
- [ ] Bot finds the item
- [ ] Select duration (tap button)
- [ ] Send any photo
- [ ] Get confirmation message
- [ ] Check Google Sheets "Rental Log" - should have new entry

### **View Rentals:**
- [ ] `/myrentals` - Shows your active rental
- [ ] Information is correct

### **Return Flow:**
- [ ] `/return` - Shows your rental
- [ ] Select item to return
- [ ] Send any photo
- [ ] Get confirmation
- [ ] Check Google Sheets - Status should be "RETURNED"

### **Admin Tests (if you added your User ID):**
- [ ] `/admin` - Shows admin panel
- [ ] "All Active Rentals" - Shows rentals
- [ ] "Statistics" - Shows stats
- [ ] "Overdue Items" - Should be empty (or show if you have any)

---

## 🐛 **Common Issues & Solutions**

### **Issue: "Module not found"**
```bash
# Solution: Install dependencies
pip3 install -r requirements.txt
```

### **Issue: "Can't connect to Google Sheets"**
**Check:**
- [ ] `credentials.json` is in the folder
- [ ] Service account email has Editor access to sheet
- [ ] Sheet names match exactly (case-sensitive!)
- [ ] Google Sheets API is enabled

**Fix:**
```bash
# Verify credentials file exists
ls -la credentials.json

# Check .env configuration
cat .env | grep GOOGLE
```

### **Issue: "Bot doesn't respond"**
**Check:**
- [ ] Bot is running (`python3 main_enhanced.py`)
- [ ] Bot token is correct
- [ ] You sent `/start` first

**Fix:**
```bash
# Test bot token
python3 test_connection.py
```

### **Issue: "Invalid bot token"**
**Fix:** Get a new token from @BotFather:
```
/newbot - Create new bot
OR
/mybots - Select your bot → API Token
```

### **Issue: "Sheet names don't match"**
**Fix:** Check exact names in .env match your Google Sheet tabs:
```env
INVENTORY_SHEET_NAME=Available Items  ← Must match exactly!
LOG_SHEET_NAME=Rental Log
```

### **Issue: Admin panel not showing**
**Fix:** Add your User ID to .env:
```bash
# Get your ID from @userinfobot
# Add to .env:
ADMIN_USER_IDS=your_user_id_here

# Restart bot
```

---

## 📸 **Testing Screenshots**

### **What you should see:**

**On Telegram:**
```
You: /start

Bot: 🙏 Welcome to Church Tech Ministry...
     [🎯 Rent Equipment]
     [📋 My Rentals]
     [📄 View Equipment List]
     [📖 Help]
```

**In Terminal:**
```
🤖 Bot is running with enhanced features...
✅ Logged rental for CAB001 by Test User
```

**In Google Sheets:**
```
Rental Log sheet should show:
| Test User | @yourname | 123456 | CAB001 | XLR Cable | 2024-12-25... | ACTIVE | ... |
```

---

## ⚡ **Quick Commands Reference**

```bash
# Install dependencies
pip3 install -r requirements.txt

# Test everything
python3 test_connection.py

# Run the bot
python3 main_enhanced.py

# Stop the bot
Press Ctrl+C

# Check if bot is running
ps aux | grep python

# View bot logs
# (just watch the terminal output)
```

---

## 🔧 **Development Tips**

### **Make Changes:**
1. Stop bot (Ctrl+C)
2. Edit code
3. Save
4. Restart bot (`python3 main_enhanced.py`)

### **Test Different Scenarios:**
- Rent multiple items
- Try returning
- Test with different Item IDs
- Test admin commands
- Make an item "overdue" (edit Google Sheet date manually)

### **Reset Testing:**
- Clear "Rental Log" sheet (except header row)
- All items become available again

---

## 📝 **What to Check**

### **Before Going Live:**
- [ ] All commands work
- [ ] Photos upload successfully
- [ ] Google Sheets logs correctly
- [ ] Admin panel works (if configured)
- [ ] Reminders test (change dates to tomorrow, wait for 9 AM)
- [ ] Multiple users can use simultaneously
- [ ] Error messages are helpful

### **Configuration Checklist:**
- [ ] Real bot token (not test)
- [ ] Production Google Sheet
- [ ] All admin User IDs added
- [ ] Public sheet URL is view-only
- [ ] Timezone is correct
- [ ] All sheet names match

---

## 🎓 **What Each File Does**

```
main_enhanced.py      → Runs the bot (start here!)
bot_enhanced.py       → Bot commands & logic
admin_commands.py     → Admin features
list_command.py       → Equipment list link
sheets_manager.py     → Google Sheets integration
reminder_scheduler.py → Daily reminders
config.py            → Configuration
.env                 → Your settings (KEEP SECRET!)
credentials.json     → Google credentials (KEEP SECRET!)
```

---

## 🚀 **Ready to Test!**

**Summary:**
1. ✅ Install Python packages
2. ✅ Create Google Sheet (2 sheets)
3. ✅ Get Google credentials
4. ✅ Create Telegram bot
5. ✅ Configure .env file
6. ✅ Run test_connection.py
7. ✅ Run main_enhanced.py
8. ✅ Test on Telegram!

**Time needed:** 10-15 minutes

**You'll need:**
- Computer with Python 3.8+
- Internet connection
- Telegram account
- Google account

---

**Questions? Issues? Check the troubleshooting section above!**

Good luck testing! 🎉

