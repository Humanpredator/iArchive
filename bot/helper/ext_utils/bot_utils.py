import logging
import threading
import os
import re

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
LOGGER = logging.getLogger(__name__)


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

def fcount(dir):
    APP_FOLDER = dir
    totalFiles = 0
    totalDir = 0
    for base, dirs, files in os.walk(APP_FOLDER):
        print('Searching in : ',base)
        for directories in dirs:
            totalDir += 1
        for Files in files:
            totalFiles += 1
    LOGGER.info(f'Total Files: {totalFiles}')
    return totalFiles

def fsize(dir):
    # assign size
    size = 0
    
    # assign folder path
    Folderpath = dir 
    
    # get size
    for ele in os.scandir(Folderpath):
        size+=os.stat(ele).st_size
        
    return size    

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def usersave(username):
    file = open("username.txt","w")
    if os.path.isfile("username.txt"):
        with open("username.txt") as f:
            file.write(username)
            file.close()

def usercheck():
    if os.path.isfile("username.txt"):
        with open("username.txt") as f:
            username = f.read()
            return username



def acc_type(val):
    if(val):
        return "🔒Private🔒"
    else:
        return "🔓Public🔓"

def yes_or_no(val):
    if(val):
        return "Yes"
    else:
        return "No"

def is_link(args):
    iglink = r'^https://www\.instagram\.com/([A-Za-z0-9._]+/)?(p|tv|reel)/([A-Za-z0-9\-_]*)'
    if re.search(iglink, args):
        return True
    else:  
        return False

def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
