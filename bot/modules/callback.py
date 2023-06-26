"""Callback handler for the bot."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackQueryHandler

from bot import bot, dispatcher
from bot.helper.ig_utils.ig_down import (
    check_username,
    download_all_posts,
    download_feed,
    download_following_stories,
    download_highlights,
    download_igtv,
    download_posts,
    download_saved,
    download_stories,
    download_tagged,
    fetch_followers,
    fetch_following,
)


# noinspection PyUnusedLocal
def cb_handler(update, context):
    """Callback handler for the bot."""
    query = update.callback_query
    cb_data = query.data.split("#")
    query_type = cb_data[0]
    user_id = cb_data[1]
    profile, error = check_username(user_id)
    if error:
        query.answer()
        query.edit_message_text(error)
        return False
    media_count = profile.mediacount
    full_name = profile.full_name
    igtv_count = profile.igtvcount

    if query_type == "PPIC":
        ppic_hd = profile.profile_pic_url
        query.answer()
        bot.send_document(
            query.message.chat.id,
            ppic_hd,
            caption=f"<b>Name:</b>{full_name}\n<b>Username:</b>{profile.username}",
            parse_mode=ParseMode.HTML,
        )

    elif query_type == "POST":
        query.delete_message()
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Picture Posts",
                                     callback_data=f"PIC#{user_id}"),
                InlineKeyboardButton("Video Posts",
                                     callback_data=f"VID#{user_id}"),
            ],
            [
                InlineKeyboardButton("Picture & Video Posts",
                                     callback_data=f"PICVID#{user_id}"),
                InlineKeyboardButton("ALL Posts",
                                     callback_data=f"ALLPOST#{user_id}"),
            ],
        ])
        bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Choose the type of posts to download from {full_name}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )

    elif query_type == "PIC":
        query.answer()

        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        else:
            msg = query.edit_message_text(
                "Starting Downloading..\nThis may take time depending upon number of Posts."
            )
            download_posts(profile, msg, picture=True)

    elif query_type == "VID":
        query.answer()

        if media_count == 0:
            query.edit_message_text("There are no posts by the user")
        else:
            msg = query.edit_message_text(
                "Starting Downloading..\nThis may take time depending upon number of Posts."
            )
            download_posts(profile, msg, video=True)

    elif query_type == "PICVID":
        query.answer()

        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")
        else:
            msg = query.edit_message_text(
                "Starting Downloading..\nThis may take time depending upon number of Posts."
            )
            download_posts(profile, msg, picture=True, video=True)

    elif query_type == "ALLPOST":
        query.answer()

        if media_count == 0:
            query.edit_message_text("There are no posts by the user")
        else:
            msg = query.edit_message_text(
                "Starting Downloading..\nThis may take time depending upon number of Posts."
            )

            download_all_posts(profile, msg)

    elif query_type == "IGTV":
        query.answer()

        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("Yes", callback_data=f"YES#{user_id}"),
            InlineKeyboardButton("No", callback_data=f"NO#{user_id}"),
        ]])
        bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Do you want to download IGTV Posts of {full_name}?",
            reply_markup=reply_markup,
        )

    elif query_type == "YES":
        query.answer()

        if igtv_count == 0:
            query.edit_message_text("There are no IGTV posts by the user")

        msg = query.edit_message_text(
            "Starting Downloading..\nThis may take longer time Depending upon number of posts."
        )
        download_igtv(profile, msg)

    elif query_type == "NO":
        query.answer()

        bot.send_message(chat_id=query.message.chat.id,
                         text="Process Cancelled by User")

    elif query_type == "FOLLOWER":
        query.answer()

        msg = bot.send_message(query.message.chat.id,
                               f"Fetching Followers List of {full_name}")
        fetch_followers(profile, msg)

    elif query_type == "FOLLOWING":
        query.answer()

        msg = bot.send_message(query.message.chat.id,
                               f"Fetching Following list of {full_name}")
        fetch_following(profile, msg)

    elif query_type == "HIGHLIGHT":
        query.answer()

        msg = bot.send_message(query.message.chat.id,
                               f"Downloading Highlights of {full_name}")
        download_highlights(profile, msg)

    elif query_type == "FEED":
        query.answer()

        msg = bot.send_message(query.message.chat.id,
                               f"Downloading Feed of {full_name}")
        download_feed(msg)

    elif query_type == "SAVED":
        query.answer()

        msg = bot.send_message(query.message.chat.id,
                               f"Downloading Saved of {full_name}")
        download_saved(profile, msg)

    elif query_type == "STORY":
        query.answer()

        msg = bot.send_message(query.message.chat.id,
                               f"Downloading Saved of {full_name}")
        download_stories(profile, msg)

    elif query_type == "TAG":
        query.answer()

        msg = bot.send_message(query.message.chat.id,
                               f"Downloading Saved of {full_name}")
        download_tagged(profile, msg)

    elif query_type == "FSTORY":
        query.answer()

        msg = bot.send_message(query.message.chat.id,
                               f"Downloading Saved of {full_name}")
        download_following_stories(msg)

    else:
        query.answer()

        msg = bot.send_message(
            query.message.chat.id,
            f"Something went wrong. Please try again later.")


callback_handler = CallbackQueryHandler(cb_handler)
dispatcher.add_handler(callback_handler)
