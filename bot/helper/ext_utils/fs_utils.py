import sys
import shutil
import os
from bot import LOGGER,OWNER_ID
import shutil
from pathlib import Path

from bot.helper.ext_utils.bot_utils import usercheck

#function to remove sub dir
def rmv(subdir):
      dir = Path(subdir).is_dir()
      if dir == True:
            shutil.rmtree(subdir)
            print("sub folder successfully removed")
      else:
            print("Path doesn't exists....Skiped!")
            pass



username=usercheck()

dir=f"{OWNER_ID}/{username}"
def clean_download(path: str):
    if os.path.exists(path):
        LOGGER.info(f"Cleaning Download: {path}")
        shutil.rmtree(path)

def start_cleanup():
    try:
        shutil.rmtree(dir)
    except FileNotFoundError:
        pass

def clean_all():
    try:
        shutil.rmtree(dir)
    except FileNotFoundError:
        pass

def exit_clean_up(signal, frame):
    try:
        LOGGER.info("Please wait, while we clean up the downloads and stop running downloads")
        clean_all()
        os.remove('username.txt')
        sys.exit(0)
    except KeyboardInterrupt:
        LOGGER.warning("Force Exiting before the cleanup finishes!")
        sys.exit(1)

