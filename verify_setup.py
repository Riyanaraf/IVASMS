#!/usr/bin/env python3
"""
IVASMS Bot - Setup Verification Script
Checks all requirements before running the bot
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def check_python_version():
    """Check Python version"""
    print_info("Checking Python version...")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str} (requirement: >= 3.8)")
        return True
    else:
        print_error(f"Python {version_str} (requirement: >= 3.8)")
        return False

def check_pip():
    """Check if pip is available"""
    print_info("Checking pip...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.split()[1]
            print_success(f"pip {version}")
            return True
        else:
            print_error("pip not available")
            return False
    except Exception as e:
        print_error(f"pip check failed: {e}")
        return False

def check_requirements_file():
    """Check if requirements.txt exists"""
    print_info("Checking requirements.txt...")
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print_success(f"requirements.txt found ({len(packages)} packages)")
        return True
    else:
        print_error("requirements.txt not found")
        return False

def check_bot_file():
    """Check if bot.py exists"""
    print_info("Checking bot.py...")
    if os.path.exists("bot.py"):
        size = os.path.getsize("bot.py")
        print_success(f"bot.py found ({size:,} bytes)")
        return True
    else:
        print_error("bot.py not found")
        return False

def check_environment_variables():
    """Check required environment variables"""
    print_info("Checking environment variables...")
    
    required_vars = {
        "IVASMS_EMAIL": "IVASMS login email",
        "IVASMS_PASSWORD": "IVASMS password",
        "BOT_TOKEN": "Telegram bot token",
        "CHAT_ID": "Telegram chat ID"
    }
    
    missing = []
    found = []
    
    for var, description in required_vars.items():
        if os.getenv(var):
            found.append(var)
        else:
            missing.append(f"{var} ({description})")
    
    for var in found:
        value = os.getenv(var)
        masked = f"{value[:20]}***" if len(value) > 20 else value
        print_success(f"{var} is set ({masked})")
    
    for var in missing:
        print_error(f"{var} is NOT set")
    
    return len(missing) == 0

def check_dependencies():
    """Check if required Python packages are installed"""
    print_info("Checking Python dependencies...")
    
    required_packages = {
        "requests": "HTTP requests",
        "bs4": "BeautifulSoup4 - HTML parsing",
        "telegram": "python-telegram-bot",
    }
    
    optional_packages = {
        "selenium": "Selenium - Cloudflare bypass",
        "undetected_chromedriver": "Undetected ChromeDriver",
    }
    
    all_good = True
    missing_required = []
    
    for package, description in required_packages.items():
        try:
            __import__(package)
            print_success(f"{package} - {description}")
        except ImportError:
            print_error(f"{package} - {description} [NOT INSTALLED]")
            missing_required.append(package)
            all_good = False
    
    print()
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print_success(f"{package} - {description} [OPTIONAL]")
        except ImportError:
            print_warning(f"{package} - {description} [OPTIONAL, NOT INSTALLED]")
    
    if missing_required:
        print(f"\n{Colors.BOLD}Install missing packages with:{Colors.RESET}")
        print(f"  pip install {' '.join(missing_required)}")
        print()
    
    return all_good

def check_network_connectivity():
    """Check network connectivity to required services"""
    print_info("Checking network connectivity...")
    
    services = {
        "IVASMS": "https://www.ivasms.com",
        "Telegram API": "https://api.telegram.org",
    }
    
    try:
        import requests
        all_ok = True
        
        for name, url in services.items():
            try:
                response = requests.head(url, timeout=5)
                if response.status_code < 500:
                    print_success(f"{name} - {url}")
                else:
                    print_warning(f"{name} - {url} (status {response.status_code})")
            except requests.RequestException as e:
                print_error(f"{name} - {url} [{str(e)[:50]}]")
                all_ok = False
        
        return all_ok
    except ImportError:
        print_warning("requests not installed, skipping connectivity check")
        return True

def check_disk_space():
    """Check available disk space"""
    print_info("Checking disk space...")
    try:
        import shutil
        usage = shutil.disk_usage(".")
        free_gb = usage.free / (1024**3)
        
        if free_gb > 1:
            print_success(f"Disk space: {free_gb:.2f} GB available")
            return True
        else:
            print_warning(f"Low disk space: {free_gb:.2f} GB available")
            return True
    except Exception as e:
        print_warning(f"Could not check disk space: {e}")
        return True

def check_port():
    """Check if default port is available"""
    print_info("Checking port 10000...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 10000))
        sock.close()
        
        if result == 0:
            print_warning("Port 10000 is in use (change via PORT environment variable)")
        else:
            print_success("Port 10000 is available")
        return True
    except Exception as e:
        print_warning(f"Could not check port: {e}")
        return True

def main():
    """Run all verification checks"""
    print_header("IVASMS Bot - Setup Verification")
    
    checks = [
        ("Python Version", check_python_version),
        ("pip", check_pip),
        ("requirements.txt", check_requirements_file),
        ("bot.py", check_bot_file),
        ("Environment Variables", check_environment_variables),
        ("Dependencies", check_dependencies),
        ("Disk Space", check_disk_space),
        ("Port Availability", check_port),
        ("Network Connectivity", check_network_connectivity),
    ]
    
    results = {}
    
    for name, check_func in checks:
        print(f"\n{Colors.BOLD}{name}:{Colors.RESET}")
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"Check failed: {e}")
            results[name] = False
    
    print_header("Verification Summary")
    
    critical_checks = ["Python Version", "bot.py", "Environment Variables", "Dependencies"]
    
    print(f"\n{Colors.BOLD}Critical Checks:{Colors.RESET}")
    for check in critical_checks:
        status = "✓" if results.get(check) else "✗"
        color = Colors.GREEN if results.get(check) else Colors.RED
        print(f"  {color}{status} {check}{Colors.RESET}")
    
    critical_pass = all(results.get(check) for check in critical_checks)
    
    print(f"\n{Colors.BOLD}Optional Checks:{Colors.RESET}")
    optional_checks = [c for c in results.keys() if c not in critical_checks]
    for check in optional_checks:
        status = "✓" if results.get(check) else "⚠"
        color = Colors.GREEN if results.get(check) else Colors.YELLOW
        print(f"  {color}{status} {check}{Colors.RESET}")
    
    print("\n" + "="*60)
    
    if critical_pass:
        print_success("All critical checks passed!")
        print(f"\n{Colors.GREEN}{Colors.BOLD}You can now run the bot with:{Colors.RESET}")
        print(f"  python3 bot.py")
        print(f"  # or")
        print(f"  ./run.sh")
        return 0
    else:
        print_error("Some critical checks failed!")
        print(f"\n{Colors.RED}{Colors.BOLD}Fix the issues above and try again.{Colors.RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
