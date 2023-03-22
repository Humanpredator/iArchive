from telegram import InlineKeyboardMarkup
from telegram.message import Message
from telegram.update import Update

from bot import LOGGER, bot


def sendMessage(text: str, bot, update: Update):
    try:
        return bot.send_message(
            update.message.chat_id,
            reply_to_message_id=update.message.message_id,
            text=text,
            allow_sending_without_reply=True,
            parse_mode="HTMl",
        )
    except Exception as e:
        LOGGER.error(str(e))


def sendMarkup(text: str, bot, update: Update, reply_markup: InlineKeyboardMarkup):
    return bot.send_message(
        update.message.chat_id,
        reply_to_message_id=update.message.message_id,
        text=text,
        reply_markup=reply_markup,
        allow_sending_without_reply=True,
        parse_mode="HTMl",
    )


def editMessage(text: str, message: Message, reply_markup=None):
    try:
        bot.edit_message_text(
            text=text,
            message_id=message.message_id,
            chat_id=message.chat.id,
            reply_markup=reply_markup,
            parse_mode="HTMl",
        )
    except Exception as e:
        LOGGER.error(str(e))


def deleteMessage(bot, message: Message):
    try:
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)
    except Exception as e:
        LOGGER.error(str(e))


def sendLogFile(bot, update: Update):
    with open("logs.log", "rb") as f:
        bot.send_document(
            document=f,
            filename=f.name,
            reply_to_message_id=update.message.message_id,
            chat_id=update.message.chat_id,
        )
