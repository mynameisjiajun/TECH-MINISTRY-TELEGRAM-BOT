# 📁 Project Folder Structure

## Overview

```
TECH-MINISTRY-TELEGRAM-BOT/
│
├── 📄 run.py                    # Main entry point (run this!)
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Your configuration (create from examples/)
├── 📄 .gitignore               # Git ignore rules
├── 📄 README.md                # Main documentation
├── 📄 CHANGELOG.md             # Version history
├── 📄 LICENSE                  # MIT License
├── 📄 Procfile                 # For deployment (Heroku/Railway)
├── 📄 runtime.txt              # Python version
│
├── 📁 src/                     # Source code
│   ├── __init__.py
│   ├── main.py                 # Bot entry point
│   ├── bot.py                  # Bot commands & logic
│   ├── admin_commands.py       # Admin features
│   ├── list_command.py         # Equipment list command
│   ├── sheets_manager.py       # Google Sheets integration
│   ├── reminder_scheduler.py   # Automated reminders
│   └── config.py               # Configuration loader
│
├── 📁 docs/                    # Documentation
│   ├── README.md               # Documentation index
│   ├── QUICKSTART.md           # 15-minute setup
│   ├── SETUP_GUIDE.md          # Detailed setup
│   ├── ADMIN_GUIDE.md          # Admin manual
│   ├── DEPLOYMENT.md           # Deployment guide
│   ├── UPGRADE_GUIDE.md        # Upgrade instructions
│   ├── FAQ.md                  # Common questions
│   ├── QUICK_REFERENCE.md      # Command reference
│   ├── LOCAL_TESTING_GUIDE.md  # Testing guide
│   ├── WHATS_NEW.md            # Feature announcement
│   ├── SIMPLIFIED_VERSION.md   # Google Sheets approach
│   ├── ENHANCEMENTS_SUMMARY.md # All improvements
│   ├── PROJECT_OVERVIEW.md     # Technical overview
│   ├── SYSTEM_DIAGRAM.txt      # Visual diagrams
│   └── FOLDER_STRUCTURE.md     # This file
│
├── 📁 scripts/                 # Utility scripts
│   ├── start.sh                # Quick start (Mac/Linux)
│   ├── start.bat               # Quick start (Windows)
│   └── test_connection.py      # Connection tester
│
└── 📁 examples/                # Example files
    ├── ENV_TEMPLATE.txt        # Environment configuration template
    ├── GOOGLE_SHEETS_TEMPLATE.txt  # Sheet structure guide
    └── example_inventory.csv   # Sample inventory data
```

---

## 📂 Folder Descriptions

### **Root Directory**
Essential files for running and configuring the bot.

- `run.py` - **Main entry point** - Run this to start the bot
- `requirements.txt` - Python package dependencies
- `.env` - Your private configuration (create from `examples/ENV_TEMPLATE.txt`)
- `.gitignore` - Protects sensitive files from Git
- `README.md` - Main project documentation

### **`src/` - Source Code**
All Python source code for the bot.

- `main.py` - Application entry point, sets up handlers
- `bot.py` - Bot commands, conversation flows, user interactions
- `admin_commands.py` - Admin panel and features
- `list_command.py` - Equipment list with Google Sheets link
- `sheets_manager.py` - Google Sheets API integration
- `reminder_scheduler.py` - Automated daily reminders
- `config.py` - Configuration loader and constants

### **`docs/` - Documentation**
All user and developer documentation.

**For Users:**
- `QUICKSTART.md` - Fast 15-minute setup
- `SETUP_GUIDE.md` - Step-by-step detailed guide
- `FAQ.md` - Common questions answered
- `QUICK_REFERENCE.md` - Commands and tips

**For Admins:**
- `ADMIN_GUIDE.md` - Complete admin manual
- `DEPLOYMENT.md` - How to deploy 24/7
- `LOCAL_TESTING_GUIDE.md` - Test before deploying

**Feature Docs:**
- `WHATS_NEW.md` - Feature announcements
- `UPGRADE_GUIDE.md` - Upgrade instructions
- `SIMPLIFIED_VERSION.md` - Google Sheets approach
- `ENHANCEMENTS_SUMMARY.md` - All improvements

**Technical:**
- `PROJECT_OVERVIEW.md` - Architecture & design
- `SYSTEM_DIAGRAM.txt` - Visual system diagrams
- `FOLDER_STRUCTURE.md` - This file

### **`scripts/` - Utility Scripts**
Helper scripts for development and testing.

- `start.sh` - Quick start script for Mac/Linux
- `start.bat` - Quick start script for Windows
- `test_connection.py` - Test all connections before running

### **`examples/` - Example Files**
Templates and sample data.

- `ENV_TEMPLATE.txt` - Complete `.env` configuration guide
- `GOOGLE_SHEETS_TEMPLATE.txt` - Sheet structure explained
- `example_inventory.csv` - Sample equipment data

---

## 🚀 How to Use This Structure

### **Running the Bot:**
```bash
# From project root
python run.py
```

### **Running Tests:**
```bash
# From project root
python scripts/test_connection.py
```

### **Accessing Documentation:**
```bash
# Open docs folder
cd docs/

# Read any guide
cat QUICKSTART.md
```

### **Setting Up:**
```bash
# 1. Copy environment template
cp examples/ENV_TEMPLATE.txt .env

# 2. Edit configuration
nano .env

# 3. Add Google credentials
# Place credentials.json in project root

# 4. Run the bot
python run.py
```

---

## 📝 Files to Create (Not in Git)

These files should be created by you and are ignored by Git:

- `.env` - Your configuration (use `examples/ENV_TEMPLATE.txt` as template)
- `credentials.json` - Google Cloud service account credentials
- `venv/` or `env/` - Python virtual environment (optional)

---

## 🔒 Security Note

**Never commit these files:**
- `.env` - Contains bot token and settings
- `credentials.json` - Google Cloud credentials
- `token.json` - OAuth tokens
- `__pycache__/` - Python cache
- `*.log` - Log files

All of these are protected by `.gitignore`.

---

## 📦 Deployment Structure

When deploying, the structure remains the same. Hosting platforms will:

1. Install dependencies from `requirements.txt`
2. Use environment variables instead of `.env` file
3. Run `run.py` to start the bot

---

## 🎯 Benefits of This Structure

✅ **Clean separation** - Code, docs, scripts, examples all separate
✅ **Easy navigation** - Everything has its place
✅ **Professional** - Industry-standard folder structure
✅ **Scalable** - Easy to add new features
✅ **Maintainable** - Clear organization
✅ **Documented** - Every folder explained

---

## 🔄 Migration from Old Structure

If upgrading from previous versions:

**Old Structure:**
```
project/
├── bot.py (old)
├── bot_enhanced.py (old)
├── main.py (old)
├── main_enhanced.py (old)
└── 20+ files in root
```

**New Structure:**
```
project/
├── run.py
├── src/ (all code here)
├── docs/ (all documentation here)
├── scripts/ (all utilities here)
└── examples/ (all templates here)
```

**Migration is automatic!** Just pull the latest code.

---

## 💡 Quick Tips

### **Finding Files:**
- **Running the bot?** → Use `run.py` in root
- **Reading docs?** → Check `docs/` folder
- **Need examples?** → Look in `examples/` folder
- **Testing?** → Run `scripts/test_connection.py`

### **Adding Features:**
- New bot commands → Edit `src/bot.py`
- New admin features → Edit `src/admin_commands.py`
- New documentation → Add to `docs/` folder
- New utility script → Add to `scripts/` folder

---

**This structure keeps everything organized and professional!** 🎉

