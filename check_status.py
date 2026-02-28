#!/usr/bin/env python3
"""
Status checker for Golf Booking Bot
Verifies configuration and system readiness
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess

def check_item(name, check_func):
    """Run a check and print result"""
    try:
        result = check_func()
        if result:
            print(f"✓ {name}")
            return True
        else:
            print(f"✗ {name}")
            return False
    except Exception as e:
        print(f"✗ {name}: {e}")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    return version.major == 3 and version.minor >= 8

def check_env_file():
    """Check if .env file exists"""
    return Path('.env').exists()

def check_credentials():
    """Check if credentials are set"""
    from config import Config
    try:
        Config.validate()
        return True
    except:
        return False

def check_chrome():
    """Check if Chrome is installed"""
    try:
        result = subprocess.run(
            ['google-chrome', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        # Try chromium on Mac
        try:
            result = subprocess.run(
                ['chromium', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

def check_dependencies():
    """Check if Python dependencies are installed"""
    try:
        import selenium
        import apscheduler
        from dotenv import load_dotenv
        import pytz
        return True
    except ImportError:
        return False

def check_directories():
    """Check if required directories exist"""
    return (Path('logs').exists() and
            Path('screenshots').exists())

def main():
    """Run all checks"""
    print("="*60)
    print("Golf Booking Bot - Status Check")
    print("="*60)
    print()

    checks = [
        ("Python 3.8+", check_python_version),
        ("Dependencies installed", check_dependencies),
        (".env file exists", check_env_file),
        ("Credentials configured", check_credentials),
        ("Chrome/Chromium installed", check_chrome),
        ("Required directories", check_directories),
    ]

    results = []
    for name, check_func in checks:
        results.append(check_item(name, check_func))

    print()
    print("="*60)

    if all(results):
        print("✓ All checks passed! Bot is ready to run.")
        print()
        print("To test the bot:")
        print("  python test_booking.py")
        print()
        print("To start the scheduler:")
        print("  python scheduler.py")
        print("="*60)
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Create .env file: cp .env.example .env")
        print("  - Add credentials to .env file")
        print("  - Create directories: mkdir logs screenshots")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
