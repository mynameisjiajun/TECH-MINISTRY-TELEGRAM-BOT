# ❓ Frequently Asked Questions (FAQ)

## General Questions

### Q: What is this bot for?
**A:** This bot helps church tech ministries manage equipment rentals. Members can borrow equipment, track rentals, and receive return reminders - all through Telegram.

### Q: Do I need to pay for anything?
**A:** The bot itself is free. You may need:
- A hosting service (free tiers available on Railway, or run locally)
- Google Sheets API access (free)
- Telegram Bot (free)

### Q: Can multiple people use the bot at once?
**A:** Yes! The bot can handle multiple users simultaneously.

---

## Setup Questions

### Q: I don't have Python installed. What do I do?
**A:** Download and install Python from [python.org](https://python.org). Get version 3.8 or higher.

### Q: How do I get a Telegram Bot Token?
**A:** 
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow the prompts
5. Copy the token provided

### Q: Where do I find my Google Sheets ID?
**A:** Look at your Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit
```
Copy the part between `/d/` and `/edit`

### Q: What is a Service Account?
**A:** It's like a robot user that the bot uses to access your Google Sheet. You create it in Google Cloud Console and give it permission to edit your sheet.

### Q: Do I need to create the credentials.json file?
**A:** No, Google Cloud creates it for you when you create a Service Account key. Just download it.

---

## Usage Questions

### Q: How do users rent equipment?
**A:**
1. User sends `/rent` to the bot
2. Enters Item ID (e.g., CAB001)
3. Specifies how many days they need it
4. Takes a photo of the item
5. Done!

### Q: What if an item is already rented?
**A:** The bot checks availability automatically. If all units are rented, it will tell the user the item is unavailable.

### Q: Can users return items early?
**A:** Yes! They can use the `/return` command anytime.

### Q: How do reminders work?
**A:** The bot automatically sends a Telegram message to users 1 day before their return date (default: 9 AM).

### Q: What if someone doesn't return an item on time?
**A:** The bot logs everything in Google Sheets. You can manually check the "Rental Log" sheet for overdue items and contact the borrower.

### Q: Can I see who rented what?
**A:** Yes! Check the "Rental Log" sheet in Google Sheets. It shows all transactions with timestamps, photos, and status.

---

## Technical Questions

### Q: Where are the photos stored?
**A:** Photos are stored on Telegram's servers. The bot saves the photo URL in your Google Sheet for reference.

### Q: Can I change the reminder time?
**A:** Yes! Edit `reminder_scheduler.py` and change the `hour` value (0-23 for 24-hour format).

### Q: What happens if the bot goes offline?
**A:** Users won't be able to rent/return items until it's back online. Scheduled reminders will be missed. That's why we recommend hosting it on a cloud service.

### Q: Can I run this on my local computer?
**A:** Yes, but it only works when your computer is on and connected to the internet.

### Q: What's the difference between Railway, Heroku, etc.?
**A:**
- **Railway**: Easy to use, free tier available, recommended for beginners
- **Heroku**: Popular but no free tier anymore, starts at $5/month
- **VPS (DigitalOcean, etc.)**: More control, requires more technical knowledge
- **Raspberry Pi**: One-time cost, runs locally at your church

### Q: How much does hosting cost?
**A:** Free options available (Railway free tier). Paid options start at $5/month.

### Q: Can I customize the bot messages?
**A:** Yes! Edit the message strings in `bot.py`.

### Q: What if I want to track more information?
**A:** You can modify the Google Sheets columns and update `config.py` and `sheets_manager.py` accordingly.

---

## Troubleshooting

### Q: Bot says "Error connecting to Google Sheets"
**A:** Check:
1. Is `credentials.json` in the correct folder?
2. Did you share the sheet with the service account email?
3. Are the Google Sheets API and Drive API enabled?
4. Is the `GOOGLE_SHEETS_ID` correct in `.env`?

### Q: Bot doesn't respond to commands
**A:** Check:
1. Is the bot running? (`python main.py`)
2. Is the bot token correct?
3. Did you `/start` the conversation?
4. Check the terminal for error messages

### Q: Reminders aren't being sent
**A:** Check:
1. Is the bot running 24/7?
2. Did users start a conversation with the bot first?
3. Is the User ID being stored in the Google Sheet?
4. Check timezone setting in `.env`

### Q: "Module not found" error
**A:** Run `pip install -r requirements.txt` to install all dependencies.

### Q: Photo upload fails
**A:** This is rare. Check:
1. User's internet connection
2. Telegram is not experiencing issues
3. Bot has proper permissions

### Q: Item shows as unavailable but it should be available
**A:** Check the "Rental Log" sheet. There might be active rentals that weren't returned properly. You can manually change the Status from "ACTIVE" to "RETURNED".

---

## Google Sheets Questions

### Q: Can I manually edit the Google Sheet?
**A:** Yes, but be careful:
- Don't change column headers
- Don't delete rows while bot is processing
- You can manually update Status if needed

### Q: What if I want different column names?
**A:** You'll need to update `config.py` to match your column names.

### Q: Can I use multiple Google Sheets?
**A:** Not with the default setup, but you can modify the code to support multiple sheets.

### Q: How do I backup my data?
**A:** Google Sheets automatically saves. You can also:
- File → Download → Excel/CSV
- Use Google Sheets built-in version history

---

## Security & Privacy

### Q: Is this secure?
**A:** Yes, when configured properly:
- Keep `credentials.json` and `.env` private
- Don't commit these files to public Git repositories
- Only share the Google Sheet with the service account

### Q: Can anyone use my bot?
**A:** Yes, anyone who finds your bot on Telegram can use it. If you want to restrict access, you'll need to add user authentication (not included by default).

### Q: What data is collected?
**A:** The bot stores:
- User's Telegram name and username
- User ID (for reminders)
- Rental history
- Photos of pickups and returns

### Q: Can I delete rental history?
**A:** Yes, you can delete rows from the "Rental Log" sheet. Just make sure items are returned first.

---

## Feature Requests

### Q: Can I add a waitlist for items?
**A:** Not by default, but you could modify the code to add this feature.

### Q: Can I set different rental periods for different items?
**A:** Currently users choose the duration. You could add maximum rental period limits by modifying the code.

### Q: Can I charge for rentals?
**A:** Not built-in, but you could integrate with payment APIs (Stripe, PayPal) if needed.

### Q: Can I get weekly reports?
**A:** Not automatically, but you can easily view all data in the "Rental Log" sheet. You could add a reporting feature by extending the bot.

### Q: Can admins override rentals?
**A:** Not by default. Admins can manually edit the Google Sheet to make changes.

---

## Best Practices

### Q: How should I organize Item IDs?
**A:** Use prefixes by category:
- CAB### for cables
- MIC### for microphones
- CAM### for cameras
- LIGHT### for lighting
Keep it consistent!

### Q: Should I tell users where items are before they confirm rental?
**A:** Yes! The bot shows location after they confirm rental and upload a photo.

### Q: How often should I check the rental log?
**A:** Weekly is good. Look for:
- Overdue items
- Popular items (consider getting more)
- Items never rented (consider removing from inventory)

### Q: Should I backup my Google Sheet?
**A:** Yes! Download a copy monthly: File → Download → Excel or CSV

---

## Contact & Support

### Q: I found a bug, what do I do?
**A:** Check the error message in the terminal. Common issues are usually in the Troubleshooting section.

### Q: Can I contribute to this project?
**A:** Yes! This is open source. Feel free to fork and improve it.

### Q: Where can I learn more about Telegram bots?
**A:** Check the [official Telegram Bot documentation](https://core.telegram.org/bots).

### Q: Where can I learn more about Google Sheets API?
**A:** Check the [Google Sheets API documentation](https://developers.google.com/sheets/api).

---

**Still have questions?** Check the main README.md or SETUP_GUIDE.md!

