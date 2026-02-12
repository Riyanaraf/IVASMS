#!/bin/bash

# IVASMS Bot - Systemd Service Installation Script
# Run as root to install bot as a system service

echo "======================================"
echo "IVASMS Bot - Systemd Service Setup"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "ERROR: This script must be run as root"
    echo "Usage: sudo ./install-systemd.sh"
    exit 1
fi

# Check for required environment variables
echo "Checking required environment variables..."

if [ -z "$IVASMS_EMAIL" ] || [ -z "$IVASMS_PASSWORD" ] || [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
    echo "ERROR: Missing required environment variables!"
    echo "Please set: IVASMS_EMAIL, IVASMS_PASSWORD, BOT_TOKEN, CHAT_ID"
    exit 1
fi

echo "✓ All environment variables found"
echo ""

# Get current user (should be called with: sudo -E ./install-systemd.sh or set user manually)
BOT_USER="${SUDO_USER:-$(whoami)}"
BOT_HOME="/opt/ivasms-bot"
BOT_GROUP="$BOT_USER"

echo "Installation Configuration:"
echo "  Bot User: $BOT_USER"
echo "  Bot Group: $BOT_GROUP"
echo "  Bot Directory: $BOT_HOME"
echo ""

# Create installation directory
if [ ! -d "$BOT_HOME" ]; then
    echo "Creating installation directory..."
    mkdir -p "$BOT_HOME"
fi

# Copy files
echo "Copying bot files..."
cp bot.py "$BOT_HOME/"
cp requirements.txt "$BOT_HOME/"
chmod 755 "$BOT_HOME"
chmod 644 "$BOT_HOME"/*.py "$BOT_HOME"/*.txt

# Create .env file
echo "Creating .env file..."
cat > "$BOT_HOME/.env" << EOF
IVASMS_EMAIL=$IVASMS_EMAIL
IVASMS_PASSWORD=$IVASMS_PASSWORD
BOT_TOKEN=$BOT_TOKEN
CHAT_ID=$CHAT_ID
PORT=10000
EOF

chmod 600 "$BOT_HOME/.env"
chown "$BOT_USER:$BOT_GROUP" "$BOT_HOME/.env"

# Create virtual environment
echo "Creating Python virtual environment..."
cd "$BOT_HOME"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
deactivate

echo "✓ Virtual environment created and dependencies installed"
echo ""

# Fix permissions
chown -R "$BOT_USER:$BOT_GROUP" "$BOT_HOME"
chmod 755 "$BOT_HOME"

# Create systemd service file
echo "Installing systemd service..."
SYSTEMD_FILE="/etc/systemd/system/ivasms-bot.service"

cat > "$SYSTEMD_FILE" << EOF
[Unit]
Description=IVASMS Telegram Bot Service
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$BOT_USER
Group=$BOT_GROUP
WorkingDirectory=$BOT_HOME
EnvironmentFile=$BOT_HOME/.env
ExecStart=$BOT_HOME/venv/bin/python3 $BOT_HOME/bot.py
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ivasms-bot
Environment="PYTHONUNBUFFERED=1"

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$BOT_HOME

# Limits
StartLimitBurst=5
StartLimitIntervalSec=300

[Install]
WantedBy=multi-user.target
EOF

chmod 644 "$SYSTEMD_FILE"

# Reload systemd daemon
echo "Reloading systemd daemon..."
systemctl daemon-reload

# Enable service
echo "Enabling service to start on boot..."
systemctl enable ivasms-bot.service

# Start service
echo "Starting IVASMS Bot service..."
systemctl start ivasms-bot.service

# Check status
sleep 2
if systemctl is-active --quiet ivasms-bot.service; then
    echo ""
    echo "======================================"
    echo "✓ Installation Successful!"
    echo "======================================"
    echo ""
    echo "Service Management Commands:"
    echo "  Start:    sudo systemctl start ivasms-bot"
    echo "  Stop:     sudo systemctl stop ivasms-bot"
    echo "  Restart:  sudo systemctl restart ivasms-bot"
    echo "  Status:   sudo systemctl status ivasms-bot"
    echo "  Logs:     sudo journalctl -u ivasms-bot -f"
    echo ""
    echo "Files:"
    echo "  Installation: $BOT_HOME"
    echo "  Service:      $SYSTEMD_FILE"
    echo "  Config:       $BOT_HOME/.env"
    echo ""
    echo "To remove service:"
    echo "  sudo systemctl stop ivasms-bot"
    echo "  sudo systemctl disable ivasms-bot"
    echo "  sudo rm $SYSTEMD_FILE"
    echo "  sudo systemctl daemon-reload"
    exit 0
else
    echo ""
    echo "ERROR: Service failed to start!"
    echo "Check logs with: sudo journalctl -u ivasms-bot"
    exit 1
fi
