# ⚡ Quick Reference Card

## 🚀 Getting Started

### **First Time Setup**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure .env file
# Add: TELEGRAM_BOT_TOKEN, GOOGLE_SHEETS_ID, ADMIN_USER_IDS

# 3. Add credentials.json (from Google Cloud)

# 4. Run enhanced version
python main_enhanced.py
```

---

## 👥 User Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Main menu with buttons | Interactive menu |
| `/rent` | Rent equipment | Enter Item ID |
| `/list` | View equipment list | Google Sheets link |
| `/myrentals` | View active rentals | Your current items |
| `/return` | Return equipment | Select item to return |
| `/help` | Get help | Show instructions |
| `/cancel` | Cancel operation | Exit current task |

---

## 🔧 Admin Commands

| Command | Description | Who Can Use |
|---------|-------------|-------------|
| `/admin` | Admin control panel | Admins only |

### **Admin Panel Options:**
- 📊 **All Active Rentals** - See everything
- ⏰ **Overdue Items** - Track late returns
- 📈 **Statistics** - Usage analytics
- 📢 **Notify Overdue** - Send reminders

---

## 📁 File Structure

### **Run the Bot:**
```bash
python main_enhanced.py    # Enhanced version (recommended)
python main.py             # Original version
```

### **Test Connections:**
```bash
python test_connection.py
```

### **Key Files:**
- `main_enhanced.py` - Enhanced bot entry point
- `bot_enhanced.py` - Enhanced bot logic
- `admin_commands.py` - Admin features
- `ux_improvements.py` - UX features
- `sheets_manager.py` - Google Sheets integration
- `config.py` - Configuration
- `.env` - Your settings

---

## ⚙️ Configuration (.env)

```env
# Required
TELEGRAM_BOT_TOKEN=your_token_here
GOOGLE_SHEETS_ID=your_sheet_id_here

# Sheet Names
INVENTORY_SHEET_NAME=Available Items
LOG_SHEET_NAME=Rental Log

# Timezone
TIMEZONE=Asia/Singapore

# Admin
ADMIN_USER_IDS=123456789,987654321

# Equipment List Link (NEW!)
PUBLIC_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_ID/edit
```

### **Get Your User ID:**
1. Message `@userinfobot` on Telegram
2. Copy the number

---

## 📊 Google Sheets Structure

### **Sheet 1: "Available Items"**
```
ItemID | Item Name | Type | Brand | Model | Quantity | Location
CAB001 | XLR Cable | Cable | Neutrik | NC3MXX | 5 | Shelf A1
```

### **Sheet 2: "Rental Log"** (auto-filled)
```
Borrower Name | Telegram Username | User ID | Item ID | Item Name | 
Rental Start Date | Expected Return Date | Actual Return Date | 
Status | Pickup Photo | Return Photo
```

---

## 🎯 Common Tasks

### **Add New Equipment**
1. Open Google Sheets "Available Items"
2. Add new row with item details
3. Save - bot will see it immediately

### **Make Someone Admin**
1. Get their User ID from @userinfobot
2. Add to `.env`: `ADMIN_USER_IDS=123,456,789`
3. Restart bot

### **Check Overdue Items**
```
/admin → Overdue Items
```

### **Send Reminders**
```
/admin → Overdue Items → Notify All
```

### **View Statistics**
```
/admin → Statistics
```

### **Force Return (Manual)**
1. Open Google Sheets "Rental Log"
2. Find the rental row
3. Change Status to "RETURNED"
4. Add Actual Return Date

---

## 🐛 Troubleshooting

### **Bot Not Responding**
```bash
# Check if running
ps aux | grep python

# Restart
python main_enhanced.py
```

### **Admin Panel Not Showing**
```bash
# Check .env
cat .env | grep ADMIN_USER_IDS

# Should show your User ID
# Restart bot after changes
```

### **Can't Connect to Sheets**
- Check `credentials.json` exists
- Verify sheet is shared with service account email
- Check `GOOGLE_SHEETS_ID` in `.env`

### **Photos Not Saving**
- Photos are stored as Telegram URLs
- Check Google Sheets for URLs
- URLs remain accessible via Telegram

---

## 📈 Admin Daily Routine

### **Morning (2 mins)**
```
/admin → Overdue Items
```
Check if anyone's late

### **Weekly (10 mins)**
```
/admin → Overdue Items → Notify All
/admin → Statistics
```
Send reminders, review stats

### **Monthly (30 mins)**
```
/admin → Statistics
Export Google Sheets data
Create report for ministry
```

---

## 🎨 User Flow (Enhanced)

### **Renting:**
```
/start or /rent
  ↓
[Browse] or [Enter ID]
  ↓
Select category (if browsing)
  ↓
Tap item [Rent] button
  ↓
Tap duration [3 days]
  ↓
Send photo
  ↓
✅ Confirmed!
```

### **Returning:**
```
/return
  ↓
Select item from list
  ↓
Send photo
  ↓
✅ Returned!
```

---

## 📚 Documentation Quick Links

| Document | Purpose |
|----------|---------|
| `QUICKSTART.md` | 15-min setup |
| `UPGRADE_GUIDE.md` | Enable new features |
| `ADMIN_GUIDE.md` | Admin manual |
| `WHATS_NEW.md` | New features |
| `FAQ.md` | Common questions |
| `README.md` | Full documentation |

---

## 🔑 Important URLs

### **Get Bot Token:**
- Telegram: `@BotFather`

### **Get User ID:**
- Telegram: `@userinfobot`

### **Google Cloud Console:**
- https://console.cloud.google.com

### **Google Sheets:**
- https://sheets.google.com

---

## 💡 Quick Tips

### **For Users:**
- 🔘 Use buttons (faster than typing!)
- 📦 Browse to discover equipment
- 📋 Check "My Rentals" regularly
- ⏰ Return on time

### **For Admins:**
- 📊 Check `/admin` daily
- 📢 Remind overdue users weekly
- 📈 Review stats monthly
- 💾 Backup sheets regularly

---

## 🆘 Emergency Contacts

### **Bot Issues:**
1. Check terminal for errors
2. Run `python test_connection.py`
3. Review documentation
4. Check `.env` configuration

### **Lost Equipment:**
1. Check `/admin` → All Rentals
2. Contact user via Telegram
3. Document in your records

### **System Down:**
1. Check if bot is running
2. Verify internet connection
3. Check Google Sheets access
4. Restart bot

---

## 📞 Support Checklist

Before asking for help:
- [ ] Read error message in terminal
- [ ] Check relevant documentation
- [ ] Verify `.env` configuration
- [ ] Test with `test_connection.py`
- [ ] Check Google Sheets access
- [ ] Restart bot

---

## 🎯 Success Metrics

### **Good Performance:**
- ✅ On-time return rate > 85%
- ✅ Active users growing
- ✅ Equipment utilization > 50%
- ✅ Overdue items < 5%

### **Need Improvement:**
- ⚠️ On-time rate < 70%
- ⚠️ Many overdue items
- ⚠️ Low equipment usage
- ⚠️ Frequent user complaints

---

## 🚀 Version Info

**Current Version:** 2.0.0 (Enhanced)

**Features:**
- ✅ Inline keyboards
- ✅ Browse by category
- ✅ Admin panel
- ✅ Overdue tracking
- ✅ Usage statistics

**Run Command:**
```bash
python main_enhanced.py
```

---

## 📱 Command Cheat Sheet

```
USER COMMANDS:
/start      - Main menu
/rent       - Rent equipment (enter Item ID)
/list       - View equipment list (Google Sheet)
/myrentals  - My active rentals
/return     - Return equipment
/help       - Get help
/cancel     - Cancel operation

ADMIN COMMANDS:
/admin      - Admin panel
  ├─ All Active Rentals
  ├─ Overdue Items
  ├─ Statistics
  └─ Notify Overdue Users
```

---

**Print this page for quick reference!** 📄

**Last Updated:** December 25, 2024  
**Version:** 2.0.0 Enhanced

