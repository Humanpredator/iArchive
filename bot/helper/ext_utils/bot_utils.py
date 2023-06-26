import os
import re

from bot import LOGGER

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"


def fcount(dir):
    APP_FOLDER = dir
    totalFiles = 0
    totalDir = 0
    for base, dirs, files in os.walk(APP_FOLDER):
        for _ in dirs:
            totalDir += 1
        for _ in files:
            totalFiles += 1
    LOGGER.info(f"Total Files: {totalFiles}")
    return totalFiles


def fsize(dir):
    size = 0
    folderpath = dir
    for ele in os.scandir(folderpath):
        size += os.stat(ele).st_size
    return size


def get_readable_time(seconds: int) -> str:
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m"
    seconds = int(seconds)
    result += f"{seconds}s"
    return result


def progress_bar(count, size):
    percent = 100
    bar_length = 20
    pbar = "\r[{:20s}] {:2.1f}%".format("#" * int(count / size * bar_length),
                                        count / size * percent)
    return pbar


def allow_access(profile):
    is_followed = profile.followed_by_viewer
    pt_acc = profile.is_private
    if pt_acc and not is_followed:
        return False
    if pt_acc and is_followed:
        return True
    if not pt_acc:
        return True
    return False


def extract_story_info(url):
    pattern = r"https?://(?:www\.)?instagram\.com/stories/([a-zA-Z0-9._]+)/(\d+)/?"
    match = re.match(pattern, url)
    url_json = {}
    if not match:
        return None
    url_json["content_type"] = "STORY"
    url_json["username"] = match.group(1)
    url_json["shortcode"] = match.group(2)
    return url_json


def extract_content_info(url):
    pattern = r"https?://(?:www\.)?instagram\.com/([a-zA-Z0-9._]+/)?(p|tv|reel)/([A-Za-z0-9_\-]+)/?"
    match = re.match(pattern, url)
    url_json = {}
    post_type = {"p": "POST", "tv": "IGTV", "reel": "REEL"}
    if not match:
        return None
    url_json["content_type"] = post_type.get(match.group(2))
    url_json["username"] = None
    url_json["shortcode"] = match.group(3)
    return url_json


def check_instagram_url(url):
    pattern = r"https?://(?:www\.)?instagram\.com/(?:[a-zA-Z0-9._]+)/?"
    match = re.match(pattern, url)
    if not match:
        return None
    if "/stories/highlights/" in url:
        return None
    if "/stories/" in url:
        url_json = extract_story_info(url)
        return url_json
    if "/p/" in url:
        url_json = extract_content_info(url)
        return url_json
    if "/tv/" in url:
        url_json = extract_content_info(url)
        return url_json
    if "/reel/" in url:
        url_json = extract_content_info(url)
        return url_json


def is_link(args):
    iglink = (
        r"^https://www\.instagram\.com/([A-Za-z0-9._]+/)?(p|tv|reel)/([A-Za-z0-9\-_]*)"
    )
    return bool(re.search(iglink, args))
