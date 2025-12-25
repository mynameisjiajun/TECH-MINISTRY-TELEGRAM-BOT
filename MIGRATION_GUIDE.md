# 🔄 Migration Guide: New Folder Structure

## What Changed in Version 2.1.0

Your project has been reorganized into a professional folder structure!

---

## 📁 New Structure

```
Before (v2.0):                  After (v2.1):
├── bot_enhanced.py            ├── run.py (NEW!)
├── main_enhanced.py           ├── src/
├── admin_commands.py          │   ├── bot.py
├── list_command.py            │   ├── main.py
├── sheets_manager.py          │   ├── admin_commands.py
├── config.py                  │   ├── list_command.py
├── 20+ doc files              │   ├── sheets_manager.py
└── ...                        │   └── ...
                               ├── docs/ (all docs here)
                               ├── scripts/ (all scripts here)
                               └── examples/ (all templates here)
```

---

## 🚀 How to Run (New Method)

### **Old Way:**
```bash
python main_enhanced.py  ❌
```

### **New Way:**
```bash
python run.py  ✅
# or
python src/main.py  ✅
```

---

## 📝 What You Need to Update

### **If You're Running Locally:**

1. **Pull latest code:**
```bash
git pull origin main
```

2. **Your `.env` and `credentials.json` stay in the root** - No changes needed! ✅

3. **Run the new way:**
```bash
python run.py
```

### **If You're Deploying:**

Update your deployment command from:
```bash
# Old
python main_enhanced.py
```

To:
```bash
# New
python run.py
```

---

## 🔍 File Location Changes

| What | Old Location | New Location |
|------|-------------|--------------|
| **Run bot** | `main_enhanced.py` | `run.py` |
| **Bot code** | `bot_enhanced.py` | `src/bot.py` |
| **Main file** | `main_enhanced.py` | `src/main.py` |
| **Admin** | `admin_commands.py` | `src/admin_commands.py` |
| **Config** | `config.py` | `src/config.py` |
| **All docs** | Root folder | `docs/` folder |
| **Scripts** | Root folder | `scripts/` folder |
| **Examples** | Root folder | `examples/` folder |

---

## ✅ What Stayed the Same

✅ **Configuration** - `.env` stays in root
✅ **Credentials** - `credentials.json` stays in root  
✅ **Dependencies** - `requirements.txt` unchanged
✅ **Functionality** - Bot works exactly the same
✅ **Data** - Google Sheets unchanged
✅ **Commands** - All bot commands unchanged

---

## 🎯 Quick Migration Checklist

- [ ] Pull latest code (`git pull origin main`)
- [ ] Verify `.env` is in root (it should be)
- [ ] Verify `credentials.json` is in root (it should be)
- [ ] Test: `python run.py`
- [ ] Update deployment scripts to use `run.py`
- [ ] Update any shortcuts/aliases
- [ ] Done! ✅

---

## 📚 Finding Documentation

**Old:**
- Docs were in root folder (messy!)

**New:**
- All docs in `docs/` folder (organized!)
- Start with: `docs/README.md`

---

## 🛠️ For Developers

### **Editing Code:**

**Before:**
```bash
vim bot_enhanced.py
vim main_enhanced.py
```

**After:**
```bash
vim src/bot.py
vim src/main.py
```

### **Running Tests:**

**Before:**
```bash
python test_connection.py
```

**After:**
```bash
python scripts/test_connection.py
```

### **Import Paths:**

Code imports are handled automatically by `run.py`. No changes needed!

---

## 💡 Benefits of New Structure

✅ **Cleaner** - Root folder only has essentials
✅ **Professional** - Industry-standard structure
✅ **Organized** - Everything has its place
✅ **Scalable** - Easy to add features
✅ **Maintainable** - Find files faster

---

## 🔧 Deployment Updates

### **Railway/Heroku:**

Update `Procfile`:
```procfile
# Old
worker: python main_enhanced.py

# New
worker: python run.py
```

### **Docker:**

Update `Dockerfile`:
```dockerfile
# Old
CMD ["python", "main_enhanced.py"]

# New
CMD ["python", "run.py"]
```

### **Systemd:**

Update service file:
```ini
# Old
ExecStart=/usr/bin/python3 /path/to/main_enhanced.py

# New
ExecStart=/usr/bin/python3 /path/to/run.py
```

---

## ❓ FAQ

### **Q: Do I need to reconfigure anything?**
A: No! `.env` and `credentials.json` stay the same.

### **Q: Will my bot stop working?**
A: Not if you use `run.py` instead of `main_enhanced.py`.

### **Q: What happened to bot_enhanced.py?**
A: Renamed to `src/bot.py` (it's the same file!)

### **Q: Can I still use the old commands?**
A: Old commands like `main_enhanced.py` won't work. Use `run.py` instead.

### **Q: Where did my documentation go?**
A: All moved to `docs/` folder. Check `docs/README.md`.

### **Q: Do I need to reinstall packages?**
A: No! `requirements.txt` is unchanged.

---

## 🆘 Troubleshooting

### **"ModuleNotFoundError" when running**

**Solution:** Use `run.py` instead of `src/main.py` directly:
```bash
python run.py  # ✅ Correct
python src/main.py  # ❌ Won't work without path setup
```

### **"Can't find .env file"**

**Solution:** Make sure `.env` is in project root, not in `src/`:
```
project/
├── .env  ← Should be here
└── src/
    └── ...
```

### **"Old command doesn't work"**

Update your command:
```bash
# If you had
python main_enhanced.py

# Change to
python run.py
```

---

## 🎉 Migration Complete!

Once you've updated to `run.py`, you're done!

The project is now:
- ✅ Better organized
- ✅ More professional
- ✅ Easier to maintain
- ✅ Ready for growth

---

**Questions?** Check `docs/FAQ.md` or `docs/FOLDER_STRUCTURE.md`

