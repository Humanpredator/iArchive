import os
import shutil
import sys
from datetime import datetime

import pytz

from bot import LOGGER, OWNER_ID


def clean_download(path: str):
    if os.path.exists(path):
        LOGGER.info(f"Cleaning Download: {path}")
        shutil.rmtree(path)


def start_cleanup():
    try:
        dir = f"{OWNER_ID}"
        shutil.rmtree(dir)
    except FileNotFoundError:
        pass


def clean_all():
    try:
        dir = f"{OWNER_ID}"
        shutil.rmtree(dir)
    except FileNotFoundError:
        pass
    return


def exit_clean_up(signal, frame):
    LOGGER.info("Cleaning up stuffs before closing...")
    clean_all()
    sys.exit(0)


def datetime_india():
    datetime_str = datetime.now(
        pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S.%f")
    datetime_obj = datetime.strptime(str(datetime_str), "%Y-%m-%d %H:%M:%S.%f")

    return datetime_str
