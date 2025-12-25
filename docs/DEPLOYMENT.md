# 🚀 Deployment Guide

This guide shows you how to deploy your bot to run 24/7 in the cloud.

## Option 1: Railway (Easiest - Recommended) 🌟

Railway offers a free tier and is very easy to use.

### Steps:

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-github-repo-url
   git push -u origin main
   ```

3. **Create New Project on Railway**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Add Environment Variables**
   - Click on your service
   - Go to "Variables" tab
   - Add each variable from your `.env` file:
     - `TELEGRAM_BOT_TOKEN`
     - `GOOGLE_SHEETS_ID`
     - `INVENTORY_SHEET_NAME`
     - `LOG_SHEET_NAME`
     - `TIMEZONE`

5. **Add Google Credentials**
   - Open your `credentials.json` file
   - Copy the entire JSON content
   - In Railway, create a new variable: `GOOGLE_CREDENTIALS`
   - Paste the entire JSON as the value

6. **Update Code to Use Environment Variable** (if needed)
   
   In `sheets_manager.py`, update the credentials section:
   ```python
   import json
   import os
   
   # Add to __init__ method:
   if os.getenv('GOOGLE_CREDENTIALS'):
       # Production: Use environment variable
       creds_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
       self.creds = Credentials.from_service_account_info(
           creds_dict,
           scopes=self.scopes
       )
   else:
       # Local: Use file
       self.creds = Credentials.from_service_account_file(
           'credentials.json',
           scopes=self.scopes
       )
   ```

7. **Deploy**
   - Railway will automatically deploy
   - Check logs to ensure bot started successfully

**Cost:** Free tier includes 500 hours/month (enough for 24/7)

---

## Option 2: Heroku (Classic Option)

### Steps:

1. **Install Heroku CLI**
   - Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-bot-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_token
   heroku config:set GOOGLE_SHEETS_ID=your_sheet_id
   heroku config:set INVENTORY_SHEET_NAME="Available Items"
   heroku config:set LOG_SHEET_NAME="Rental Log"
   heroku config:set TIMEZONE="Asia/Singapore"
   ```

5. **Add Google Credentials**
   ```bash
   heroku config:set GOOGLE_CREDENTIALS="$(cat credentials.json)"
   ```

6. **Deploy**
   ```bash
   git push heroku main
   heroku ps:scale worker=1
   ```

7. **Check Logs**
   ```bash
   heroku logs --tail
   ```

**Cost:** Heroku no longer offers free tier; starts at $5/month

---

## Option 3: Google Cloud Run (Advanced)

For advanced users familiar with Docker.

### Steps:

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD ["python", "main.py"]
   ```

2. **Build and Deploy**
   ```bash
   gcloud run deploy church-tech-bot \
     --source . \
     --region asia-southeast1 \
     --allow-unauthenticated
   ```

**Cost:** Free tier includes 2 million requests/month

---

## Option 4: DigitalOcean Droplet

For full control with a virtual server.

### Steps:

1. **Create a Droplet**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Create a $5/month basic droplet (Ubuntu)

2. **SSH into Droplet**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Install Python**
   ```bash
   apt update
   apt install python3 python3-pip git -y
   ```

4. **Clone Your Repository**
   ```bash
   git clone your-repo-url
   cd your-bot-folder
   ```

5. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Add Credentials and .env**
   - Upload `credentials.json` and `.env` to the server

7. **Run with systemd** (to keep it running)
   
   Create `/etc/systemd/system/church-bot.service`:
   ```ini
   [Unit]
   Description=Church Tech Bot
   After=network.target
   
   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/your-bot-folder
   ExecStart=/usr/bin/python3 /root/your-bot-folder/main.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   systemctl enable church-bot
   systemctl start church-bot
   systemctl status church-bot
   ```

**Cost:** $5/month

---

## Option 5: Raspberry Pi (Local Server)

Run the bot on a Raspberry Pi at your church.

### Steps:

1. **Install Python on Raspberry Pi**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   ```

2. **Clone Repository**
   ```bash
   git clone your-repo-url
   cd your-bot-folder
   ```

3. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Add Credentials**
   - Transfer `credentials.json` and `.env` to the Pi

5. **Run on Startup**
   
   Add to `/etc/rc.local` (before `exit 0`):
   ```bash
   cd /home/pi/your-bot-folder && python3 main.py &
   ```

6. **Or use systemd** (better option)
   - Follow the same systemd setup as DigitalOcean

**Cost:** One-time cost of Raspberry Pi (~$50)

---

## Comparison Table

| Platform | Cost | Ease of Setup | Best For |
|----------|------|---------------|----------|
| **Railway** | Free/Paid | ⭐⭐⭐⭐⭐ Very Easy | Beginners |
| **Heroku** | $5/month | ⭐⭐⭐⭐ Easy | Simple deployments |
| **Google Cloud Run** | Free tier/Paid | ⭐⭐⭐ Moderate | Advanced users |
| **DigitalOcean** | $5/month | ⭐⭐⭐ Moderate | Full control |
| **Raspberry Pi** | $50 one-time | ⭐⭐ Requires hardware | Local hosting |

---

## 🔍 Monitoring Your Bot

### Check if Bot is Running

Send a message to your bot on Telegram. If it responds, it's running!

### Railway Monitoring
- Check "Deployments" tab
- View "Logs" for errors

### Heroku Monitoring
```bash
heroku logs --tail
```

### Server Monitoring (DigitalOcean/Raspberry Pi)
```bash
systemctl status church-bot
journalctl -u church-bot -f
```

---

## 🆘 Troubleshooting Deployment

### Bot not responding after deployment
1. Check if environment variables are set correctly
2. View logs for error messages
3. Verify Google Sheets credentials are properly configured
4. Ensure bot token is correct

### "Module not found" errors
- Make sure `requirements.txt` is in your repository
- Check if platform installed all dependencies

### Google Sheets connection errors
- Verify `GOOGLE_CREDENTIALS` environment variable is set
- Check if service account has access to the sheet
- Ensure APIs are enabled in Google Cloud

---

## 📊 Monitoring Usage

### Google Sheets
- Check "Rental Log" sheet for all transactions
- Monitor "Available Items" for inventory levels

### Bot Analytics
You can add simple logging to track:
- Number of rentals per day
- Most rented items
- Average rental duration

---

## 🔒 Security Best Practices

1. **Never commit sensitive files**
   - `credentials.json`
   - `.env`
   - Always use environment variables in production

2. **Restrict Google Sheet Access**
   - Only share with service account email
   - Don't make sheet publicly accessible

3. **Keep Bot Token Secret**
   - Never share on GitHub or publicly
   - Regenerate if accidentally exposed (via @BotFather)

4. **Regular Updates**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## ✅ Post-Deployment Checklist

- [ ] Bot responds to /start command
- [ ] Can rent an item successfully
- [ ] Photos are being saved to Google Sheets
- [ ] Google Sheets is logging transactions
- [ ] Can return items
- [ ] Reminder scheduler is running (check logs)
- [ ] Environment variables are secure
- [ ] Bot token is not exposed publicly

---

Need help? Check the main README.md or open an issue!

