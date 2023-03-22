"""Main Bot File"""
import os
import shutil
import signal
import time
from sys import executable

# noinspection PyUnresolvedReferences
import modules
import psutil
from pyrogram import idle
from telegram import ParseMode, TelegramError
from telegram.ext import CommandHandler

from bot import (
    AUTHORIZED_CHATS,
    IGNORE_PENDING_REQUESTS,
    INSTA,
    OWNER_ID,
    STATUS,
    app,
    botStartTime,
    dispatcher,
    updater,
    LOGGER
)
from bot.helper.ext_utils import fs_utils
from bot.helper.ext_utils.bot_utils import (
    get_readable_file_size,
    get_readable_time,
    usercheck,
)
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import *


def stats_(update, context):
    current_time = get_readable_time(time.time() - botStartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = (
        f"<b>Bot Uptime:</b> <code>{currentTime}</code>\n"
        f"<b>Total Disk Space:</b> <code>{total}</code>\n"
        f"<b>Used:</b> <code>{used}</code> "
        f"<b>Free:</b> <code>{free}</code>\n\n"
        f"<b>Upload:</b> <code>{sent}</code>\n"
        f"<b>Download:</b> <code>{recv}</code>\n\n"
        f"<b>CPU:</b> <code>{cpuUsage}%</code> "
        f"<b>RAM:</b> <code>{memory}%</code> "
        f"<b>DISK:</b> <code>{disk}%</code>"
    )
    sendMessage(stats, context.bot, update)


def restart(update, context):
    """Restart the bot"""
    restart_message = sendMessage(
        "Restarting Bot, Please wait!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    with open(".restartmsg", "w", encoding="UTF-8") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    os.execl(executable, executable, "-m", "bot")


def ping(update, context):
    """Ping the bot"""
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f"{end_time - start_time} ms", reply)


def log(update, context):
    """Send the log file"""
    sendLogFile(context.bot, update)


def main():
    """Start the bot"""
    fs_utils.start_cleanup()
    try:
        USER = usercheck()
        os.path.exists(f"./{USER}")
        INSTA.load_session_from_file(USER, filename=f"./{USER}")
        STATUS.add(1)
        LOGGER.info(f"{USER} - Session file loaded")
    except FileNotFoundError:
        LOGGER.info("Session file not Found")
    # Check if the bot is restarting
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg", encoding="UTF-8") as file_:
            chat_id, msg_id = map(int, file_)
        bot.edit_message_text("Restarted successfully!", chat_id, msg_id)
        os.remove(".restart-msg")
    elif OWNER_ID:
        try:
            text = "<b>Bot Restarted!</b>"
            bot.sendMessage(chat_id=OWNER_ID, text=text,
                            parse_mode=ParseMode.HTML)
            if AUTHORIZED_CHATS:
                for i in AUTHORIZED_CHATS:
                    bot.sendMessage(chat_id=i, text=text,
                                    parse_mode=ParseMode.HTML)
        except Exception as error:
            LOGGER.warning(error)

    ping_handler = CommandHandler(
        BotCommands.PingCommand,
        ping,
        filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
        run_async=True,
    )
    restart_handler = CommandHandler(
        BotCommands.RestartCommand,
        restart,
        filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
        run_async=True,
    )
    stats_handler = CommandHandler(
        BotCommands.StatsCommand,
        stats,
        filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
        run_async=True,
    )
    log_handler = CommandHandler(
        BotCommands.LogCommand,
        log,
        filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
        run_async=True,
    )
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


app.start()
main()
idle()
