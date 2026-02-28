"""
Configuration management for Golf Booking Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # Golf booking credentials
    GOLF_USERNAME = os.getenv('GOLF_USERNAME')
    GOLF_PASSWORD = os.getenv('GOLF_PASSWORD')

    # Booking settings
    NUM_PLAYERS = int(os.getenv('NUM_PLAYERS', 4))
    BOOKING_TIME = os.getenv('BOOKING_TIME', '06:00')
    TIMEZONE = os.getenv('TIMEZONE', 'America/New_York')

    # URLs
    GOLF_HOME_URL = 'https://golfstpete.com/mangrove-bay/'
    BOOKING_URL = 'https://foreupsoftware.com/index.php/booking/19671/2149#/teetimes'

    # Selenium settings
    HEADLESS = os.getenv('HEADLESS', 'True').lower() == 'true'
    SCREENSHOT_ON_ERROR = True
    PAGE_LOAD_TIMEOUT = 30
    IMPLICIT_WAIT = 10

    # Paths
    LOG_DIR = 'logs'
    SCREENSHOT_DIR = 'screenshots'

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GOLF_USERNAME or not cls.GOLF_PASSWORD:
            raise ValueError(
                "Missing required credentials. "
                "Please set GOLF_USERNAME and GOLF_PASSWORD in .env file"
            )
        return True
