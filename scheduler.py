"""
Scheduler for automated golf booking bot
Runs at exactly 6:00 AM EST every day
"""
import logging
from datetime import datetime
from pathlib import Path
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import Config
from booking_bot import GolfBookingBot

# Create required directories
Path(Config.LOG_DIR).mkdir(exist_ok=True)
Path(Config.SCREENSHOT_DIR).mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_booking():
    """Execute the booking bot"""
    logger.info("Scheduled booking job triggered!")

    try:
        bot = GolfBookingBot()
        success = bot.run()

        if success:
            logger.info("✓ Booking completed successfully")
        else:
            logger.error("✗ Booking failed - check logs for details")

    except Exception as e:
        logger.error(f"Unexpected error in scheduled job: {e}", exc_info=True)


def main():
    """Main scheduler entry point"""
    logger.info("="*60)
    logger.info("Golf Booking Bot Scheduler Starting")
    logger.info("="*60)

    # Get timezone
    timezone = pytz.timezone(Config.TIMEZONE)
    logger.info(f"Timezone: {Config.TIMEZONE}")

    # Parse booking time
    hour, minute = map(int, Config.BOOKING_TIME.split(':'))
    logger.info(f"Scheduled run time: {hour:02d}:{minute:02d} {Config.TIMEZONE}")

    # Create scheduler
    scheduler = BlockingScheduler(timezone=timezone)

    # Schedule the job for 6:00 AM EST every day
    scheduler.add_job(
        run_booking,
        trigger=CronTrigger(hour=hour, minute=minute, timezone=timezone),
        id='golf_booking',
        name='Golf Tee Time Booking',
        replace_existing=True,
        max_instances=1  # Only one instance at a time
    )

    logger.info("Scheduler configured successfully")
    logger.info(f"Next run time: {scheduler.get_jobs()[0].next_run_time}")
    logger.info("="*60)
    logger.info("Scheduler is now running. Press Ctrl+C to exit.")
    logger.info("="*60)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
