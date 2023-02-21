import glob
import time
from datetime import datetime

import pytz
from pyrogram.errors import FloodWait
from telegram import InputMediaPhoto, InputMediaVideo

from bot import DOWNLOAD_STATUS_UPDATE_INTERVAL, LOGGER
from bot.helper.ext_utils.bot_utils import progress_bar, usercheck
from bot.helper.telegram_helper.message_utils import *

USER = usercheck()
IST = pytz.timezone('Asia/Kolkata')
session = f"./{USER}"


# A functionUpload Content to Telegram


def tgup(chat_id, dir):
    datetime_ist = datetime.now(IST)
    ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
    m = bot.send_message(chat_id, "Uploading to Telegram, Please wait...")
    videos = glob.glob(f"{dir}/*.mp4")
    VDO = []
    GIF = []
    for video in videos:
        try:
            VDO.append(video)
        except Exception as e:
            GIF.append(video)
            LOGGER.error(e)
    PIC = glob.glob(f"{dir}/*.jpg")

    totalpics = len(PIC)
    totalgif = len(GIF)
    totalvideo = len(VDO)
    TOTAL = totalpics + totalvideo + totalgif
    total = TOTAL

    up = 0
    rm = TOTAL
    if total == 0:
        return
    if totalpics > 0:
        for i in range(0, len(PIC), 10):
            chunk = PIC[i:i + 10]
            media = []
            for photo in chunk:
                media.append(InputMediaPhoto(open(photo, 'rb')))
                up += 1
                rm -= 1
            try:

                time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                bot.send_media_group(chat_id=chat_id, media=media)
            except FloodWait as e:
                time.sleep(e.x)
                bot.send_media_group(chat_id=chat_id, media=media)
            except Exception as e:
                LOGGER.error(e)
            msg = f'''
<b>Uploading: </b><code>{progress_bar(up, total)}</code>
<b>Files uploaded: </b><code>0{up}/{total}</code>
<b>Files remaining: </b><code>0{rm}/{total}</code>
<b>Total Files : </b><code>{total}</code>
<b>Last Updated : </b><code>{ISTIME}</code>
<b>Currently Uploading: </b><code>Pictures</code>
'''
            editMessage(msg, m)

    if totalvideo > 0:
        for i in range(0, len(VDO), 10):
            chunk = VDO[i:i + 10]

            media = []
            for video in chunk:
                media.append(InputMediaVideo(media=open(video, 'rb')))
                up += 1
                rm -= 1
            try:
                time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                bot.send_media_group(chat_id=chat_id, media=media)
            except FloodWait as e:
                time.sleep(e.x)
                bot.send_media_group(chat_id=chat_id, media=media)
                rm -= 1
            except Exception as e:
                LOGGER.error(e)
            msg = f'''
<b>Uploading: </b><code>{progress_bar(up, total)}</code>
<b>Files uploaded: </b><code>0{up}/{total}</code>
<b>Files remaining: </b><code>0{rm}/{total}</code>
<b>Total Files : </b><code>{total}</code>
<b>Last Updated : </b><code>{ISTIME}</code>
<b>Currently Uploading: </b><code>Videos</code>
'''
            editMessage(msg, m)

    if totalgif > 0:
        for gif in GIF:
            try:
                datetime_ist = datetime.now(IST)
                ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                up += 1
                time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                bot.send_animation(chat_id=chat_id, animation=open(gif, 'rb'))
                rm -= 1
                msg = f'''
<b>Uploading: </b><code>{progress_bar(up, total)}</code>
<b>Files uploaded: </b><code>0{up}/{total}</code>
<b>Files remaining: </b><code>0{rm}/{total}</code>
<b>Total Files : </b><code>{total}</code>
<b>Last Updated : </b><code>{ISTIME}</code>
<b>Currently Uploading: </b><code>GIFS</code>
'''
                editMessage(msg, m)
            except FloodWait as e:
                up += 1
                time.sleep(e.x)
                bot.send_animation(chat_id=chat_id, animation=open(gif, 'rb'))
                rm -= 1
                msg = f'''
<b>Uploading: </b><code>{progress_bar(up, total)}</code>
<b>Files uploaded: </b><code>0{up}/{total}</code>
<b>Files remaining: </b><code>0{rm}/{total}</code>
<b>Total Files : </b><code>{total}</code>
<b>Last Updated : </b><code>{ISTIME}</code>
<b>Currently Uploading: </b><code>GIFS</code>
'''
                editMessage(msg, m)
            except Exception as e:
                LOGGER.error(e)

    editMessage("Telegram Upload Completed", m)
    LOGGER.info("Telegram Upload Completed")
    return True
