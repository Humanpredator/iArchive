import logging
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

        for _ in dirs:
            totalDir += 1
        for _ in files:
            totalFiles += 1
    LOGGER.info(f'Total Files: {totalFiles}')
    return totalFiles


def fsize(dir):
    size = 0
    folderpath = dir
    for ele in os.scandir(folderpath):
        size += os.stat(ele).st_size
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


def progress_bar(count, size):
    percent = 100
    bar_length = 20
    pbar = ("\r[{:20s}] {:2.1f}%".format(
        '#' * int(count / size * bar_length), count / size * percent))
    return pbar


def usersave(username):
    file = open("username.txt", "w")
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
    if val:
        return "🔒Private🔒"
    return "🔓Public🔓"


def yes_or_no(val):
    if val:
        return "Yes"
    return "No"


def is_link(args):
    iglink = r'^https://www\.instagram\.com/([A-Za-z0-9._]+/)?(p|tv|reel)/([A-Za-z0-9\-_]*)'
    return bool(re.search(iglink, args))


