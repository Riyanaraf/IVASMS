# IVASMS Telegram Bot - Production Ready

<div align="center">

**Complete SMS Monitoring Bot for IVASMS.com with Cloudflare Protection Bypass**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Production](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](README_COMPLETE.md)

[Quick Start](#quick-start) • [Installation](#installation) • [Configuration](#configuration) • [Troubleshooting](#troubleshooting) • [Deployment](#deployment)

</div>

---

## Overview

**IVASMS Bot** is a production-grade Telegram bot that:

✅ Monitors IVASMS.com accounts for incoming SMS messages  
✅ Bypasses Cloudflare protection with Selenium + undetected-chromedriver  
✅ Handles automatic login with exponential retry backoff  
✅ Sends formatted SMS notifications to Telegram with custom buttons  
✅ Provides admin commands for status, statistics, and control  
✅ Runs health check server for monitoring/load balancers  
✅ Deploys on Pterodactyl Panel, VPS, Docker, systemd, or any Python server  
✅ **ZERO ERRORS** - Comprehensive error handling and logging  
✅ **SINGLE FILE** - All code consolidated in bot.py  
✅ **PRODUCTION TESTED** - Used in production environments  

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ivasms-bot.git
cd ivasms-bot

# 2. Set environment variables
export IVASMS_EMAIL="your@email.com"
export IVASMS_PASSWORD="yourpassword"
export BOT_TOKEN="123456:ABC-DEF..."
export CHAT_ID="1234567890"

# 3. Install and run
pip install -r requirements.txt
python3 bot.py
```

See [QUICKSTART.md](QUICKSTART.md) for detailed quick start guide.

## Installation

### Linux/macOS

```bash
# Clone and enter directory
git clone <repo-url>
cd ivasms-bot

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Run setup verification
python3 verify_setup.py

# Option 1: Direct execution
python3 bot.py

# Option 2: Using provided script
chmod +x run.sh
./run.sh

# Option 3: As systemd service (recommended for production)
sudo -E ./install-systemd.sh
# Then: sudo systemctl status ivasms-bot
```

### Windows

```batch
# Clone and enter directory
git clone <repo-url>
cd ivasms-bot

# Create .env file
copy .env.example .env
REM Edit .env with your credentials

# Run setup verification
python verify_setup.py

# Option 1: Direct execution
python bot.py

# Option 2: Using provided script
run.bat
```

### Docker

```bash
# Build image
docker build -t ivasms-bot .

# Run with environment variables
docker run -d \
  -e IVASMS_EMAIL="your@email.com" \
  -e IVASMS_PASSWORD="password" \
  -e BOT_TOKEN="token" \
  -e CHAT_ID="chatid" \
  -p 10000:10000 \
  ivasms-bot

# Or with docker-compose
docker-compose up -d
```

### Pterodactyl Panel

1. Create server with Python 3.11 egg
2. Upload files:
   - bot.py
   - requirements.txt
   - run.sh
3. In admin panel, set startup command: `./run.sh`
4. Set environment variables
5. Start server

### VPS/Server (systemd)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip git -y

# Clone repository
git clone <repo-url>
cd ivasms-bot

# Set environment variables
export IVASMS_EMAIL="your@email.com"
export IVASMS_PASSWORD="password"
export BOT_TOKEN="token"
export CHAT_ID="chatid"

# Install as systemd service
sudo -E ./install-systemd.sh

# Manage service
sudo systemctl status ivasms-bot
sudo systemctl restart ivasms-bot
sudo journalctl -u ivasms-bot -f
```

## Configuration

### Required Environment Variables

| Variable | Type | Example | Required |
|----------|------|---------|----------|
| `IVASMS_EMAIL` | string | `user@example.com` | ✓ Yes |
| `IVASMS_PASSWORD` | string | `MyPassword123!` | ✓ Yes |
| `BOT_TOKEN` | string | `123456:ABCDEFGhijk...` | ✓ Yes |
| `CHAT_ID` | string | `1234567890` | ✓ Yes |
| `PORT` | integer | `10000` | Optional |

### Optional Environment Variables

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `PORT` | integer | `10000` | Health check server port |
| `LOG_LEVEL` | string | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

### How to Get Credentials

#### IVASMS Credentials
1. Go to https://www.ivasms.com/login
2. Enter your email and password
3. Use exact same credentials

#### Telegram Bot Token
1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow instructions
4. Copy the token (e.g., `123456789:ABCDEFGHIJKLMNOPQRSTUVWxyz`)

#### Telegram Chat ID
1. Send message to your target chat/group
2. Open Telegram and message [@userinfobot](https://t.me/userinfobot)
3. It shows your chat ID (e.g., `1234567890` or `-1001234567890` for groups)

## Bot Commands

Use these commands in Telegram:

| Command | Description | Admin Only | Example |
|---------|-------------|-----------|---------|
| `/start` | Welcome message | No | Shows bot info |
| `/help` | List all commands | No | Shows available commands |
| `/status` | Check bot status | No | Shows online/offline status |
| `/stats` | Detailed statistics | Yes | Shows message count, failures |
| `/restart` | Restart monitoring | Yes | Resets failure counter |

## Project Structure

```
ivasms-bot/
├── bot.py                    # Main bot application (ALL-IN-ONE)
├── requirements.txt          # Python dependencies
├── .env.example             # Configuration template
├── run.sh                   # Linux startup script
├── run.bat                  # Windows startup script
├── verify_setup.py          # Setup verification tool
├── install-systemd.sh       # Systemd installation script
├── docker-compose.yml       # Docker compose configuration
├── Dockerfile              # Docker image definition
├── ivasms-bot.service      # Systemd service file
├── QUICKSTART.md           # Quick start guide
├── DEPLOYMENT_GUIDE.md     # Detailed deployment guide
├── README_COMPLETE.md      # This file
└── sms_statistics.json     # SMS tracking data (auto-created)
```

## Deployment Options

### Option 1: Direct Python (Development)
```bash
python3 bot.py
```
- Simplest setup
- Good for testing/development
- Press Ctrl+C to stop

### Option 2: Docker (Containerized)
```bash
docker-compose up -d
curl http://localhost:10000  # Health check
docker logs -f ivasms-bot
```
- Best for cloud hosting
- Isolated environment
- Easy to scale

### Option 3: Systemd Service (Production Linux)
```bash
sudo systemctl start ivasms-bot
sudo systemctl status ivasms-bot
sudo journalctl -u ivasms-bot -f
```
- Starts automatically on reboot
- Restarts on failure
- Professional monitoring

### Option 4: Pterodactyl Panel
```
Set startup command to: ./run.sh
```
- Integrated with panel
- Easy remote management
- Built-in restart handling

### Option 5: PM2 (Process Manager)
```bash
npm install -g pm2
pm2 start bot.py --name "ivasms-bot"
pm2 save
pm2 startup
```
- Monitor multiple processes
- Auto-restart on crash
- Clustering support

## Monitoring & Logs

### Console Output
Logs are printed to console with timestamps and log levels:
```
2025-02-13 10:30:45 - INFO - [IVASMSBot] Initial login successful!
2025-02-13 10:31:15 - INFO - [IVASMSBot] Found 1 new message(s)
2025-02-13 10:31:16 - INFO - [NOTIFICATION] SMS notification sent
```

### Log Levels
- `DEBUG` - Detailed debug information
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical system errors

### Health Check Endpoint

```bash
# Check if bot is running
curl http://localhost:10000/

# Response:
# HTTP 200 OK
# <html>
#   <h1>IVASMS Bot Status</h1>
#   <p>Status: ✓ Running</p>
# </html>
```

### Systemd Logs

```bash
# View logs
sudo journalctl -u ivasms-bot

# Follow logs in real-time
sudo journalctl -u ivasms-bot -f

# Last 50 lines
sudo journalctl -u ivasms-bot -n 50

# Since last boot
sudo journalctl -u ivasms-bot -b
```

## Troubleshooting

### Issue: "Missing required environment variables"

**Cause:** One or more environment variables not set

**Solution:**
```bash
# Check which are missing
python3 verify_setup.py

# Set variables
export IVASMS_EMAIL="your@email.com"
export IVASMS_PASSWORD="yourpassword"
export BOT_TOKEN="token"
export CHAT_ID="chatid"

# Or use .env file
cp .env.example .env
# Edit .env with your values
python3 bot.py  # Will auto-read .env
```

### Issue: "Login failed - check your credentials"

**Cause:** Invalid email/password or account locked

**Solution:**
1. Test credentials manually at https://www.ivasms.com/login
2. Check for typos in IVASMS_EMAIL and IVASMS_PASSWORD
3. Check if account is locked or IP banned
4. Try from different IP address
5. Check IVASMS.com status page

### Issue: "Selenium not available - using requests fallback"

**Cause:** Selenium/Chrome not installed (not critical)

**Solution:**
```bash
# Bot will still work with requests + advanced headers
# Optional: Install Selenium for better Cloudflare bypass
pip install selenium undetected-chromedriver

# Or on Debian/Ubuntu:
sudo apt install chromium-browser chromium-driver
```

### Issue: "Telegram: Could not send message"

**Cause:** Invalid bot token or chat ID

**Solution:**
1. Verify BOT_TOKEN is correct (from @BotFather)
2. Verify CHAT_ID is correct (from @userinfobot)
3. Ensure bot is added to the group
4. Check if group has message restrictions
5. Verify bot has send_messages permission

### Issue: "Port 10000 already in use"

**Cause:** Another process using port 10000

**Solution:**
```bash
# Option 1: Use different port
export PORT=9999
python3 bot.py

# Option 2: Kill process using port (Linux)
lsof -i :10000  # Find process
kill -9 <PID>   # Kill it

# Option 3: On Windows
netstat -ano | findstr :10000
taskkill /PID <PID> /F
```

### Issue: "Module not found" errors

**Cause:** Dependencies not installed

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install requests beautifulsoup4 python-telegram-bot selenium undetected-chromedriver

# Verify installation
python3 -c "import requests, bs4, telegram, selenium; print('All OK')"
```

### Issue: "Memory/CPU usage too high"

**Cause:** Check interval too aggressive or infinite loops

**Solution:**
Edit bot.py line ~510:
```python
check_interval = 60  # Increase from 30 (seconds between checks)
```

### Issue: "Bot keeps crashing/restarting"

**Cause:** Unhandled exceptions or connection issues

**Solution:**
1. Check logs: `sudo journalctl -u ivasms-bot -f`
2. Run setup verification: `python3 verify_setup.py`
3. Check network connectivity
4. Verify environment variables are correct

## Advanced Configuration

### Custom Check Interval

Edit bot.py around line 510:
```python
check_interval = 60  # Changed from 30 seconds
```

### Custom Admin IDs

Edit bot.py line 39:
```python
ADMIN_IDS = [7500869913, 6524840104, 1234567890]  # Add your Telegram user IDs
```

### Custom Keyboard Buttons

Edit bot.py `get_inline_keyboard()` function:
```python
def get_inline_keyboard():
    keyboard = [
        [InlineKeyboardButton("My Custom Button", url="https://your-url.com")],
        [InlineKeyboardButton("Another Button", callback_data="action")],
    ]
    return InlineKeyboardMarkup(keyboard)
```

### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
python3 bot.py
```

## Performance Optimization

### For Low-Resource Servers

```python
# Increase check interval to reduce CPU usage
check_interval = 120  # Check every 2 minutes instead of 30 seconds

# Reduce login retry attempts
for attempt in range(3):  # Changed from 5
```

### For High-Volume Monitoring

```python
# Decrease check interval for faster SMS detection
check_interval = 10  # Check every 10 seconds

# Increase concurrent connections (not recommended)
session = requests.Session()
session.max_retries = Retry(total=5)
```

## Security Best Practices

1. **Never commit .env files to git**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use strong passwords**
   - IVASMS password: 12+ characters, mixed case, numbers, symbols
   - Telegram: Use 2FA on Telegram account

3. **Rotate credentials regularly**
   - Change IVASMS password monthly
   - Regenerate Telegram bot token yearly

4. **Restrict bot access**
   - Only add trusted admins
   - Use channel/group privacy settings
   - Don't share bot token publicly

5. **Monitor logs regularly**
   ```bash
   sudo journalctl -u ivasms-bot | grep ERROR
   ```

6. **Use HTTPS/SSH**
   - For any remote connections use SSH
   - Never expose bot to HTTP without authentication

## License & Attribution

- **Author:** IVASMS Bot Team
- **License:** MIT
- **Status:** Production Ready
- **Python Version:** 3.8+

## Support & Contributing

For issues, feature requests, or contributions:

1. Check [Troubleshooting](#troubleshooting) section
2. Run setup verification: `python3 verify_setup.py`
3. Check logs: `sudo journalctl -u ivasms-bot -f`
4. Open GitHub issue with logs and configuration

## Changelog

### v1.0.0 (Current)
- ✅ Complete bot consolidation into single file
- ✅ Cloudflare protection bypass with Selenium
- ✅ Comprehensive error handling
- ✅ Multi-platform deployment support
- ✅ Detailed documentation
- ✅ Setup verification tool
- ✅ Production ready

---

<div align="center">

**Made with ❤️ for IVASMS Monitoring**

[⬆ Back to top](#ivasms-telegram-bot---production-ready)

</div>
