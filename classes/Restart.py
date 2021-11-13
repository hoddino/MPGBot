import sys
import threading
import schedule
import time

import config


class Restart(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        schedule.every().day.at(config.DAILY_RESTART_TIME).do(self.stop)

        while True:
            schedule.run_pending()
            time.sleep(60)

    def stop(self):
        sys.exit()
