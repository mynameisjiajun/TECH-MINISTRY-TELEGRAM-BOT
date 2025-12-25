# 🔧 Admin Guide

Complete guide for administrators of the Church Tech Ministry Rental Bot.

---

## 🎯 Admin Overview

As an admin, you have special access to:
- **View all rentals** - See what everyone has borrowed
- **Track overdue items** - Know what's late
- **Send notifications** - Remind users about returns
- **View statistics** - Understand usage patterns
- **Admin control panel** - Central command center

---

## ⚙️ Admin Setup

### Step 1: Get Your Telegram User ID

1. Open Telegram
2. Search for `@userinfobot`
3. Start a chat
4. Send any message
5. Copy the User ID (it's a number like: `123456789`)

### Step 2: Add Yourself as Admin

Edit your `.env` file:

```env
# Single admin
ADMIN_USER_IDS=123456789

# Multiple admins (comma-separated, no spaces)
ADMIN_USER_IDS=123456789,987654321,456789123
```

### Step 3: Restart the Bot

```bash
python main.py
# or
python main_enhanced.py
```

### Step 4: Test Admin Access

1. Open your bot on Telegram
2. Send `/admin`
3. You should see the Admin Control Panel

If you don't see it:
- Check your User ID is correct
- Make sure bot restarted
- Verify no spaces in `.env` file

---

## 📱 Admin Commands

### `/admin` - Admin Control Panel

Opens the main admin interface with buttons for all admin functions.

**Quick Access:**
- 📊 All Active Rentals
- ⏰ Overdue Items
- 📈 Statistics
- ❌ Close Panel

---

## 📊 View All Active Rentals

**What it does:**
- Shows every item currently rented
- Displays borrower information
- Shows due dates

**Use cases:**
- Check who has what
- Verify equipment location before events
- Plan equipment needs

**How to use:**
1. Send `/admin`
2. Click "📊 All Active Rentals"
3. View the list
4. Click "🔙 Back" when done

**Example output:**
```
📦 Active Rentals (5)

1. XLR Cable 3m (CAB001)
   👤 John Doe (@johndoe)
   📅 Due: 2024-12-28

2. Wireless Mic (MIC001)
   👤 Jane Smith (@janesmith)
   📅 Due: 2024-12-29

...
```

---

## ⏰ View Overdue Items

**What it does:**
- Automatically calculates overdue rentals
- Shows how many days overdue
- Sorts by most overdue first

**Use cases:**
- Identify items that need immediate attention
- Contact users about overdue returns
- Track repeat late returnees

**How to use:**
1. Send `/admin`
2. Click "⏰ Overdue Items"
3. View the list
4. Optionally click "📢 Notify All Overdue"

**Example output:**
```
⚠️  Overdue Items (2)

1. XLR Cable 3m (CAB001)
   👤 John Doe (@johndoe)
   📅 Due: 2024-12-20
   🚨 5 days overdue

2. Camera (CAM001)
   👤 Jane Smith (@janesmith)
   📅 Due: 2024-12-23
   🚨 2 days overdue

[📢 Notify All Overdue]
```

---

## 📢 Notify Overdue Users

**What it does:**
- Sends a reminder message to each overdue user
- Personalized with item details
- Includes how many days overdue
- One-click operation

**Message sent to users:**
```
🚨 OVERDUE EQUIPMENT REMINDER

📦 Item: XLR Cable 3m
🆔 Item ID: CAB001
📅 Was due: 2024-12-20
⚠️  5 days overdue

Please return this item as soon as possible!
Use /return to complete the return process.

Thank you! 🙏
```

**How to use:**
1. View Overdue Items
2. Click "📢 Notify All Overdue"
3. Bot sends messages to all overdue users
4. You'll see confirmation: "✅ Sent X notification(s)!"

**Best practices:**
- Send reminders weekly for items 3+ days overdue
- Follow up personally for items 7+ days overdue
- Be understanding - people forget!

---

## 📈 Usage Statistics

**What it shows:**
- Total rentals (all time)
- Active vs completed rentals
- Unique user count
- On-time return rate (percentage)
- Top 5 most rented items

**Use cases:**
- Understand equipment demand
- Identify items to buy more of
- Track system usage
- Monthly reports for ministry
- Budget planning

**How to use:**
1. Send `/admin`
2. Click "📈 Statistics"
3. Review the data

**Example output:**
```
📊 Usage Statistics

📦 Total Rentals: 47
🟢 Active: 5
✅ Completed: 42
👥 Unique Users: 12
⏱️  On-Time Return Rate: 92.9%

🔥 Most Rented Items:
1. CAB001 - 12 rentals
2. MIC001 - 8 rentals
3. CAM001 - 6 rentals
4. LIGHT001 - 5 rentals
5. CAB002 - 4 rentals
```

**Insights from stats:**
- **High total rentals** = System is being used well
- **Low on-time rate** (<80%) = Need stricter policies
- **Popular items** = Consider buying duplicates
- **Unique users** = Track engagement growth

---

## 🛠️ Admin Best Practices

### Daily Tasks (2 minutes)
- [ ] Check overdue items
- [ ] Review new rentals from today

### Weekly Tasks (10 minutes)
- [ ] Send reminders to overdue users
- [ ] Review active rentals
- [ ] Check statistics
- [ ] Follow up on items 7+ days overdue

### Monthly Tasks (30 minutes)
- [ ] Generate usage report
- [ ] Review on-time return rate
- [ ] Identify popular items
- [ ] Plan equipment purchases
- [ ] Clean up old logs (if needed)
- [ ] Backup Google Sheets

---

## 📋 Common Admin Scenarios

### Scenario 1: User Lost an Item

**What to do:**
1. Check rental log in Google Sheets
2. Confirm it was rented by that user
3. Contact user via Telegram
4. Manually mark as returned in Google Sheets
   - Or keep as ACTIVE to track the loss
5. Add note in your records

### Scenario 2: Item Damaged on Return

**What to do:**
1. User completes return normally
2. You inspect item
3. Note damage in your records
4. Optionally add note in Google Sheets
5. Mark item for repair (manual)
6. Contact user if needed

**Future enhancement:** Damage reporting system

### Scenario 3: User Needs Extension

**What to do:**
1. Check if item is needed by others
2. If available, approve extension
3. Manually update "Expected Return Date" in Google Sheets
4. Inform user

**Note:** Update the Google Sheets Log directly
- Find the rental row
- Edit "Expected Return Date" column
- User will get reminder on new date

### Scenario 4: Emergency Item Needed

**What to do:**
1. Check `/admin` → "All Active Rentals"
2. Find who has the item
3. Contact user directly
4. Arrange early return or swap

### Scenario 5: Item Stuck as "Active"

**Problem:** User returned item but forgot to use `/return`

**Solution:**
1. Verify item is physically returned
2. Open Google Sheets "Rental Log"
3. Find the rental row
4. Update:
   - "Actual Return Date" = today's date
   - "Status" = RETURNED
   - "Return Photo" = (optional) add link or note
5. Item now shows as available

---

## 📊 Google Sheets Admin Tasks

As admin, you sometimes need to edit Google Sheets directly.

### Viewing Data

**Available Items Sheet:**
- Current inventory
- Quantities
- Locations

**Rental Log Sheet:**
- All transactions
- Active vs returned
- User history

### Manual Edits (When Needed)

**Change Return Date:**
1. Open "Rental Log" sheet
2. Find the rental (filter by Status = ACTIVE)
3. Edit "Expected Return Date" column
4. Save

**Force Return:**
1. Open "Rental Log" sheet
2. Find the rental
3. Edit:
   - "Status" → RETURNED
   - "Actual Return Date" → today
4. Save

**Add Notes:**
- You can add a "Notes" column if needed
- Track special circumstances
- Document damages

---

## 🔐 Admin Security

### Protect Your Admin Access

✅ **DO:**
- Keep your User ID private
- Only add trusted admins
- Review admin list regularly
- Use secure device for admin tasks

❌ **DON'T:**
- Share your Telegram account
- Add admins you don't fully trust
- Leave admin session open on shared devices
- Share Google Sheets access publicly

### Who Should Be an Admin?

✅ **Good candidates:**
- Tech ministry leaders
- Equipment managers
- Trusted volunteers with responsibility

❌ **Not recommended:**
- General church members
- Temporary volunteers
- People who just want to see stats

---

## 📈 Analytics & Reports

### Weekly Report Template

```
📊 Weekly Equipment Rental Report
Week of: [Date Range]

📦 Active Rentals: X
⏰ Overdue Items: X
✅ Completed This Week: X
👥 Active Users: X
⏱️  On-Time Rate: X%

🔥 Top Items This Week:
1. [Item Name] - X rentals
2. [Item Name] - X rentals
3. [Item Name] - X rentals

⚠️  Issues:
- [Any problems or concerns]

📝 Notes:
- [Observations or recommendations]
```

### Export Data for Reports

1. Open Google Sheets "Rental Log"
2. File → Download → Excel or CSV
3. Open in Excel/Numbers
4. Create pivot tables/charts
5. Generate reports

**Useful Reports:**
- Rentals per month
- Popular items
- User activity
- On-time vs late returns

---

## 🆘 Admin Troubleshooting

### "Can't access /admin command"

**Check:**
1. Is your User ID in `.env` ADMIN_USER_IDS?
2. Did you restart the bot?
3. Any spaces in the comma-separated list?
4. Is User ID correct (check @userinfobot)?

**Fix:**
```bash
# Check .env
cat .env | grep ADMIN_USER_IDS

# Should show: ADMIN_USER_IDS=123456789,987654321

# Restart bot
python main.py
```

### "Overdue items not showing"

**Possible causes:**
1. No items actually overdue
2. Date format issue in Google Sheets
3. Bot timezone wrong

**Fix:**
```bash
# Check timezone in .env
cat .env | grep TIMEZONE

# Should match your location
# Common: Asia/Singapore, America/New_York, etc.
```

### "Statistics seem wrong"

**Check:**
1. Google Sheets "Rental Log" data
2. Status column (should be ACTIVE or RETURNED)
3. Date formats

**Manual verification:**
- Count rows manually
- Check calculations
- Verify data integrity

---

## 🎓 Admin Training Checklist

### New Admin Onboarding

- [ ] Get Telegram User ID
- [ ] Added to ADMIN_USER_IDS
- [ ] Test `/admin` command access
- [ ] View all active rentals
- [ ] Check overdue items
- [ ] Review statistics
- [ ] Practice sending overdue notifications
- [ ] Learn Google Sheets access
- [ ] Understand manual edits process
- [ ] Read common scenarios section
- [ ] Know emergency contact procedures

### Admin Certification Quiz

1. How do you check all active rentals?
2. What button sends reminders to overdue users?
3. Where do you manually edit return dates?
4. Who should have admin access?
5. What's the on-time return rate goal?
6. How often should you check overdue items?
7. How do you export data for reports?

---

## 💡 Admin Pro Tips

1. **Set a schedule** - Check admin panel same time daily
2. **Be proactive** - Don't wait for users to ask
3. **Document everything** - Keep notes on issues
4. **Communicate clearly** - Users appreciate reminders
5. **Review regularly** - Weekly stats review helps planning
6. **Plan ahead** - Know what's needed for upcoming events
7. **Be kind** - People forget; reminders should be friendly

---

## 🚀 Advanced Admin Features (Coming Soon)

Future enhancements planned:
- [ ] Force return from admin panel (no sheet edit)
- [ ] User management (ban/unban)
- [ ] Custom reminder messages
- [ ] Scheduled notifications
- [ ] Bulk operations
- [ ] Maintenance mode for items
- [ ] Damage reporting system
- [ ] Admin activity log
- [ ] Export reports directly from bot

---

## 📞 Admin Support

**Need help?**
1. Check this guide first
2. Review `FAQ.md`
3. Check `README.md`
4. Ask other admins
5. Check Google Sheets for data issues

**Have suggestions?**
- Document them
- Discuss with tech ministry
- Consider contributing to the project

---

**Remember:** Being an admin is about serving your church community by making equipment access easy and accountable. Thank you for your service! 🙏

---

## 📚 Related Documentation

- `UPGRADE_GUIDE.md` - How to enable admin features
- `README.md` - Main documentation
- `FAQ.md` - Common questions
- `PROJECT_OVERVIEW.md` - Technical details

---

**Questions?** Reach out to your tech ministry leadership or check the documentation!

