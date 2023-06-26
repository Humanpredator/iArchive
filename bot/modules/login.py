""" Login Module for the userbot. //Simple Module for logging into Instagram"""
import os

from instaloader import (
    BadCredentialsException,
    InstaloaderException,
    Profile,
    TwoFactorAuthRequiredException,
)
from telegram import ParseMode
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler

from bot import INSTA, STATUS, bot, dispatcher
from bot.helper.ext_utils.bot_utils import (
    is_link,
)
from bot.helper.tg_utils.bot_commands import BotCommands
from bot.helper.tg_utils.filters import CustomFilters
from bot.helper.tg_utils.message_utils import (
    deleteMessage,
    editMessage,
    sendMessage,
)

CODE_SAVE = range(2)


def user_login(update, context):
    """For the /login command, logs the user in and starts the conversation."""
    current_user = INSTA.context.username
    args = update.message.text.split(" ", maxsplit=2)
    if len(args) > 2:
        username = args[1]
        password = args[2]
        deleteMessage(context.bot, update.message)
        msg = sendMessage(
            f"Checking given user @{username} and password.\nPlease Wait...!",
            context.bot,
            update,
        )
        if 1 in STATUS:
            editMessage(
                f"@{current_user} is already logged in.\nTry to /logout.", msg)
        elif is_link(args[1]):
            editMessage("Don't use links...!", msg)
        else:
            try:
                INSTA.login(username, password)
                INSTA.save_session_to_file(filename="./sessionfile")
                STATUS.add(1)
                editMessage(
                    f"Fetching the details of @{username}\n Please wait...!", msg
                )
                profile = Profile.from_username(INSTA.context, INSTA.context.username)
                media_count = profile.mediacount
                name = profile.full_name
                bio = profile.biography
                ppic = profile.profile_pic_url
                igtv_count = profile.igtvcount
                followers = profile.followers
                following = profile.followees
                deleteMessage(context.bot, msg)
                bot.send_photo(
                    chat_id=update.message.chat.id,
                    caption=f"<b>Your Account Details</b>\n\n\
                    🏷 <b>Name</b>: {name}\n\
                    🔖 <b>Username</b>: {profile.username}\n\
                    📝 <b>Bio</b>: {bio}\n\
                    📍 <b>Account Type</b>: {profile.is_private}\n\
                    🏭 <b>Is Business Account?</b>: {profile.is_business_account}\n\
                    👥 <b>Total Followers</b>: {followers}\n\
                    👥 <b>Total Following</b>: {following}\n\
                    📸 <b>Total Posts</b>: {media_count}\n\
                    📺 <b>IGTV Videos</b>: {igtv_count}",
                    parse_mode=ParseMode.HTML,
                    photo=ppic,
                )
                return

            except BadCredentialsException:
                editMessage("Wrong credentials\nTry to /login again.", msg)
                return

            except TwoFactorAuthRequiredException:
                editMessage("Send your 2F code within 30sec...!", msg)
                return CODE_SAVE

            except InstaloaderException as error:
                editMessage(f"{error}\nTry to /login again.", msg)
                return
    else:
        if 1 in STATUS:
            sendMessage(
                f"@{current_user} is already logged in.\nTry to /logout.",
                context.bot,
                update,
            )
            return
        sendMessage("Send /login <b>username</b> <b>password</b>",
                    context.bot, update)
        return


def timeout(update):
    """Logs out the user and ends the conversation from timeout."""
    update.message.reply_text("Oh! TimeOut.\nTry to /login again.")
    return ConversationHandler.END


def codei_(update, context):
    """Checks the 2F code and logs the user in."""
    code = update.message.text
    if code.isdigit():
        code = int(code)
        msg = sendMessage(
            "Checking given code.\n please wait...!", context.bot, update)
        try:
            INSTA.two_factor_login(code)
            INSTA.save_session_to_file(filename="./sessionfile")
            STATUS.add(1)
            editMessage("Fetching details from Instagram..!", msg)
            profile = Profile.from_username(INSTA.context, INSTA.context.username)
            media_count = profile.mediacount
            name = profile.full_name
            bio = profile.biography
            ppic = profile.profile_pic_url
            igtv_count = profile.igtvcount
            followers = profile.followers
            following = profile.followees
            deleteMessage(context.bot, msg)
            bot.send_photo(
                chat_id=update.message.chat.id,
                caption=f"<b>Your Account Details</b>\n\n\
                               🏷 <b>Name</b>: {name}\n\
                               🔖 <b>Username</b>: {profile.username}\n\
                               📝 <b>Bio</b>: {bio}\n\
                               📍 <b>Account Type</b>: {profile.is_private}\n\
                               🏭 <b>Is Business Account?</b>: {profile.is_business_account}\n\
                               👥 <b>Total Followers</b>: {followers}\n\
                               👥 <b>Total Following</b>: {following}\n\
                               📸 <b>Total Posts</b>: {media_count}\n\
                               📺 <b>IGTV Videos</b>: {igtv_count}",
                parse_mode=ParseMode.HTML,
                photo=ppic,
            )
        except BadCredentialsException:
            editMessage("Wrong credentials\n Try to /login again.", msg)
        except InstaloaderException as error:
            editMessage(f"{error}\nTry to /login again.", msg)
    else:
        sendMessage("Please enter a valid code.", context.bot, update)
    return ConversationHandler.END


def logout(update, context):
    """Logs out the user and ends the conversation."""
    if 1 in STATUS:
        sendMessage("You're successfully logged out.", context.bot, update)
        STATUS.remove(1)
        os.remove(f"./sessionfile")
    else:
        sendMessage("You're not logged in.\n Try to /login.",
                    context.bot, update)


logout_handler = CommandHandler(
    BotCommands.IgLogoutCommand,
    logout,
    filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
)

userlogin_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            BotCommands.LoginCommand,
            user_login,
            filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
        )
    ],
    states={
        CODE_SAVE: [MessageHandler(Filters.text, codei_)],
        ConversationHandler.TIMEOUT: [
            MessageHandler(Filters.text | Filters.command, timeout)
        ],
    },
    fallbacks=[],
    conversation_timeout=30,
)

dispatcher.add_handler(logout_handler)

dispatcher.add_handler(userlogin_handler)
