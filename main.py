import os
import time
from loguru import logger

from dotenv import load_dotenv

from src.sale_detector import get_current_dapps, retrieve_dapps, save_dapps
from src.telegram_handler import send_irritative_notification_to_all_users, handle_telegram_updates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, ".env")))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CHECK_INTERVAL_SECONDS = 25

def main():
    logger.add("logfile.log", rotation="2 MB", level="INFO")

    while True:
        # Handle incoming Telegram messages to register users
        handle_telegram_updates()

        # Check for new sales
        current_dapps = get_current_dapps()
        previous_dapps = retrieve_dapps()
        if current_dapps and previous_dapps:
            new_dapps = current_dapps - previous_dapps
            save_dapps(current_dapps.union(previous_dapps))

            # if new sales appear -> send notification
            if new_dapps:
                new_dapps_str = "  |  ".join(new_dapps)
                notification_message = f"🚨 New Sale Detected on web3.okx.com!  {new_dapps_str}"
                send_irritative_notification_to_all_users(notification_message)

        # Wait before the next check
        logger.info(f"Waiting for {CHECK_INTERVAL_SECONDS} seconds...")
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()