# IVASMS Bot - Quick Start Guide

Get your bot running in 5 minutes!

## 1. Prerequisites Check

```bash
python3 --version  # Should be 3.8+
pip --version      # Should be 20.0+
```

## 2. Get Your Credentials

### IVASMS Credentials
- Email: Your IVASMS.com login email
- Password: Your IVASMS.com password
- Test at: https://www.ivasms.com/login

### Telegram Bot Token
1. Open Telegram and message @BotFather
2. Send: `/newbot`
3. Follow instructions
4. You'll get a token like: `123456789:ABCDEFGHIJKLMNOPQRSTUVWxyz`

### Telegram Chat ID
1. Send any message to your target group/chat
2. Open Telegram and message @userinfobot
3. It shows your Chat ID (e.g., 1234567890)

## 3. Linux/Mac/Pterodactyl - Quick Start

```bash
# Download files
git clone <repo-url>
cd IVASMS

# Create .env file
cat > .env << EOF
IVASMS_EMAIL=your@email.com
IVASMS_PASSWORD=yourpass
BOT_TOKEN=your_token_here
CHAT_ID=your_chat_id_here
EOF

# Run (auto-installs dependencies)
chmod +x run.sh
./run.sh
```

## 4. Windows - Quick Start

```batch
# Create .env file in same folder
# Content:
# IVASMS_EMAIL=your@email.com
# IVASMS_PASSWORD=yourpass
# BOT_TOKEN=your_token_here
# CHAT_ID=your_chat_id_here

# Run
run.bat
```

## 5. Verify It Works

You should see in console:
```
✓ Initial login successful!
Bot started successfully - monitoring for SMS...
Next check in 45.2s...
```

Send any message to your Telegram bot and you should get:
```
Bot Status: 🟢 Online and monitoring
Messages tracked: 0
```

## 6. Test SMS Notification

1. Send an SMS to any number monitored in IVASMS
2. Check your Telegram group - you should see notification with:
   - Sender number
   - Message content
   - Timestamp

## Common Issues

| Problem | Solution |
|---------|----------|
| "Missing required environment variables" | Check .env file has all 4 fields |
| "Login failed" | Verify email/password at ivasms.com |
| "Telegram: Could not send message" | Check bot token and chat ID |
| Port 10000 in use | Change PORT in .env or `export PORT=9999` |
| Module not found errors | Run `pip install -r requirements.txt` |

## Next Steps

- Check `/status` command in Telegram
- Review DEPLOYMENT_GUIDE.md for advanced setup
- Check logs for any warnings
- Set up monitoring with screen/systemd (see guide)

## Support

For detailed documentation, see: DEPLOYMENT_GUIDE.md
