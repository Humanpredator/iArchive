import glob
import time
from datetime import datetime

from telegram import InputMediaPhoto, InputMediaVideo

from bot import LOGGER, DOWNLOAD_STATUS_UPDATE_INTERVAL
from bot.helper.ext_utils.bot_utils import progress_bar
from bot.helper.tg_utils.message_utils import editMessage, sendMediaGroup


def tgup(msg, directory):
    editMessage("Telegram Upload Started", msg)
    media_groups = []
    total = 0

    def update_progress(up, rm, currently_uploading):
        progress = progress_bar(up, total)
        files_uploaded = f"{up:02d}/{total:02d}"
        files_remaining = f"{rm:02d}/{total:02d}"
        pmsg = f"""
<b>Uploading: </b><code>{progress}</code>
<b>Files uploaded: </b><code>{files_uploaded}</code>
<b>Files remaining: </b><code>{files_remaining}</code>
<b>Total Files: </b><code>{total}</code>
<b>Last Updated: </b><code>{datetime.now()}</code>
<b>Currently Uploading: </b><code>{currently_uploading}</code>
"""
        editMessage(pmsg, msg)

    def upload_media(media, currently_uploading):
        nonlocal total
        total += len(media)
        up = 0
        rm = total
        for i in range(0, len(media), 10):
            chunk = media[i:i + 10]
            media_list = []
            for item in chunk:
                media_list.append(item)
                up += 1
                rm -= 1
            try:
                time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                sendMediaGroup(msg, media=media_list)
            except Exception as e:
                LOGGER.error(e)
                sendMediaGroup(msg, media=media_list)
            update_progress(up, rm, currently_uploading)

    videos = glob.glob(f"{directory}/*.mp4")
    images = glob.glob(f"{directory}/*.jpg")

    if images:
        media_groups.append((images, "Pictures"))

    if videos:
        media_groups.append((videos, "Videos"))

    for media, currently_uploading in media_groups:
        if currently_uploading == "Pictures":
            media_list = [InputMediaPhoto(open(photo, "rb")) for photo in media]
            upload_media(media_list, currently_uploading)
        elif currently_uploading == "Videos":
            media_list = [InputMediaVideo(open(video, "rb")) for video in media]
            upload_media(media_list, currently_uploading)

    editMessage("Telegram Upload Completed", msg)
    LOGGER.info("Telegram Upload Completed")
    return True
