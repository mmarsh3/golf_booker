"""
Golf Tee Time Booking Bot using Selenium
"""
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from config import Config

# Create required directories
Path(Config.LOG_DIR).mkdir(exist_ok=True)
Path(Config.SCREENSHOT_DIR).mkdir(exist_ok=True)

# Setup logging
log_file = Path(Config.LOG_DIR) / f'booking_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GolfBookingBot:
    """Automated golf tee time booking bot"""

    def __init__(self):
        """Initialize the booking bot"""
        Config.validate()
        self.driver = None
        self.wait = None
        self.booking_date = None
        self.screenshot_counter = 0

    def setup_driver(self):
        """Configure and initialize Chrome WebDriver"""
        logger.info("Setting up Chrome WebDriver...")

        chrome_options = Options()
        if Config.HEADLESS:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        self.wait = WebDriverWait(self.driver, Config.PAGE_LOAD_TIMEOUT)

        logger.info("WebDriver setup complete")

    def take_screenshot(self, name):
        """Take a screenshot for debugging"""
        if Config.SCREENSHOT_ON_ERROR:
            screenshot_path = Path(Config.SCREENSHOT_DIR) / f'{name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            self.driver.save_screenshot(str(screenshot_path))
            logger.info(f"Screenshot saved: {screenshot_path}")

    def calculate_booking_date(self):
        """Calculate the date 7 days in the future (when tee times open)"""
        self.booking_date = datetime.now() + timedelta(days=7)
        logger.info(f"Target booking date: {self.booking_date.strftime('%Y-%m-%d')}")
        return self.booking_date

    def navigate_to_booking_page(self):
        """Navigate to the booking system"""
        logger.info("Navigating to booking page...")

        try:
            # Go directly to booking URL
            self.driver.get(Config.BOOKING_URL)
            time.sleep(5)  # Allow page to fully load
            self.take_screenshot('01_booking_page_loaded')
            logger.info("Booking page loaded successfully")

        except Exception as e:
            logger.error(f"Error navigating to booking page: {e}")
            self.take_screenshot('error_navigation')
            raise

    def login_in_popup(self):
        """Log in via the popup that appears after selecting a tee time"""
        logger.info("Attempting to log in via popup...")

        try:
            # Wait for login form to appear in popup
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "login_email"))
            )
            password_field = self.driver.find_element(By.ID, "login_password")

            # Enter credentials
            username_field.clear()
            username_field.send_keys(Config.GOLF_USERNAME)
            password_field.clear()
            password_field.send_keys(Config.GOLF_PASSWORD)

            self.take_screenshot('03_credentials_entered_popup')
            logger.info("Credentials entered in popup")

            # Submit login form - try multiple button selectors
            submit_selectors = [
                "//button[@type='submit']",
                "//button[contains(text(), 'Log In')]",
                "//button[contains(text(), 'Sign In')]",
                "//input[@type='submit']",
                "//button[contains(@class, 'login') or contains(@class, 'submit')]",
            ]

            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.XPATH, selector)
                    logger.info(f"Found submit button with selector: {selector}")
                    break
                except:
                    continue

            if not submit_button:
                # Last resort - press Enter key on password field
                logger.warning("Submit button not found, pressing Enter on password field")
                from selenium.webdriver.common.keys import Keys
                password_field.send_keys(Keys.RETURN)
            else:
                submit_button.click()
                logger.info("Login form submitted")

            # Wait for login to complete
            time.sleep(5)
            self.take_screenshot('04_logged_in')
            logger.info("Login successful")

        except Exception as e:
            logger.error(f"Error during login: {e}")
            self.take_screenshot('error_login_popup')
            raise

    def select_date(self):
        """Select the booking date (6 days from today) on the calendar"""
        logger.info(f"Selecting date: {self.booking_date.strftime('%Y-%m-%d')}")

        try:
            # Bootstrap datepicker structure: #date > div > div[1] > table > tbody
            target_day = self.booking_date.day
            target_month = self.booking_date.strftime('%B %Y')  # e.g., "March 2026"

            logger.info(f"Looking for day {target_day} in calendar")

            # Wait for calendar to be visible
            time.sleep(2)

            # Check current month displayed in calendar
            current_month_elem = self.driver.find_element(
                By.XPATH, "//*[@id='date']/div/div[1]/table/thead/tr[1]/th[2]"
            )
            current_month_displayed = current_month_elem.text
            logger.info(f"Current month displayed: {current_month_displayed}")

            # Navigate to correct month if needed (click next arrow)
            while target_month not in current_month_displayed:
                next_button = self.driver.find_element(
                    By.XPATH, "//*[@id='date']/div/div[1]/table/thead/tr[1]/th[3]"  # Next arrow
                )
                next_button.click()
                time.sleep(1)
                current_month_elem = self.driver.find_element(
                    By.XPATH, "//*[@id='date']/div/div[1]/table/thead/tr[1]/th[2]"
                )
                current_month_displayed = current_month_elem.text
                logger.info(f"Navigated to: {current_month_displayed}")

            # Find the day cell - try multiple selectors
            # Note: "active" class = today, NOT our target date
            # We want "day" class (excluding "old" and "disabled")
            selectors = [
                # Best: day class, not old, not disabled
                f"//*[@id='date']//td[contains(@class, 'day') and not(contains(@class, 'old')) and not(contains(@class, 'disabled')) and text()='{target_day}']",
                # Next month dates have "new" class
                f"//*[@id='date']//td[contains(@class, 'new') and contains(@class, 'day') and text()='{target_day}']",
                # Fallback: any day cell with matching text
                f"//*[@id='date']//td[contains(@class, 'day') and text()='{target_day}']",
            ]

            day_cell = None
            for selector in selectors:
                try:
                    day_cell = self.driver.find_element(By.XPATH, selector)
                    logger.info(f"Found day {target_day} with selector: {selector}")
                    break
                except:
                    continue

            if not day_cell:
                raise Exception(f"Could not find day {target_day} in calendar with any selector")

            # Click using JavaScript for reliability
            logger.info(f"Clicking day {target_day}...")
            self.driver.execute_script("arguments[0].click();", day_cell)
            time.sleep(2)

            self.take_screenshot('02_date_selected')
            logger.info("Date selection complete")

        except Exception as e:
            logger.error(f"Error selecting date: {e}")
            self.take_screenshot('error_date_selection')
            raise

    def select_first_available_time(self):
        """Select the first available tee time on the page"""
        logger.info("Looking for first available tee time...")

        try:
            # Wait longer for tee times to load after date change
            logger.info("Waiting for tee times to load...")
            time.sleep(5)

            # Look for the first tee time card/slot displayed on the page
            # These are the large cards on the right side with time, players, price
            selectors = [
                "//div[contains(@class, 'booking-start-time-label')]",  # Time label in card
                "//div[contains(@class, 'teesheet')]//div[contains(@class, 'time')]",
                "//div[@data-time]",
                "//a[contains(@class, 'book') or contains(@href, 'book')]",
            ]

            first_time = None
            for selector in selectors:
                try:
                    logger.info(f"Trying selector: {selector}")
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements and len(elements) > 0:
                        first_time = elements[0]
                        logger.info(f"Found {len(elements)} tee time(s) with selector: {selector}")
                        break
                except Exception as e:
                    logger.debug(f"Selector failed: {e}")
                    continue

            if not first_time:
                # Last resort - look for ANY clickable element with time pattern
                logger.info("Trying to find any element with time text...")
                all_divs = self.driver.find_elements(By.XPATH, "//div")
                for div in all_divs[:50]:  # Check first 50 divs
                    text = div.text.strip()
                    if text and ('am' in text.lower() or 'pm' in text.lower()):
                        first_time = div
                        logger.info(f"Found time element by text pattern: {text}")
                        break

            if not first_time:
                raise Exception("No tee times found on page!")

            time_text = first_time.text
            logger.info(f"Found first tee time: {time_text}")

            # Scroll into view and click
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_time)
            time.sleep(1)

            # Click to open booking popup
            self.driver.execute_script("arguments[0].click();", first_time)
            logger.info("Clicked first tee time - popup should appear")
            time.sleep(3)

            self.take_screenshot('03_tee_time_clicked')

        except Exception as e:
            logger.error(f"Error selecting tee time: {e}")
            self.take_screenshot('error_time_selection')
            raise

    def select_holes_and_players(self):
        """Select 18 holes and 4 players in the booking popup"""
        logger.info("Configuring 18 holes and 4 players...")

        try:
            # Select 18 holes using the provided XPath
            holes_xpath = "//*[@id='content']/div/section/div[1]/div[2]/div[4]/div[1]/div/label/div"
            logger.info("Clicking 18 holes option...")
            holes_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, holes_xpath))
            )
            holes_button.click()
            logger.info("Selected 18 holes")
            time.sleep(1)

            # Select 4 players using the provided XPath
            players_xpath = "//*[@id='content']/div/section/div[1]/div[2]/div[4]/div[2]/div/label[3]/div"
            logger.info("Clicking 4 players option...")
            players_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, players_xpath))
            )
            players_button.click()
            logger.info("Selected 4 players")
            time.sleep(2)

            self.take_screenshot('05_holes_and_players_selected')

        except Exception as e:
            logger.error(f"Error selecting holes and players: {e}")
            self.take_screenshot('error_holes_players')
            raise

    def complete_booking(self):
        """Click the Book time button"""
        logger.info("Clicking Book time button...")

        try:
            # Use the provided XPath for Book time button
            book_button_xpath = "//*[@id='content']/div/section/div[2]/section/button"

            book_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, book_button_xpath))
            )

            logger.info(f"Found 'Book time' button")
            book_button.click()
            logger.info("Clicked Book time button")
            time.sleep(5)

            self.take_screenshot('06_booking_complete')
            logger.info("Booking process completed successfully!")

        except Exception as e:
            logger.error(f"Error clicking Book time button: {e}")
            self.take_screenshot('error_booking_completion')
            raise

    def run(self):
        """Execute the full booking process"""
        try:
            logger.info("="*50)
            logger.info("Starting Golf Tee Time Booking Bot")
            logger.info("="*50)

            self.calculate_booking_date()
            self.setup_driver()

            self.navigate_to_booking_page()
            self.select_date()  # Select date (1 week from today)
            self.select_first_available_time()  # Click first tee time (opens popup)
            self.login_in_popup()  # Login in the popup
            self.select_holes_and_players()  # Select 18 holes and 4 players
            self.complete_booking()  # Click "Book time"

            logger.info("="*50)
            logger.info("BOOKING COMPLETED SUCCESSFULLY!")
            logger.info("="*50)
            return True

        except Exception as e:
            logger.error(f"Booking failed: {e}")
            return False

        finally:
            if self.driver:
                logger.info("Closing browser...")
                time.sleep(2)
                self.driver.quit()


def main():
    """Main entry point"""
    bot = GolfBookingBot()
    success = bot.run()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
