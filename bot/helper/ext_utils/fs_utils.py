import os
import shutil
import sys
from pathlib import Path

from bot import LOGGER, OWNER_ID


def subpath(path):
    subfolder = []
    try:
        for it in os.scandir(path):
            if it.is_dir():
                subfolder.append(it.path)
        return subfolder
    except FileNotFoundError:
        pass


def rmv(subdir):
    dir = Path(subdir).is_dir()
    if dir:
        shutil.rmtree(subdir)
    else:

        pass


def subfolder(DIR):
    try:
        dirlist = subpath(DIR)
        for dir in dirlist:
            files = os.listdir(dir)
            for file in files:
                file_name = os.path.join(dir, file)
                shutil.move(file_name, DIR + '/' + file)
            rmv(dir)
    except FileNotFoundError:
        pass


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


def exit_clean_up(signal, frame):
    try:
        LOGGER.info(
            "Please wait, while we clean up the downloads and stop running downloads")
        clean_all()
        os.remove('username.txt')
        sys.exit(0)
    except KeyboardInterrupt:
        LOGGER.warning("Force Exiting before the cleanup finishes!")
        sys.exit(1)
