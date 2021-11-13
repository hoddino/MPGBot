import sys
import threading
import schedule


class Restart(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        schedule.every().minute.do(sys.exit(0))
