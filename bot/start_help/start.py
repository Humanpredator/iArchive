from telegram.ext import CommandHandler
from bot import  dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper import button_build


def start(update, context):
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("Insta-Scrap Repo", "https://github.com/Humanpredator/Insta-Scrap")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(1))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
Thanks to SUBIN for repo.\n
This bot can download all the Instagram Accounts posts..!
Type /{BotCommands.HelpCommand} to get a list of available Instagram commands..!
'''
        sendMarkup(start_string, context.bot, update, reply_markup)
    else:
        sendMarkup(
            'Oops! not a Authorized user.\nPlease deploy your own <b>Insta-Scrap Bot</b>.',
            context.bot,
            update,
            reply_markup,
        )











start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)
dispatcher.add_handler(start_handler)