import sys
import time

import schedule
import threading

import guardian
import listener
import config
import storage

from logger import logger

# TODO: add stuff
# TODO: add checking permission to execute command in Firewall


def main():
    guardian.unbanService()

    thread = threading.Thread(target=listener.start, name="lip-core")
    thread.start()

    # schedulers
    schedule.every(config.UNBAN_USERS_INTERVAL).seconds.do(guardian.unbanService)
    schedule.every(config.CHECK_INACTIVE_USERS_INTERVAL).seconds.do(storage.cleanService)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # TODO
        logger.info('Stopping...')
        sys.exit(130)