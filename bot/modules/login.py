from bot.helper.ext_utils.bot_utils import acc_type, usercheck, usersave, is_link, yes_or_no
import os
from instaloader import Profile, TwoFactorAuthRequiredException, BadCredentialsException
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher, INSTA, STATUS
from bot.helper.telegram_helper.bot_commands import BotCommands
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

insta = INSTA
CODE_SAVE = range(2)


def user_login(update, context):
    USER = usercheck()
    args = update.message.text.split(" ", maxsplit=2)
    if len(args) > 2:
        username = args[1]
        password = args[2]
        deleteMessage(context.bot, update.message)
        m = sendMessage(
            f"Checking given user @{username} and password.\nPlease Wait...!", context.bot, update)
        if 1 in STATUS:
            editMessage(f"@{USER} is already logged in.\nTry to /logout.", m)
        elif is_link(args[1]):
            editMessage("Don't use links...!", m)
        else:
            try:
                insta.login(username, password)
                insta.save_session_to_file(filename=f"./{username}")
                STATUS.add(1)
                usersave(username)
                editMessage(
                    f"Fetching the details of @{username}\n Please wait...!", m)
                profile = Profile.from_username(insta.context, username)
                media_count = profile.mediacount
                name = profile.full_name
                bio = profile.biography
                ppic = profile.profile_pic_url
                igtv_count = profile.igtvcount
                followers = profile.followers
                following = profile.followees
                deleteMessage(context.bot, m)
                bot.send_photo(
                    chat_id=update.message.chat.id,
                    caption=f"You are successfully logged in as {name}\n\n<b>Your Account Details</b>\n\n🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n📸 <b>Total Posts</b>: {media_count}\n📺 <b>IGTV Videos</b>: {igtv_count}", parse_mode="HTML",
                    photo=ppic
                )
                return

            except BadCredentialsException:
                editMessage("Wrong credentials\nTry to /login again.", m)
                pass
                return

            except TwoFactorAuthRequiredException:
                usersave(username)
                editMessage("Send your 2F code within 30sec...!", m)
                return CODE_SAVE

            except Exception as e:
                editMessage(f"{e}\nTry to /login again.", m)
                return
    else:
        if 1 in STATUS:
            sendMessage(
                f"@{USER} is already logged in.\n Try to /logout.\n Use /account to see current logged in user.", context.bot, update)
            return
        else:
            sendMessage(
                f'Send /login <b>username</b> <b>password</b>', context.bot, update)
            return


def timeout(update):
    update.message.reply_text('Oh! TimeOut.\nTry to /login again.')
    return ConversationHandler.END


def codei(update, context):
    username = usercheck()
    codei = update.message.text
    if codei.isdigit():
        codei = int(codei)
        m = sendMessage(
            f"Checking given code.\n please wait...!", context.bot, update)
        try:
            insta.two_factor_login(codei)
            insta.save_session_to_file(filename=f"./{username}")
            STATUS.add(1)
            editMessage("Fetching details from Instagram..!", m)
            profile = Profile.from_username(insta.context, username)
            media_count = profile.mediacount
            name = profile.full_name
            bio = profile.biography
            ppic = profile.profile_pic_url
            igtv_count = profile.igtvcount
            followers = profile.followers
            following = profile.followees
            deleteMessage(context.bot, m)
            bot.send_photo(
                chat_id=update.message.chat.id,
                caption=f"You are successfully in as {name}\n\n<b>Your Account Details</b>\n\n🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n📸 <b>Total Posts</b>: {media_count}\n📺 <b>IGTV Videos</b>: {igtv_count}", parse_mode="HTML",
                photo=ppic
            )
        except BadCredentialsException:
            editMessage("Wrong credentials\n Try to /login again.", m)
            pass
        except Exception as e:
            editMessage(f"{e}\nTry to /login again.", m)
            pass
    else:
        sendMessage("Please enter a valid code.", context.bot, update)
    return ConversationHandler.END


def logout(update, context):
    USER = usercheck()
    if 1 in STATUS:
        sendMessage("You're successfully logged out.", context.bot, update)
        STATUS.remove(1)
        os.remove(f"./{USER}")
        os.remove('username.txt')
    else:
        sendMessage("You're not logged in.\n Try to /login.",
                    context.bot, update)


logout_handler = CommandHandler(BotCommands.IgLogoutCommand, logout,
                                filters=CustomFilters.owner_filter | CustomFilters.sudo_user)

userlogin_handler = ConversationHandler(entry_points=[CommandHandler(BotCommands.LoginCommand, user_login, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)],
                                        states={CODE_SAVE: [MessageHandler(Filters.text, codei)],
                                                ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, timeout)]},
                                        fallbacks=[], conversation_timeout=30)

dispatcher.add_handler(logout_handler)

dispatcher.add_handler(userlogin_handler)
