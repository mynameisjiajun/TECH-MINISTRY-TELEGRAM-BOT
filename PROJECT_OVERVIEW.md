# 📋 Project Overview

## Church Tech Ministry Equipment Rental Bot

A complete Telegram bot solution for managing equipment rentals in church tech ministries.

---

## 🎯 Project Goals

1. **Simplify Equipment Tracking** - Replace manual tracking with automated system
2. **Improve Accountability** - Photo verification for pickups and returns
3. **Reduce Lost Equipment** - Automated reminders before return dates
4. **Easy to Use** - Simple Telegram interface, no app installation needed
5. **Transparent Logging** - All transactions logged in Google Sheets

---

## 📁 Project Structure

```
TECH-MINISTRY-TELEGRAM-BOT/
│
├── 📄 main.py                  # Main entry point (runs bot + scheduler)
├── 🤖 bot.py                   # Telegram bot logic and commands
├── 📊 sheets_manager.py        # Google Sheets integration
├── ⏰ reminder_scheduler.py    # Automated reminder system
├── ⚙️  config.py                # Configuration and constants
│
├── 📋 requirements.txt         # Python dependencies
├── 🌍 .env                     # Environment variables (your config)
├── 🔑 credentials.json         # Google Service Account credentials
│
├── 🚀 start.sh                 # Quick start script (Mac/Linux)
├── 🚀 start.bat                # Quick start script (Windows)
├── 🧪 test_connection.py       # Connection test script
│
├── 📖 README.md                # Main documentation
├── 📖 SETUP_GUIDE.md           # Step-by-step setup instructions
├── 📖 DEPLOYMENT.md            # Deployment options guide
├── 📖 FAQ.md                   # Frequently asked questions
├── 📖 CHANGELOG.md             # Version history
│
├── 📄 example_inventory.csv    # Sample inventory data
├── 📄 GOOGLE_SHEETS_TEMPLATE.txt # Sheet structure guide
│
├── 🚫 .gitignore               # Git ignore rules
├── 📜 LICENSE                  # MIT License
├── 📦 Procfile                 # For Heroku/Railway deployment
└── 🐍 runtime.txt              # Python version for deployment
```

---

## 🔧 Core Components

### 1. **bot.py** - Telegram Bot Interface
- Handles all user interactions
- Conversation flow for rentals and returns
- Command handlers (/start, /rent, /return, etc.)
- Photo processing
- User-friendly error messages

### 2. **sheets_manager.py** - Google Sheets Manager
- Connects to Google Sheets API
- Checks item availability
- Logs rental transactions
- Tracks active rentals
- Updates return information
- Queries for due items

### 3. **reminder_scheduler.py** - Automated Reminders
- Background scheduler
- Checks daily for items due tomorrow
- Sends Telegram messages to users
- Configurable reminder time

### 4. **config.py** - Configuration
- Environment variable loading
- Sheet column mappings
- Constants and settings
- Easy to modify

### 5. **main.py** - Application Entry Point
- Initializes bot
- Starts reminder scheduler
- Combines all components
- Error handling

---

## 📊 Data Flow

### Rental Process:
```
User → /rent command
  ↓
Bot asks for Item ID
  ↓
User provides Item ID
  ↓
Bot checks Google Sheets availability
  ↓
Bot asks for duration
  ↓
User provides duration (days)
  ↓
Bot shows location & asks for photo
  ↓
User sends photo
  ↓
Bot logs to Google Sheets
  ↓
User receives confirmation
```

### Return Process:
```
User → /return command
  ↓
Bot fetches user's active rentals from Google Sheets
  ↓
Bot displays list of rentals
  ↓
User selects item to return
  ↓
Bot asks for return photo
  ↓
User sends photo
  ↓
Bot updates Google Sheets (status → RETURNED)
  ↓
User receives confirmation
```

### Reminder Process:
```
Scheduler runs daily (9 AM)
  ↓
Queries Google Sheets for items due tomorrow
  ↓
For each due item:
  ↓
Send Telegram message to user
  ↓
User receives reminder notification
```

---

## 🗂️ Google Sheets Structure

### Sheet 1: "Available Items"
- **Purpose:** Inventory database
- **Columns:** ItemID, Item Name, Type, Brand, Model, Quantity, Location
- **Managed by:** Admins (manual updates)
- **Used by:** Bot (reads for availability checks)

### Sheet 2: "Rental Log"
- **Purpose:** Transaction history
- **Columns:** Borrower Name, Telegram Username, User ID, Item ID, Item Name, Rental Start, Expected Return, Actual Return, Status, Pickup Photo, Return Photo
- **Managed by:** Bot (automatic)
- **Used by:** Admins (monitoring), Bot (active rental checks, reminders)

---

## 🔐 Security & Privacy

### What's Stored:
- User's Telegram name and username
- User ID (for sending reminders)
- Item rental history
- Photo URLs (hosted by Telegram)
- Rental dates and durations

### What's NOT Stored:
- Payment information
- Personal contact details beyond Telegram
- Chat history
- Private messages

### Security Measures:
- Service Account authentication (not personal Google account)
- Environment variables for sensitive data
- .gitignore prevents credential commits
- Minimal data collection
- No public access to sheets

---

## 🚀 Deployment Options Comparison

| Option | Cost | Difficulty | Uptime | Best For |
|--------|------|------------|--------|----------|
| **Local Computer** | Free | ⭐ Easy | Only when PC is on | Testing |
| **Railway** | Free tier | ⭐⭐ Easy | 24/7 | Production (Recommended) |
| **Heroku** | $5/month | ⭐⭐ Easy | 24/7 | Production |
| **DigitalOcean VPS** | $5/month | ⭐⭐⭐ Moderate | 24/7 | Advanced users |
| **Raspberry Pi** | $50 one-time | ⭐⭐⭐ Moderate | 24/7 (if church has power) | Local hosting |

---

## 🎓 Learning Resources

### Technologies Used:
1. **Python** - Main programming language
   - Learn: [python.org/about/gettingstarted](https://python.org/about/gettingstarted)

2. **python-telegram-bot** - Telegram Bot API wrapper
   - Docs: [python-telegram-bot.org](https://python-telegram-bot.org)

3. **gspread** - Google Sheets Python API
   - Docs: [gspread.readthedocs.io](https://gspread.readthedocs.io)

4. **APScheduler** - Job scheduling
   - Docs: [apscheduler.readthedocs.io](https://apscheduler.readthedocs.io)

5. **Google Sheets API** - Data storage
   - Docs: [developers.google.com/sheets/api](https://developers.google.com/sheets/api)

---

## 🛣️ Development Roadmap

### Phase 1: Core Features ✅ (Current Version)
- [x] Basic rental system
- [x] Google Sheets integration
- [x] Photo verification
- [x] Automated reminders
- [x] Return functionality
- [x] Documentation

### Phase 2: Enhancement (Future)
- [ ] Admin commands (view all rentals, force return, etc.)
- [ ] User authentication/whitelist
- [ ] Overdue notifications
- [ ] Item reservation system
- [ ] Maintenance mode for items

### Phase 3: Advanced Features (Future)
- [ ] Usage analytics dashboard
- [ ] QR code integration
- [ ] Multi-language support
- [ ] SMS/Email notifications
- [ ] Integration with church calendar
- [ ] Damage reporting system

### Phase 4: Enterprise (Future)
- [ ] Multiple church support
- [ ] Web dashboard
- [ ] Mobile app
- [ ] Payment integration
- [ ] Advanced reporting

---

## 📈 Usage Metrics (What You Can Track)

From the "Rental Log" sheet, you can analyze:

1. **Most Popular Items** - Which equipment is rented most often
2. **Usage Frequency** - How often each item is used
3. **Average Rental Duration** - Typical loan periods
4. **On-Time Returns** - Percentage of timely returns
5. **Active Users** - Who uses the system regularly
6. **Peak Times** - When rentals are most common
7. **Inventory Needs** - Items that might need duplicates

---

## 🤝 Contributing

This project is open source and welcomes contributions:

### How to Contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution:
- Bug fixes
- Feature enhancements
- Documentation improvements
- Translations
- Testing
- Performance optimization

---

## 🆘 Support & Community

### Get Help:
1. Check FAQ.md for common questions
2. Review SETUP_GUIDE.md for setup issues
3. Check DEPLOYMENT.md for hosting problems
4. Look at error messages in terminal
5. Review Google Sheets for data issues

### Report Issues:
- Include error messages
- Describe steps to reproduce
- Mention your setup (OS, Python version, deployment method)
- Check if issue already exists

---

## 📜 License

MIT License - Free for church and ministry use. See LICENSE file for details.

---

## 🙏 Acknowledgments

Built with love for church tech ministries worldwide.

**Special Thanks:**
- Telegram Bot API community
- Google Sheets API
- Python open source community
- All contributors and users

---

## 📞 Quick Reference

### Important Commands:
```bash
# Test connections
python test_connection.py

# Start bot (manual)
python main.py

# Start bot (quick start - Mac/Linux)
./start.sh

# Start bot (quick start - Windows)
start.bat
```

### Important Files to Configure:
1. `.env` - Your bot token and sheet ID
2. `credentials.json` - Google Service Account credentials
3. Google Sheets - Inventory and log sheets

### Bot Commands (in Telegram):
- `/start` - Begin interaction
- `/rent` - Rent equipment
- `/myrentals` - View active rentals
- `/return` - Return equipment
- `/help` - Get help
- `/cancel` - Cancel operation

---

## 🎯 Success Metrics

Your bot is successful if:
- ✅ Users can rent equipment in < 2 minutes
- ✅ All rentals are logged automatically
- ✅ Users receive timely reminders
- ✅ Equipment tracking is accurate
- ✅ Return rate improves
- ✅ Lost equipment decreases
- ✅ Admin workload reduces

---

**Last Updated:** December 25, 2024  
**Version:** 1.0.0  
**Status:** Production Ready ✅

