#!/usr/bin/env python3
"""
IVASMS Telegram Bot - Complete Production Version
Handles Cloudflare protection, automatic login, SMS monitoring and notifications
Fully deployable on Pterodactyl Panel, VPS, or any Python server
"""

import requests
import re
import json
import time
import logging
import asyncio
import threading
import random
import os
import sys
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    import undetected_chromedriver as uc
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
)
logger = logging.getLogger(__name__)

ADMIN_IDS = [7500869913, 6524840104]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

BANNER_URL = "https://files.catbox.moe/koc535.jpg"


class HealthHandler(BaseHTTPRequestHandler):
    """HTTP Health Check Handler"""
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = b'''<!DOCTYPE html>
<html><head><title>IVASMS Bot - Running</title></head>
<body style="font-family: Arial; margin: 20px;">
<h1>IVASMS Bot Status</h1>
<p><strong>Status:</strong> <span style="color: green;">✓ Running</span></p>
<p><strong>Service:</strong> Telegram SMS Monitoring Bot</p>
<p><strong>Last Updated:</strong> {}</p>
</body></html>'''.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).encode()
        self.wfile.write(response)
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def log_message(self, format, *args):
        pass


def run_health_server():
    """Run HTTP health check server"""
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        logger.info(f"Health check server listening on 0.0.0.0:{port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"Health server error: {e}")


def get_random_headers():
    """Generate random browser headers to bypass detection"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        'Sec-Fetch-User': '?1',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="121"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
    }


def get_inline_keyboard():
    """Get Telegram inline keyboard with useful links"""
    keyboard = [
        [InlineKeyboardButton("𝐍ᴜᴍʙᴇʀ 𝐂ʜᴀɴɴᴇʟ", url="https://t.me/mrafrixtech")],
        [InlineKeyboardButton("𝐎ᴛᴘ 𝐆𝐫𝐨𝐮𝐩", url="https://t.me/afrixotpgc")],
        [InlineKeyboardButton("𝐑ᴇɴᴛ 𝐒ᴄʀɪᴘᴛ", url="https://t.me/jaden_afrix")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_powered_by_caption():
    """Get powered by caption with current year"""
    current_year = datetime.now().year
    return f"©ᴘᴏᴡᴇʀᴇᴅ ʙʏ 𝐀ᴜʀᴏʀᴀ𝐈ɪɴᴄ {current_year}"


def is_admin(user_id):
    """Check if user is admin"""
    return user_id in ADMIN_IDS


class IVASMSBot:
    """Main IVASMS Telegram Bot Class"""
    
    def __init__(self):
        self.email = os.getenv("IVASMS_EMAIL", "").strip()
        self.password = os.getenv("IVASMS_PASSWORD", "").strip()
        self.bot_token = os.getenv("BOT_TOKEN", "").strip()
        self.chat_id = os.getenv("CHAT_ID", "").strip()
        self.session = requests.Session()
        self.driver = None
        self.consecutive_failures = 0
        self.last_sms = {}
        self.login_attempts = 0
        self.csrf_token = None
        self.last_login_time = None
        
        if not all([self.email, self.password, self.bot_token, self.chat_id]):
            logger.critical("MISSING ENVIRONMENT VARIABLES")
            logger.critical(f"Email: {'SET' if self.email else 'NOT SET'}")
            logger.critical(f"Password: {'SET' if self.password else 'NOT SET'}")
            logger.critical(f"Bot Token: {'SET' if self.bot_token else 'NOT SET'}")
            logger.critical(f"Chat ID: {'SET' if self.chat_id else 'NOT SET'}")
            sys.exit(1)
        
        logger.info("Bot initialized with environment variables")
    
    def init_selenium_driver(self):
        """Initialize Selenium with undetected-chromedriver for Cloudflare bypass"""
        if not HAS_SELENIUM:
            logger.warning("Selenium not available - using requests fallback")
            return False
        
        try:
            logger.info("Initializing Selenium Chrome driver...")
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-web-resources")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--headless=new")
            options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            self.driver = uc.Chrome(options=options, version_main=None, suppress_welcome=True)
            logger.info("Chrome driver initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            self.driver = None
            return False
    
    def selenium_login(self):
        """Login using Selenium to bypass Cloudflare protection"""
        if not HAS_SELENIUM or not self.driver:
            logger.warning("Selenium unavailable, using requests")
            return self.requests_login()
        
        try:
            logger.info("Starting Selenium login...")
            
            logger.info("Warming up connection...")
            self.driver.get("https://www.ivasms.com/")
            time.sleep(random.uniform(2, 4))
            
            logger.info("Navigating to login page...")
            self.driver.get("https://www.ivasms.com/login")
            time.sleep(random.uniform(3, 5))
            
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
            )
            
            logger.info("Filling login form...")
            
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            for char in self.email:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.03, 0.12))
            
            time.sleep(random.uniform(0.5, 1.5))
            
            password_input = self.driver.find_element(By.NAME, "password")
            for char in self.password:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.03, 0.12))
            
            time.sleep(random.uniform(0.5, 1.5))
            
            logger.info("Submitting login form...")
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            logger.info("Waiting for login response...")
            time.sleep(random.uniform(4, 8))
            
            current_url = self.driver.current_url
            if any(keyword in current_url for keyword in ["dashboard", "home", "portal", "sms"]):
                logger.info("✓ Selenium login successful!")
                self.consecutive_failures = 0
                self.last_login_time = datetime.now()
                self.login_attempts = 0
                return True
            else:
                logger.error(f"Login may have failed - URL: {current_url}")
                return False
                
        except Exception as e:
            logger.error(f"Selenium login error: {e}")
            return False
    
    def requests_login(self):
        """Fallback login using requests with Cloudflare headers"""
        try:
            logger.info("Starting requests-based login...")
            
            logger.info("Warming up connection...")
            for attempt in range(3):
                try:
                    resp = self.session.get(
                        "https://www.ivasms.com/",
                        headers=get_random_headers(),
                        timeout=20,
                        verify=True
                    )
                    if resp.status_code == 200:
                        logger.info("Homepage loaded")
                        break
                except Exception as e:
                    logger.warning(f"Warmup attempt {attempt+1} failed: {e}")
                    time.sleep(random.uniform(3, 6))
            
            time.sleep(random.uniform(2, 4))
            
            logger.info("Attempting login...")
            for attempt in range(5):
                try:
                    logger.info(f"Login attempt {attempt+1}/5...")
                    
                    login_response = self.session.post(
                        "https://www.ivasms.com/login",
                        data={"email": self.email, "password": self.password},
                        headers=get_random_headers(),
                        timeout=25,
                        allow_redirects=True,
                        verify=True
                    )
                    
                    if login_response.status_code == 200:
                        if any(kw in login_response.url for kw in ["dashboard", "portal", "home", "sms"]) or \
                           any(kw in login_response.text for kw in ["Logout", "dashboard", "sms/received"]):
                            logger.info("✓ Login successful!")
                            self.consecutive_failures = 0
                            self.last_login_time = datetime.now()
                            self.login_attempts = 0
                            
                            csrf_match = re.search(r'csrf-token["\']?\s*content=["\']([^"\']+)["\']', login_response.text)
                            if csrf_match:
                                self.csrf_token = csrf_match.group(1)
                                logger.info("CSRF token extracted")
                            
                            return True
                        else:
                            logger.warning(f"Status 200 but not authenticated - URL: {login_response.url}")
                    else:
                        logger.error(f"Status {login_response.status_code}: {login_response.reason}")
                        
                except requests.Timeout:
                    logger.warning(f"Timeout on attempt {attempt+1}")
                except requests.RequestException as e:
                    logger.error(f"Request error on attempt {attempt+1}: {e}")
                
                if attempt < 4:
                    wait_time = random.uniform(5, 15) * (attempt + 1)
                    logger.info(f"Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)
            
            logger.error("All login attempts failed")
            self.consecutive_failures += 1
            self.login_attempts += 1
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error in requests login: {e}")
            self.consecutive_failures += 1
            self.login_attempts += 1
            return False
    
    def check_sms(self):
        """Check for new SMS messages from IVASMS"""
        try:
            logger.info("Fetching SMS messages...")
            
            response = self.session.get(
                "https://www.ivasms.com/api/sms",
                headers=get_random_headers(),
                timeout=20,
                verify=True
            )
            
            if response.status_code == 200:
                try:
                    sms_data = response.json()
                    new_messages = []
                    
                    if isinstance(sms_data, list):
                        for sms in sms_data:
                            sms_id = sms.get("id", str(random.random()))
                            if sms_id not in self.last_sms:
                                new_messages.append(sms)
                                self.last_sms[sms_id] = True
                    elif isinstance(sms_data, dict):
                        sms_id = sms_data.get("id", str(random.random()))
                        if sms_id not in self.last_sms:
                            new_messages.append(sms_data)
                            self.last_sms[sms_id] = True
                    
                    if new_messages:
                        logger.info(f"Found {len(new_messages)} new message(s)")
                        self.consecutive_failures = 0
                        return new_messages
                    else:
                        logger.debug("No new messages")
                        return []
                except json.JSONDecodeError:
                    logger.warning("Could not parse JSON response")
                    return []
            else:
                logger.error(f"API error: {response.status_code}")
                self.consecutive_failures += 1
                return []
                
        except Exception as e:
            logger.error(f"Error checking SMS: {e}")
            self.consecutive_failures += 1
            return []
    
    async def send_telegram_message(self, bot, message_text, silent=False):
        """Send message to Telegram"""
        try:
            await bot.send_message(
                chat_id=self.chat_id,
                text=message_text,
                parse_mode="HTML",
                disable_notification=silent
            )
            logger.info("Message sent to Telegram")
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def send_sms_notification(self, bot, sms):
        """Send SMS notification with banner to Telegram"""
        try:
            message = f"""
<b>📱 New SMS Received</b>

<b>From:</b> <code>{sms.get('sender', sms.get('from', 'Unknown'))}</code>
<b>Message:</b> {sms.get('message', sms.get('text', 'No content'))}
<b>Time:</b> {sms.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}

{get_powered_by_caption()}
"""
            
            try:
                await bot.send_photo(
                    chat_id=self.chat_id,
                    photo=BANNER_URL,
                    caption=message,
                    parse_mode="HTML",
                    reply_markup=get_inline_keyboard()
                )
                logger.info("SMS notification sent with banner")
            except Exception as photo_error:
                logger.warning(f"Could not send photo, sending text: {photo_error}")
                await self.send_telegram_message(bot, message)
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    async def handle_command(self, update, context):
        """Handle Telegram commands"""
        try:
            user_id = update.effective_user.id
            command = update.message.text.split()[0].lower() if update.message.text else ""
            
            if command == "/start":
                await update.message.reply_text(
                    "👋 Welcome to IVASMS Bot!\n\n"
                    "🤖 I monitor your ivasms.com account and notify you about incoming SMS.\n\n"
                    "📝 Commands:\n"
                    "/status - Check bot status\n"
                    "/help - Show this message\n",
                    reply_markup=get_inline_keyboard()
                )
            
            elif command == "/help":
                await update.message.reply_text(
                    "📖 Available Commands:\n\n"
                    "/start - Welcome message\n"
                    "/status - Bot status\n"
                    "/help - This message\n"
                    "/stats - Admin stats (admin only)\n"
                    "/restart - Restart monitoring (admin only)\n",
                    reply_markup=get_inline_keyboard()
                )
            
            elif command == "/status":
                status = "🟢 Online" if self.consecutive_failures < 5 else f"🟡 Issues ({self.consecutive_failures} failures)"
                last_login = self.last_login_time.strftime("%Y-%m-%d %H:%M:%S") if self.last_login_time else "Never"
                
                await update.message.reply_text(
                    f"Bot Status: {status}\n"
                    f"Messages tracked: {len(self.last_sms)}\n"
                    f"Last login: {last_login}\n"
                    f"Consecutive failures: {self.consecutive_failures}\n\n"
                    f"{get_powered_by_caption()}",
                    reply_markup=get_inline_keyboard()
                )
            
            elif command == "/stats" and is_admin(user_id):
                await update.message.reply_text(
                    f"📊 Admin Statistics:\n"
                    f"Messages tracked: {len(self.last_sms)}\n"
                    f"Consecutive failures: {self.consecutive_failures}\n"
                    f"Login attempts: {self.login_attempts}\n"
                    f"Last login: {self.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_login_time else 'Never'}\n"
                    f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"{get_powered_by_caption()}",
                    reply_markup=get_inline_keyboard()
                )
            
            elif command == "/restart" and is_admin(user_id):
                await update.message.reply_text("🔄 Restarting monitoring system...")
                self.consecutive_failures = 0
                self.login_attempts = 0
                logger.info(f"Bot restarted by admin {user_id}")
        
        except Exception as e:
            logger.error(f"Error handling command: {e}")


async def main():
    """Main bot execution function"""
    
    logger.info("=" * 60)
    logger.info("IVASMS Telegram Bot - Starting")
    logger.info("=" * 60)
    
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    try:
        bot = Bot(token=os.getenv("BOT_TOKEN"))
        application = Application.builder().token(os.getenv("BOT_TOKEN")).build()
        
        ivasms = IVASMSBot()
        
        application.add_handler(CommandHandler("start", ivasms.handle_command))
        application.add_handler(CommandHandler("help", ivasms.handle_command))
        application.add_handler(CommandHandler("status", ivasms.handle_command))
        application.add_handler(CommandHandler("stats", ivasms.handle_command))
        application.add_handler(CommandHandler("restart", ivasms.handle_command))
        
        await application.initialize()
        await application.start()
        
        logger.info("Attempting initial login...")
        if HAS_SELENIUM:
            logger.info("Selenium available, trying Chrome driver login...")
            if ivasms.init_selenium_driver():
                login_success = ivasms.selenium_login()
            else:
                logger.info("Fallback to requests login...")
                login_success = ivasms.requests_login()
        else:
            logger.info("Using requests-based login...")
            login_success = ivasms.requests_login()
        
        if not login_success:
            logger.error("CRITICAL: Initial login failed!")
            logger.error("Check your credentials (IVASMS_EMAIL, IVASMS_PASSWORD)")
            await application.stop()
            return
        
        logger.info("✓ Initial login successful!")
        logger.info("Bot started successfully - monitoring for SMS...")
        
        check_interval = 30
        failed_checks = 0
        
        try:
            while True:
                try:
                    sms_messages = ivasms.check_sms()
                    
                    if sms_messages:
                        for sms in sms_messages:
                            await ivasms.send_sms_notification(bot, sms)
                        failed_checks = 0
                    else:
                        failed_checks += 1
                    
                    wait_time = random.uniform(check_interval - 5, check_interval + 5)
                    logger.debug(f"Next check in {wait_time:.1f}s...")
                    await asyncio.sleep(wait_time)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                    ivasms.consecutive_failures += 1
                    failed_checks += 1
                    
                    if ivasms.consecutive_failures >= 10:
                        logger.warning("Too many failures, attempting re-login...")
                        if HAS_SELENIUM and ivasms.driver:
                            if ivasms.selenium_login():
                                ivasms.consecutive_failures = 0
                                failed_checks = 0
                        else:
                            if ivasms.requests_login():
                                ivasms.consecutive_failures = 0
                                failed_checks = 0
                    
                    await asyncio.sleep(random.uniform(30, 60))
        
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        finally:
            if ivasms.driver:
                try:
                    ivasms.driver.quit()
                except:
                    pass
            await application.stop()
            logger.info("Bot stopped")
    
    except Exception as e:
        logger.critical(f"Fatal error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot terminated by user")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        sys.exit(1)
