# IVASMS Bot - Deployment Checklist

Use this checklist to ensure proper deployment.

## Pre-Deployment

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] pip available (`pip --version`)
- [ ] Git installed (for cloning) - optional
- [ ] Read START_HERE.md
- [ ] Read QUICKSTART.md or DEPLOYMENT_GUIDE.md

## Preparation

- [ ] Download/clone project files
- [ ] Navigate to project directory
- [ ] Verify `bot.py` exists (591 lines)
- [ ] Verify `requirements.txt` exists
- [ ] Copy `.env.example` to `.env`

## Credentials & Configuration

### Get Your Credentials

- [ ] IVASMS Email: __________________
- [ ] IVASMS Password: __________________
- [ ] Telegram Bot Token (from @BotFather): __________________
- [ ] Telegram Chat ID (from @userinfobot): __________________

### Set Up Environment

Choose your method:

#### Method 1: .env File (Recommended)
- [ ] Create `.env` file in project directory
- [ ] Add: `IVASMS_EMAIL=your@email.com`
- [ ] Add: `IVASMS_PASSWORD=yourpassword`
- [ ] Add: `BOT_TOKEN=123456:ABC-DEF...`
- [ ] Add: `CHAT_ID=1234567890`
- [ ] Save file

#### Method 2: Environment Variables
- [ ] `export IVASMS_EMAIL="your@email.com"`
- [ ] `export IVASMS_PASSWORD="yourpassword"`
- [ ] `export BOT_TOKEN="123456:ABC-DEF..."`
- [ ] `export CHAT_ID="1234567890"`

#### Method 3: System Environment (Pterodactyl/VPS)
- [ ] Set IVASMS_EMAIL in system environment
- [ ] Set IVASMS_PASSWORD in system environment
- [ ] Set BOT_TOKEN in system environment
- [ ] Set CHAT_ID in system environment

## Pre-Launch Verification

- [ ] Run: `python3 verify_setup.py`
- [ ] All checks pass (green checkmarks)
- [ ] Test IVASMS login manually: https://www.ivasms.com/login
- [ ] Verify Telegram bot token with @BotFather
- [ ] Verify Chat ID with @userinfobot
- [ ] Check network connectivity: `curl https://www.ivasms.com`

## Choose Deployment Method

### Option 1: Direct Python
- [ ] `pip install -r requirements.txt`
- [ ] `python3 bot.py`
- [ ] See console output: "Bot started successfully..."

### Option 2: Linux/Pterodactyl Script
- [ ] `chmod +x run.sh`
- [ ] `./run.sh`
- [ ] See console output: "Bot started successfully..."

### Option 3: Windows Script
- [ ] `run.bat`
- [ ] See console output: "Bot started successfully..."

### Option 4: Docker
- [ ] `docker-compose up -d`
- [ ] `docker logs -f ivasms-bot`
- [ ] See: "Bot started successfully..."

### Option 5: Linux Systemd Service
- [ ] `sudo -E ./install-systemd.sh`
- [ ] `sudo systemctl status ivasms-bot`
- [ ] Status shows "running"

### Option 6: Manual VPS
- [ ] Follow DEPLOYMENT_GUIDE.md section "VPS Installation"
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Run bot

## Initial Test

After deployment:

- [ ] Bot is running (check console or status)
- [ ] Open Telegram app
- [ ] Find your bot
- [ ] Send command: `/start`
- [ ] Receive welcome message
- [ ] Send command: `/status`
- [ ] Receive status response with 🟢 Online indicator

## Verification Tests

### Test 1: Bot Responds
- [ ] `/start` returns welcome message
- [ ] `/help` shows command list
- [ ] `/status` shows bot status

### Test 2: Health Check
- [ ] Run: `curl http://localhost:10000`
- [ ] Get: "IVASMS Bot is running!"

### Test 3: SMS Notification (Optional)
- [ ] Send SMS to monitored number
- [ ] Wait 30-60 seconds
- [ ] Receive notification in Telegram
- [ ] Notification includes sender, message, time

### Test 4: Admin Commands
- [ ] `/stats` shows statistics (admin only)
- [ ] `/restart` resets system (admin only)

## Logging Verification

### Check Logs
- [ ] Systemd: `sudo journalctl -u ivasms-bot -f`
- [ ] Docker: `docker logs -f ivasms-bot`
- [ ] Direct: Check console output

### Look For
- [ ] "Initial login successful!"
- [ ] "Bot started successfully..."
- [ ] No ERROR messages
- [ ] Periodic "Next check in..." messages

## Common Issues - Fix Before Going Live

### Issue: "Missing required environment variables"
- [ ] Verify all 4 variables are set
- [ ] Check spelling (case-sensitive)
- [ ] Reload terminal/server

### Issue: "Login failed - check credentials"
- [ ] Test credentials manually at ivasms.com
- [ ] Verify no typos
- [ ] Check account isn't locked
- [ ] Try from different IP

### Issue: "Telegram: Could not send message"
- [ ] Verify BOT_TOKEN is correct
- [ ] Verify CHAT_ID is correct
- [ ] Ensure bot is in group/chat
- [ ] Check group message restrictions

### Issue: "Port 10000 already in use"
- [ ] Change PORT: `export PORT=9999`
- [ ] Or: kill process using port

### Issue: "Module not found"
- [ ] Run: `pip install -r requirements.txt`
- [ ] Or: Run `./run.sh` (auto-installs)

## Production Setup

If going to production:

- [ ] Set up systemd service (Linux)
- [ ] Enable auto-start: `sudo systemctl enable ivasms-bot`
- [ ] Set up monitoring
- [ ] Configure log rotation
- [ ] Set up backup/recovery plan
- [ ] Document your setup
- [ ] Test restart/recovery

## Monitoring Plan

- [ ] Check bot status daily
- [ ] Review logs weekly
- [ ] Monitor resource usage
- [ ] Set up alerts for errors
- [ ] Plan credential rotation

## Post-Launch

- [ ] Bot running 24/7 ✓
- [ ] Notifications working ✓
- [ ] Logs being created ✓
- [ ] Health check responding ✓
- [ ] Admin commands working ✓

## Final Verification

After 24 hours of operation:

- [ ] Bot still running
- [ ] No memory leaks
- [ ] No connection issues
- [ ] SMS notifications working
- [ ] Logs show normal operation
- [ ] No errors in logs

## Maintenance Schedule

- [ ] Daily: Check bot status
- [ ] Weekly: Review logs for errors
- [ ] Monthly: Test all commands
- [ ] Quarterly: Update dependencies
- [ ] Annually: Rotate credentials

## Emergency Procedures

If bot stops:

- [ ] Check status: `sudo systemctl status ivasms-bot`
- [ ] Check logs: `sudo journalctl -u ivasms-bot -n 50`
- [ ] Restart: `sudo systemctl restart ivasms-bot`
- [ ] If still down, check credentials
- [ ] Run verify_setup.py again

If login keeps failing:

- [ ] Verify credentials manually
- [ ] Check account status
- [ ] Check IP blocking
- [ ] Try from different IP
- [ ] Contact IVASMS support

## Success Criteria

Your deployment is successful when:

✅ Bot starts without errors
✅ Telegram commands work
✅ /status shows 🟢 Online
✅ Health check responds
✅ Logs show normal operation
✅ SMS notifications arrive in Telegram
✅ Bot recovers on network issues
✅ All admin commands work

---

## Deployment Completed!

Date deployed: __________________
Deployment method used: __________________
Deployed by: __________________
Notes: __________________________________________________

For ongoing support, refer to:
- DEPLOYMENT_GUIDE.md (troubleshooting)
- README_COMPLETE.md (full docs)
- REQUIREMENTS_INFO.md (dependencies)

✅ **Status: READY FOR PRODUCTION**
