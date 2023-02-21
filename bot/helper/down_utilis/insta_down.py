import subprocess
import threading
import time
from datetime import datetime

import pytz

from bot import DOWNLOAD_STATUS_UPDATE_INTERVAL, TG_UPLOAD
from bot.helper.ext_utils.bot_utils import usercheck
from bot.helper.ext_utils.fs_utils import clean_download, subfolder
from bot.helper.telegram_helper.message_utils import *
from bot.helper.upload_utilis.gdrive import gup
from bot.helper.upload_utilis.tg_upload import tgup

IST = pytz.timezone("Asia/Kolkata")


# A function to download content from Instagram
def download_insta(command, m, dir, username, chat_id, fetch):
    def download(command, m, dir, fetch):
        USER = usercheck()
        session = f"./{USER}"
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
        )
        while True:
            output = process.stdout.readline()
            if output == b"":
                subfolder(dir)
                gup(dir, m, username, fetch)
                break
            if output:
                datetime_ist = datetime.now(IST)
                ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                try:
                    msg = f'CURRENT_STATUS ⚙️ : <code>{format(output.decode("UTF8"))}</code>\n<b>Last Updated</b> : <code>{ISTIME}</code>\n<b>Directory</b> : <code>{dir}</code>\n<b>session</b> : <code>{session}</code>\n<b>Type</b> : <code>{fetch}</code>'
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    bot.edit_message_text(
                        msg, m.chat.id, m.message_id, parse_mode="HTML"
                    )
                    LOGGER.info(f"{output.decode('UTF8')}")
                except Exception as e:
                    LOGGER.info(f"{e}")
        while True:
            error = process.stderr.readline()
            if error == b"":
                break
            if error:
                datetime_ist = datetime.now(IST)
                ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                try:
                    ermsg = "ERROR ❌ : <code>{}</code>\nLast Updated : <code>{}</code>".format(
                        error.decode("UTF8"), ISTIME
                    )
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    bot.edit_message_text(
                        ermsg, m.chat.id, m.message_id, parse_mode="HTML"
                    )
                    LOGGER.info(f"{error.decode('UTF8')}")
                except Exception as e:
                    LOGGER.info(f"{e}")
                return True
        LOGGER.info(f"Download Completed-{dir}")
        if TG_UPLOAD:
            tgup(chat_id, dir)
        else:
            pass
        clean_download(dir)

    threading.Thread(target=download, args=(command, m, dir, fetch)).start()
    return True
