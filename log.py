import config
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def info(message):
    print(datetime.now().strftime(DATE_FORMAT), config.PREFIX_INFO, message)


def warn(message):
    print(datetime.now().strftime(DATE_FORMAT), config.PREFIX_WARNING, message)


def error(message):
    print(datetime.now().strftime(DATE_FORMAT), config.PREFIX_ERROR, message)
