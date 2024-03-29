"""Module To Authorize Users To Use The Bot"""
from telegram.ext import CommandHandler

from bot import AUTHORIZED_CHATS, DB_URI, SUDO_USERS, dispatcher
from bot.helper.ext_utils.db_handler import DbManger
from bot.helper.tg_utils.bot_commands import BotCommands
from bot.helper.tg_utils.filters import CustomFilters
from bot.helper.tg_utils.message_utils import sendMessage


def authorize(update, context):
    """Authorize a user to use the bot"""
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(" ")
    if len(message_) == 2:
        user_id = int(message_[1])
        if user_id in AUTHORIZED_CHATS:
            msg = f"User({user_id}) Already Authorized"
        elif DB_URI is not None:
            msg = DbManger().db_auth(user_id)
        else:
            with open("authorized_chats.txt", "a", encoding="UTF-8") as file:
                file.write(f"{user_id}\n")
                AUTHORIZED_CHATS.add(user_id)
                msg = f"User({user_id}) Authorized"
    elif reply_message is None:
        # Trying to authorize a chat
        chat_id = update.effective_chat.id
        if chat_id in AUTHORIZED_CHATS:
            msg = f"Chat({chat_id}) Already Authorized"

        elif DB_URI is not None:
            msg = DbManger().db_auth(chat_id)
        else:
            with open("authorized_chats.txt", "a", encoding="UTF-8") as file:
                file.write(f"{chat_id}\n")
                AUTHORIZED_CHATS.add(chat_id)
                msg = f"Chat({chat_id}) Authorized"
    else:
        # Trying to authorize someone by replying
        user_id = reply_message.from_user.id
        if user_id in AUTHORIZED_CHATS:
            msg = f"User({user_id}) Already Authorized"
        elif DB_URI is not None:
            msg = DbManger().db_auth(user_id)
        else:
            with open("authorized_chats.txt", "a", encoding="UTF-8") as file:
                file.write(f"{user_id}\n")
                AUTHORIZED_CHATS.add(user_id)
                msg = f"User({user_id}) Authorized"
    sendMessage(msg, context.bot, update)


def un_authorize(update, context):
    """Unauthorize a user to use the bot"""
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(" ")
    if len(message_) == 2:
        user_id = int(message_[1])
        if user_id in AUTHORIZED_CHATS:
            if DB_URI is not None:
                msg = DbManger().db_unauth(user_id)
            else:
                AUTHORIZED_CHATS.remove(user_id)
                msg = f"User({user_id}) Unauthorized"
        else:
            msg = f"User({user_id}) Already Unauthorized"
    elif reply_message is None:
        # Trying to unauthorize a chat
        chat_id = update.effective_chat.id
        if chat_id in AUTHORIZED_CHATS:
            if DB_URI is not None:
                msg = DbManger().db_unauth(chat_id)
            else:
                AUTHORIZED_CHATS.remove(chat_id)
                msg = f"Chat({chat_id}) Unauthorized"
        else:
            msg = f"Chat({chat_id}) Already Unauthorized"
    else:
        # Trying to authorize someone by replying
        user_id = reply_message.from_user.id
        if user_id in AUTHORIZED_CHATS:
            if DB_URI is not None:
                msg = DbManger().db_unauth(user_id)
            else:
                AUTHORIZED_CHATS.remove(user_id)
                msg = f"User({user_id}) Unauthorized"
        else:
            msg = f"User({user_id}) Already Unauthorized"
    with open("authorized_chats.txt", "a", encoding="UTF-8") as file:
        file.truncate(0)
        for i in AUTHORIZED_CHATS:
            file.write(f"{i}\n")
    sendMessage(msg, context.bot, update)


def add_sudo(update, context):
    """Promote a user to Sudo"""
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(" ")
    if len(message_) == 2:
        user_id = int(message_[1])
        if user_id in SUDO_USERS:
            msg = f"User({user_id}) was Already Sudo"
        elif DB_URI is not None:
            msg = DbManger().db_addsudo(user_id)
        else:
            with open("sudo_users.txt", "a", encoding="UTF-8") as file:
                file.write(f"{user_id}\n")
                SUDO_USERS.add(user_id)
                msg = f"User({user_id}) is Promoted as Sudo"
    elif reply_message is None:
        msg = "Give ID or Reply To message of whom you want to Promote"
    else:
        # Trying to authorize someone by replying
        user_id = reply_message.from_user.id
        if user_id in SUDO_USERS:
            msg = f"User({user_id}) was Already Sudo"
        elif DB_URI is not None:
            msg = DbManger().db_addsudo(user_id)
        else:
            with open("sudo_users.txt", "a", encoding="UTF-8") as file:
                file.write(f"{user_id}\n")
                SUDO_USERS.add(user_id)
                msg = f"User({user_id}) is Promoted as Sudo"
    sendMessage(msg, context.bot, update)


def remove_sudo(update, context):
    """Remove a user from Sudo"""
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(" ")
    if len(message_) == 2:
        user_id = int(message_[1])
        if user_id in SUDO_USERS:
            if DB_URI is not None:
                msg = DbManger().db_rmsudo(user_id)
            else:
                SUDO_USERS.remove(user_id)
                msg = f"User({user_id}) was Demoted"
        else:
            msg = f"User({user_id}) was Not a Sudo"
    elif reply_message is None:
        msg = "Give ID or Reply To message of whom you want to remove from Sudo"
    else:
        user_id = reply_message.from_user.id
        if user_id in SUDO_USERS:
            if DB_URI is not None:
                msg = DbManger().db_rmsudo(user_id)
            else:
                SUDO_USERS.remove(user_id)
                msg = f"User({user_id}) was Demoted"
        else:
            msg = f"User({user_id}) was Not a Sudo"
    if DB_URI is None:
        with open("sudo_users.txt", "a", encoding="UTF-8") as file:
            file.truncate(0)
            for i in SUDO_USERS:
                file.write(f"{i}\n")
    sendMessage(msg, context.bot, update)


def send_auth_chats(update, context):
    """Send the list of authorized chats"""
    user = sudo = ""
    user += "\n".join(str(id) for id in AUTHORIZED_CHATS)
    sudo += "\n".join(str(id) for id in SUDO_USERS)
    sendMessage(
        f"<b><u>Authorized Chats</u></b>\n\
                <code>{user}</code>\n\
                <b><u>Sudo Users</u></b>\n\
                <code>{sudo}</code>",
        context.bot,
        update,
    )


send_auth_handler = CommandHandler(
    command=BotCommands.AuthorizedUsersCommand,
    callback=send_auth_chats,
    filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
    run_async=True,
)
authorize_handler = CommandHandler(
    command=BotCommands.AuthorizeCommand,
    callback=authorize,
    filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
    run_async=True,
)
un_authorize_handler = CommandHandler(
    command=BotCommands.UnAuthorizeCommand,
    callback=un_authorize,
    filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
    run_async=True,
)
add_sudo_handler = CommandHandler(
    command=BotCommands.AddSudoCommand,
    callback=add_sudo,
    filters=CustomFilters.owner_filter,
    run_async=True,
)
remove_sudo_handler = CommandHandler(
    command=BotCommands.RmSudoCommand,
    callback=remove_sudo,
    filters=CustomFilters.owner_filter,
    run_async=True,
)

dispatcher.add_handler(send_auth_handler)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(un_authorize_handler)
dispatcher.add_handler(add_sudo_handler)
dispatcher.add_handler(remove_sudo_handler)
