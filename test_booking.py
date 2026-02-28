#!/usr/bin/env python3
"""
Test script for golf booking bot
Runs the bot in non-headless mode for debugging
"""
import os
import sys
from pathlib import Path

# Override headless setting for testing
os.environ['HEADLESS'] = 'False'

from booking_bot import GolfBookingBot

def main():
    """Run test booking"""
    print("="*60)
    print("Golf Booking Bot - Test Mode")
    print("="*60)
    print("This will run the bot with browser visible for debugging.")
    print("")

    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return 1

    print("\nStarting test run...\n")

    bot = GolfBookingBot()
    success = bot.run()

    print("\n" + "="*60)
    if success:
        print("✓ Test completed successfully!")
        print("\nCheck:")
        print(f"  - Logs: {Path('logs').resolve()}")
        print(f"  - Screenshots: {Path('screenshots').resolve()}")
    else:
        print("✗ Test failed - check logs for details")
    print("="*60)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
