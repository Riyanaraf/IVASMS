# 🚀 IVASMS Telegram Bot - START HERE

Welcome! Your production-ready bot is ready to deploy. Follow this guide to get started.

## ⏱️ Quick Summary

| Item | Status |
|------|--------|
| Bot Code | ✅ Complete (bot.py - 591 lines) |
| Cloudflare Bypass | ✅ Implemented (Selenium + headers) |
| Login Handling | ✅ Auto-retry with backoff |
| Telegram Integration | ✅ Full command support |
| Error Handling | ✅ Comprehensive with logging |
| Documentation | ✅ Complete (2000+ lines) |
| Deployment Options | ✅ 7 different methods |
| Verification Tools | ✅ Setup checker included |
| Production Ready | ✅ **YES** |

## 📋 What You Have

```
bot.py                    ← Your main bot (USE THIS)
requirements.txt          ← All dependencies listed
.env.example             ← Config template
QUICKSTART.md            ← Get running in 5 min
README_COMPLETE.md       ← Full documentation
DEPLOYMENT_GUIDE.md      ← All deployment options
REQUIREMENTS_INFO.md     ← Dependency details
verify_setup.py          ← Setup verification
run.sh & run.bat         ← Quick start scripts
docker-compose.yml       ← Docker setup
Dockerfile              ← Docker image
install-systemd.sh      ← Linux service installer
ivasms-bot.service      ← Systemd config
INSTALLATION_COMPLETE.md ← What was done
START_HERE.md           ← This file
```

## 🎯 Next Steps (Choose One)

### ⚡ Option 1: Run in 2 Minutes (Testing)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export IVASMS_EMAIL="your@email.com"
export IVASMS_PASSWORD="yourpassword"
export BOT_TOKEN="123456:ABC-DEF..."
export CHAT_ID="1234567890"

# 3. Run
python3 bot.py
```

**Time:** 2 minutes  
**Best for:** Testing, development  
**Pros:** Quickest setup  
**Cons:** Stops when terminal closes

---

### 🐧 Option 2: Linux/Pterodactyl (Production)

```bash
# 1. Make script executable
chmod +x run.sh

# 2. Create .env file (copy .env.example)
cp .env.example .env
# Edit .env with your credentials

# 3. Run
./run.sh
```

**Time:** 3 minutes  
**Best for:** Pterodactyl Panel, VPS, Linux servers  
**Pros:** Auto-installs dependencies, professional setup  
**Cons:** Linux only

---

### 🪟 Option 3: Windows (Quick)

```batch
REM 1. Create .env file (copy .env.example)
copy .env.example .env
REM 2. Edit .env with your credentials

REM 3. Run
run.bat
```

**Time:** 2 minutes  
**Best for:** Windows local testing, development  
**Pros:** Simple, one-click setup  
**Cons:** Manual .env editing

---

### 🐳 Option 4: Docker (Best for Production)

```bash
# 1. Create .env file
cp .env.example .env
# Edit .env with your credentials

# 2. Run with Docker Compose
docker-compose up -d

# 3. Check health
curl http://localhost:10000
```

**Time:** 3 minutes  
**Best for:** Cloud hosting, containerized environments  
**Pros:** Isolated, reproducible, scales easily  
**Cons:** Requires Docker

---

### 🖥️ Option 5: Linux as Service (Enterprise)

```bash
# 1. Set environment variables
export IVASMS_EMAIL="your@email.com"
export IVASMS_PASSWORD="yourpassword"
export BOT_TOKEN="123456:ABC-DEF..."
export CHAT_ID="1234567890"

# 2. Install as systemd service
sudo -E ./install-systemd.sh

# 3. Manage service
sudo systemctl status ivasms-bot
sudo systemctl restart ivasms-bot
sudo journalctl -u ivasms-bot -f
```

**Time:** 5 minutes  
**Best for:** Production Linux servers, auto-restart needed  
**Pros:** Auto-starts on reboot, professional monitoring  
**Cons:** Linux only, requires sudo

---

## 📝 Configuration Steps

### 1. Get Your Credentials

#### IVASMS Email & Password
- Login to https://www.ivasms.com
- Use the exact email and password you use there

#### Telegram Bot Token
1. Open Telegram
2. Search for @BotFather
3. Send `/newbot`
4. Follow instructions
5. Get your token (format: `123456789:ABC-DEF...`)

#### Telegram Chat ID
1. Send any message to your target chat
2. Open Telegram and search for @userinfobot
3. It shows your Chat ID (e.g., `1234567890`)

### 2. Create .env File

```bash
# Copy template
cp .env.example .env

# Edit with your values (nano, vim, VS Code, Notepad, etc.)
nano .env

# Or create manually:
# IVASMS_EMAIL=your@email.com
# IVASMS_PASSWORD=yourpassword
# BOT_TOKEN=123456789:ABCDEFGhijk...
# CHAT_ID=1234567890
```

### 3. Verify Setup

```bash
python3 verify_setup.py
```

Should show:
- ✓ Python version check
- ✓ All dependencies installed
- ✓ Environment variables set
- ✓ Network connectivity OK

## ✅ Start Your Bot

### Run and test:

```bash
python3 bot.py
```

You should see:
```
INFO - Initial login successful!
INFO - Bot started successfully - monitoring for SMS...
```

### In Telegram:

Send `/status` to your bot, you should get:
```
Bot Status: 🟢 Online and monitoring
Messages tracked: 0
```

## 📚 Need Help?

| Question | Answer |
|----------|--------|
| **How to stop the bot?** | Press Ctrl+C in terminal |
| **Bot keeps crashing?** | Run `verify_setup.py` to diagnose |
| **Not getting SMS?** | Check IVASMS credentials manually |
| **Telegram not responding?** | Verify bot token and chat ID |
| **Port 10000 in use?** | Change PORT: `export PORT=9999` |
| **Module not found?** | Run `pip install -r requirements.txt` |

## 📖 Detailed Documentation

- **QUICKSTART.md** - 5-minute quick start guide
- **DEPLOYMENT_GUIDE.md** - Complete deployment guide (366 lines)
- **README_COMPLETE.md** - Full documentation with examples (559 lines)
- **REQUIREMENTS_INFO.md** - All dependencies explained (460 lines)
- **INSTALLATION_COMPLETE.md** - What was done and how to use it

## 🎮 Bot Commands (In Telegram)

Once running:
- `/start` - Welcome message
- `/help` - Show all commands
- `/status` - Check bot status
- `/stats` - Admin statistics
- `/restart` - Admin restart

## 🔍 Monitor Your Bot

### Check it's running:
```bash
curl http://localhost:10000
# Returns: IVASMS Bot is running!
```

### View logs:
```bash
# Linux systemd
sudo journalctl -u ivasms-bot -f

# Docker
docker logs -f ivasms-bot

# Direct console (if running in terminal)
(See output on screen)
```

## ⚠️ Important

1. **All credentials required** - Email, password, bot token, chat ID
2. **Environment variables** - Must be set before running bot
3. **Bot works offline** - No database, no external service needed
4. **Single file** - All code in bot.py, no other dependencies
5. **Error recovery** - Automatic retry on failure

## 🚀 Production Checklist

Before going live:
- [ ] Tested on target server/OS
- [ ] Environment variables verified
- [ ] Credentials tested manually
- [ ] Bot commands working in Telegram
- [ ] Monitoring setup (systemd, Docker, etc.)
- [ ] Logs being monitored
- [ ] Backup plan for crashes
- [ ] Updates/maintenance plan

## 🆘 Troubleshooting

**Error: "Missing required environment variables"**
```bash
# Check which are missing
python3 verify_setup.py

# Set them
export IVASMS_EMAIL="your@email.com"
export IVASMS_PASSWORD="yourpassword"
export BOT_TOKEN="token"
export CHAT_ID="chatid"
```

**Error: "Login failed"**
1. Verify credentials manually at https://www.ivasms.com/login
2. Check for typos in email/password
3. Try different IP (might be blocked)
4. Check account isn't locked

**Error: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
python3 -c "import requests, bs4, telegram; print('OK')"
```

**Telegram bot not responding:**
1. Verify BOT_TOKEN is correct
2. Verify CHAT_ID is correct
3. Ensure bot is added to group/chat
4. Check group message restrictions

**See DEPLOYMENT_GUIDE.md for detailed troubleshooting**

---

## 🎯 Choose Your Deployment Path

```
Do you want to test locally?
├─ YES → Option 1 (2 minutes)
└─ NO → Continue

Do you have Linux?
├─ YES → Option 2 (Pterodactyl) or Option 5 (Service)
└─ NO → Continue

Do you have Windows?
├─ YES → Option 3 (Windows)
└─ NO → Continue

Do you have Docker?
├─ YES → Option 4 (Docker)
└─ NO → Use Option 1 (Direct Python)
```

## 📈 Next Steps After Setup

1. **Verify it works:**
   - Send `/status` in Telegram
   - Send SMS to test number
   - Check notification arrives

2. **Set up monitoring:**
   - Configure systemd (Linux)
   - Set up monitoring alerts
   - Plan backup/recovery

3. **Monitor usage:**
   - Check logs regularly
   - Monitor resource usage
   - Update credentials periodically

4. **Maintain:**
   - Keep Python updated
   - Update dependencies: `pip install --upgrade -r requirements.txt`
   - Review logs weekly

---

## 💡 Pro Tips

- **Test credentials first:** Login manually to verify they work
- **Use .env file:** Not environment variables (easier to manage)
- **Monitor logs:** Check daily for any errors
- **Systemd service:** Set up on production servers (auto-restart)
- **Docker:** Best for cloud hosting and scaling
- **Health checks:** Monitor `curl http://localhost:10000`

---

## 🎉 You're Ready!

Your bot is fully set up and ready to deploy. 

**Choose an option above and get started in minutes!**

For detailed help, see the documentation files listed above.

---

<div align="center">

**Questions?** Check the detailed docs  
**Issues?** Run `python3 verify_setup.py`  
**Ready?** Pick your deployment option and go!

**Status: PRODUCTION READY** ✅

</div>
