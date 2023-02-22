'''A module to download content from Instagram'''

import subprocess
import threading
import time
from datetime import datetime

import pytz
from telegram import TelegramError

from bot import DOWNLOAD_STATUS_UPDATE_INTERVAL, LOGGER, TG_UPLOAD,bot

from bot.helper.ext_utils.bot_utils import usercheck
from bot.helper.ext_utils.fs_utils import clean_download, subfolder

from bot.helper.upload_utilis.gdrive import gup
from bot.helper.upload_utilis.tg_upload import tgup

IST = pytz.timezone("Asia/Kolkata")


# A function to download content from Instagram
def download_insta(command, msg, directory, username, chat_id, fetch):
    '''A function to download content from Instagram'''
    def download(command, msg, directory, fetch):
        current_user = usercheck()
        session = f"./{current_user}"
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
        )
        while True:
            output = process.stdout.readline()
            if output == b"":
                subfolder(directory)
                gup(directory, msg, username, fetch)
                break
            if output:
                datetime_ist = datetime.now(IST)
                ist_time = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                try:
                    msg = f'CURRENT_STATUS ⚙️: <code>{format(output.decode("UTF8"))}</code>\n\
                    <b>Last Updated</b> : <code>{ist_time}</code>\n\
                    <b>directoryectory</b> : <code>{directory}</code>\n\
                    <b>session</b> : <code>{session}</code>\n\
                    <b>Type</b> : <code>{fetch}</code>'
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    bot.edit_message_text(
                        msg, msg.chat.id, msg.message_id, parse_mode="HTML"
                    )
                    LOGGER.info(output.decode('UTF8'))
                except TelegramError as error:
                    LOGGER.info(error)
        while True:
            error = process.stderr.readline()
            if error == b"":
                break
            if error:
                datetime_ist = datetime.now(IST)
                ist_time = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                try:
                    ermsg = f"ERROR❌:<code>{error.decode('UTF8')}</code>\n\
                            Last Updated : <code>{ist_time}</code>"
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    bot.edit_message_text(
                        ermsg, msg.chat.id, msg.message_id, parse_mode="HTML"
                    )
                    LOGGER.info(error.decode('UTF8'))
                except TelegramError as error:
                    LOGGER.info(error)
                return True
        LOGGER.info("Download Completed-%s",directory)
        if TG_UPLOAD:
            tgup(chat_id, directory)
        else:
            pass
        clean_download(directory)

    threading.Thread(target=download, args=(command, msg, directory, fetch)).start()
    return True
