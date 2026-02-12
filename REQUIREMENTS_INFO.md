# IVASMS Bot - Requirements & Dependencies

## System Requirements

### Minimum
- **OS:** Linux, Windows, macOS, or any Unix-like system
- **Python:** 3.8 or higher
- **RAM:** 100 MB minimum
- **Disk:** 200 MB for installation (+ dependencies)
- **Network:** Stable internet connection (1 Mbps+)

### Recommended for Production
- **OS:** Ubuntu 20.04+ or CentOS 8+
- **Python:** 3.10 or higher
- **RAM:** 512 MB
- **Disk:** 1 GB SSD
- **CPU:** 1 vCPU minimum
- **Network:** 10+ Mbps

## Python Dependencies

All dependencies are listed in `requirements.txt`. Install with:

```bash
pip install -r requirements.txt
```

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| requests | 2.31.0 | HTTP requests for login & API calls |
| beautifulsoup4 | 4.12.2 | HTML parsing for responses |
| python-telegram-bot | 20.3 | Telegram bot API integration |
| selenium | 4.15.2 | Browser automation (optional but recommended) |
| undetected-chromedriver | 3.5.4 | Cloudflare bypass with Chrome (optional) |
| webdriver-manager | 4.0.1 | Automatic ChromeDriver management (optional) |

### What Each Package Does

#### requests (REQUIRED)
- Makes HTTP requests to IVASMS.com
- Handles login and API calls
- **Cannot be omitted**

```python
import requests
response = requests.post("https://www.ivasms.com/login", data={...})
```

#### beautifulsoup4 (REQUIRED)
- Parses HTML responses
- Extracts data from web pages
- **Cannot be omitted**

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
```

#### python-telegram-bot (REQUIRED)
- Sends messages to Telegram
- Handles bot commands
- **Cannot be omitted**

```python
from telegram import Bot
bot = Bot(token="YOUR_TOKEN")
```

#### selenium (RECOMMENDED)
- Browser automation
- Handles Cloudflare challenges
- **Optional but highly recommended**
- Bot will work without it (uses requests fallback)

```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.ivasms.com/login")
```

#### undetected-chromedriver (RECOMMENDED)
- Evades anti-bot detection
- Works with Cloudflare
- **Optional but highly recommended**
- Requires Chrome/Chromium browser

```python
import undetected_chromedriver as uc
driver = uc.Chrome()
```

#### webdriver-manager (OPTIONAL)
- Automatically manages ChromeDriver version
- Prevents version conflicts
- Makes Selenium easier to setup

```python
from webdriver_manager.chrome import ChromeDriverManager
```

## Installation Methods

### 1. Using pip (Recommended)

```bash
pip install -r requirements.txt
```

**Pros:**
- Simple and standard
- Works everywhere
- Easy to manage versions

**Cons:**
- May have version conflicts on some systems

### 2. Using pip with --upgrade

```bash
pip install --upgrade -r requirements.txt
```

**Pros:**
- Gets latest compatible versions
- Fixes outdated packages

**Cons:**
- May break compatibility if versions change

### 3. Using virtual environment (Recommended for production)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

**Pros:**
- Isolates dependencies
- No conflicts with system packages
- Professional standard
- Easy to replicate

**Cons:**
- Requires activation each time

### 4. Using conda

```bash
conda create -n ivasms python=3.11
conda activate ivasms
pip install -r requirements.txt
```

**Pros:**
- Good for data science workflows
- Easy environment management
- Cross-platform

**Cons:**
- Overkill for this use case
- Requires conda installation

## Verification

### Check all packages are installed

```bash
python3 -c "import requests, bs4, telegram, selenium, undetected_chromedriver; print('All packages OK')"
```

### Or use our verification tool

```bash
python3 verify_setup.py
```

This will check:
- ✓ Python version
- ✓ pip availability
- ✓ All required packages
- ✓ Optional packages
- ✓ Network connectivity
- ✓ Port availability
- ✓ Environment variables

## Troubleshooting Dependency Issues

### Issue: "ModuleNotFoundError: No module named 'requests'"

**Solution:**
```bash
pip install requests==2.31.0
```

### Issue: "pip: command not found"

**Solution:**
```bash
# Python 3
python3 -m pip install -r requirements.txt

# Or install pip
python3 -m ensurepip --upgrade
pip install -r requirements.txt
```

### Issue: "Permission denied" when installing

**Solution:**
```bash
# Option 1: Use --user flag
pip install --user -r requirements.txt

# Option 2: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 3: Use sudo (not recommended)
sudo pip install -r requirements.txt
```

### Issue: "Incompatible versions"

**Solution:**
```bash
# Clear pip cache
pip cache purge

# Upgrade pip
pip install --upgrade pip

# Install with compatible versions
pip install -r requirements.txt
```

### Issue: "Selenium: ChromeDriver not found"

**Solution:**
```bash
# Install webdriver-manager
pip install webdriver-manager

# Or install Chrome/Chromium
# Ubuntu/Debian
sudo apt install chromium-browser

# Fedora
sudo dnf install chromium

# macOS
brew install chromium

# Then webdriver-manager will auto-manage it
```

## Optional: Installing Selenium & ChromeDriver

Selenium is optional but highly recommended for Cloudflare bypass.

### 1. Install Selenium packages

```bash
pip install selenium undetected-chromedriver webdriver-manager
```

### 2. Install Chrome/Chromium browser

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install chromium-browser
```

**Linux (Fedora/CentOS):**
```bash
sudo dnf install chromium
```

**macOS:**
```bash
brew install chromium
```

**Windows:**
- Download from https://www.google.com/chrome/
- Or use Chromium portable

### 3. Verify Selenium works

```bash
python3 -c "import selenium; import undetected_chromedriver; print('Selenium OK')"
```

## Optional Dependencies Explained

### When You NEED Selenium
- Cloudflare is heavily blocking your requests
- Regular requests keep getting 403 errors
- You want browser automation for other tasks
- You have Chrome/Chromium available

### When You DON'T NEED Selenium
- Bot works fine with requests fallback
- Server doesn't have GUI (headless servers)
- You want minimal resource usage
- GUI-less Docker environment

The bot **will work without Selenium** - it has built-in fallback to use requests with advanced headers.

## Linux System Dependencies

For some packages, you may need system libraries:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-dev python3-pip python3-venv -y
# For Selenium
sudo apt install chromium-browser chromium-driver -y
# For SSL
sudo apt install libssl-dev -y
```

**Fedora/CentOS:**
```bash
sudo dnf install python3-devel python3-pip -y
# For Selenium
sudo dnf install chromium -y
# For SSL
sudo dnf install openssl-devel -y
```

**Alpine (Docker):**
```dockerfile
RUN apk add --no-cache python3 py3-pip chromium chromium-chromedriver
```

## Docker Dependency Handling

If using Docker, all dependencies are handled in the Dockerfile:

```dockerfile
RUN pip install -r requirements.txt
```

The Dockerfile also installs:
- Python 3.11
- chromium-browser
- chromium-driver
- Required system libraries

## Minimum Installation (If Limited)

If you have severe resource constraints:

```bash
# Only required packages
pip install requests beautifulsoup4 python-telegram-bot

# Skip optional packages:
# selenium, undetected-chromedriver, webdriver-manager
```

**Note:** Bot will use requests fallback instead of Selenium. May have issues with aggressive Cloudflare.

## Checking Specific Package Version

```bash
# Check installed version
pip show requests

# Check if specific version is available
pip index versions requests

# Force specific version
pip install requests==2.31.0
```

## Requirements Lock File

For production, you may want to lock exact versions:

```bash
# Generate lock file
pip freeze > requirements-lock.txt

# Use lock file
pip install -r requirements-lock.txt
```

This ensures exact reproducibility across environments.

## Environment-Specific Requirements

### Docker
All requirements included in Dockerfile

### Pterodactyl Panel
Install via egg or manual pip install

### Systemd Service
Install in virtual environment under `/opt/ivasms-bot/venv`

### VPS Manual
Install system Python, pip, then run pip install -r requirements.txt

### Windows
Use system Python, pip will handle everything

### Raspberry Pi / ARM
Same as Linux, but may need to compile some packages

## Final Verification

After installation, verify everything:

```bash
# Run verification script
python3 verify_setup.py

# Or manual check
python3 -c "
import requests
import bs4
import telegram
from selenium import webdriver
import undetected_chromedriver as uc
print('✓ All dependencies installed')
"
```

## Support

If you have dependency issues:

1. Run `python3 verify_setup.py`
2. Check error messages
3. Use `pip list` to see installed packages
4. Try `pip install --upgrade pip setuptools wheel`
5. Clear pip cache: `pip cache purge`
6. Try fresh install in virtual environment

---

**Status: All dependencies documented and verified** ✅
