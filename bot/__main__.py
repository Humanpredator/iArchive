"""Main Bot File"""
import os
import shutil
import signal
import time
from sys import executable

import psutil
from telegram import ParseMode
from telegram.ext import CommandHandler

# noinspection PyUnresolvedReferences
from bot import (
    AUTHORIZED_CHATS,
    IG_USERNAME,
    IGNORE_PENDING_REQUESTS,
    INSTA,
    LOGGER,
    OWNER_ID,
    STATUS,
    app,
    bot,
    botStartTime,
    dispatcher,
    get_config,
    helper,
    modules,
)
from bot.helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from bot.helper.ext_utils.fs_utils import exit_clean_up, start_cleanup
from bot.helper.tg_utils.bot_commands import BotCommands
from bot.helper.tg_utils.filters import CustomFilters
from bot.helper.tg_utils.message_utils import editMessage, sendLogFile, sendMessage


def stats(update, context):
    current_time = get_readable_time(time.time() - botStartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats_msg = (f"<b>Bot Uptime:</b> <code>{current_time}</code>\n"
                 f"<b>Total Disk Space:</b> <code>{total}</code>\n"
                 f"<b>Used:</b> <code>{used}</code> "
                 f"<b>Free:</b> <code>{free}</code>\n\n"
                 f"<b>Upload:</b> <code>{sent}</code>\n"
                 f"<b>Download:</b> <code>{recv}</code>\n\n"
                 f"<b>RAM:</b> <code>{memory}%</code> "
                 f"<b>DISK:</b> <code>{disk}%</code> ")
    sendMessage(stats_msg, context.bot, update)


def restart(update, context):
    """Restart the bot"""
    restart_message = sendMessage("Restarting Bot, Please wait!", context.bot,
                                  update)
    # Save restart message object in order to reply to it after restarting
    with open(".restart-msg", "w", encoding="UTF-8") as f:
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


def errorhandler(update, context):
    """Log Errors caused by Updates."""
    LOGGER.warning('Caused Error: "%s"', context.error)

    error_message = str(context.error)

    sendMessage(f"Error Occurred: {error_message}", context.bot, update)


def main():
    """Start the bot"""
    start_cleanup()
    if not os.path.exists(f"./sessionfile"):
        LOGGER.info(f"No Session File Loaded...!")
    else:
        INSTA.load_session_from_file(IG_USERNAME, filename=f"./sessionfile")
        STATUS.add(1)
        LOGGER.info(f"{IG_USERNAME} - Session File Loaded")
    if os.path.isfile(".restart-msg"):
        with open(".restart-msg", encoding="UTF-8") as file_:
            chat_id, msg_id = map(int, file_)
        bot.edit_message_text("Restarted successfully!", chat_id, msg_id)
        os.remove(".restart-msg")
    elif OWNER_ID:
        try:
            text = "<b>Services are Online...!</b>"
            bot.sendMessage(chat_id=OWNER_ID,
                            text=text,
                            parse_mode=ParseMode.HTML)
            if AUTHORIZED_CHATS:
                for i in AUTHORIZED_CHATS:
                    bot.sendMessage(chat_id=i,
                                    text=text,
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
    dispatcher.add_error_handler(errorhandler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    signal.signal(signal.SIGINT, exit_clean_up)
    app.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("Bot Started Successfully.")
    app.idle()


if __name__ == "__main__":
    main()
