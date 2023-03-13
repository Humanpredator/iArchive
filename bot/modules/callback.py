"""Callback handler for the bot."""
import json

from instaloader import Profile
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import TelegramError
from telegram.ext import CallbackQueryHandler

from bot import INSTA, LOGGER, OWNER_ID, bot, dispatcher
from bot.helper.down_utilis.insta_down import download_insta
from bot.helper.ext_utils.bot_utils import usercheck


# noinspection PyUnusedLocal
def cb_handler(update, context):
    """Callback handler for the bot."""
    current_user = usercheck()
    session = f"./{current_user}"
    query = update.callback_query
    username = query.data.split("#")[1]
    profile = Profile.from_username(INSTA.context, username)
    media_count = profile.mediacount
    full_name = profile.full_name
    igtv_count = profile.igtvcount

    if query.data.startswith("ppic"):
        profile = Profile.from_username(INSTA.context, username)
        ppic_hd = profile.profile_pic_url
        query.answer()
        bot.send_document(
            query.message.chat.id,
            ppic_hd,
            caption=f"<b>Name:</b>{full_name}\n<b>Username:</b>{username}",
            parse_mode="HTML",
        )

    elif query.data.startswith("post"):
        query.answer()
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Pictures Only",
                                     callback_data=f"photos#{username}"),
                InlineKeyboardButton("Videos Only",
                                     callback_data=f"videos#{username}"),
            ],
            [
                InlineKeyboardButton("Pictures and videos",
                                     callback_data=f"picandvid#{username}"),
                InlineKeyboardButton("All Posts",
                                     callback_data=f"allposts#{username}"),
            ],
        ])
        bot.send_message(
            chat_id=query.message.chat.id,
            text="Select the type of posts you want to fetch?",
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    elif query.data.startswith("photos"):
        query.answer()
        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        else:
            msg = query.edit_message_text(
                "Starting Downloading..\nThis may take time depending upon number of Posts."
            )
            directory = f"{OWNER_ID}/{username}"
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-videos",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login",
                current_user,
                "-f",
                session,
                "--dirname-pattern",
                directory,
                "--",
                username,
            ]
            download_insta(command,
                           msg,
                           directory,
                           username,
                           chat_id,
                           fetch="Photos")

    elif query.data.startswith("videos"):
        query.answer()
        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        msg = query.edit_message_text(
            "Starting Downloading..\nThis may take time depending upon number of Posts."
        )
        directory = f"{OWNER_ID}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-pictures",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login",
            current_user,
            "-f",
            session,
            "--dirname-pattern",
            directory,
            "--",
            username,
        ]
        download_insta(command,
                       msg,
                       directory,
                       username,
                       chat_id,
                       fetch="Videos")

    elif query.data.startswith("picandvid"):
        query.answer()
        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        msg = query.edit_message_text(
            "Starting Downloading..\nThis may take time depending upon number of Posts."
        )
        directory = f"{OWNER_ID}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login",
            current_user,
            "-f",
            session,
            "--dirname-pattern",
            directory,
            "--",
            username,
        ]
        download_insta(command,
                       msg,
                       directory,
                       username,
                       chat_id,
                       fetch="Photos and Videos")

    elif query.data.startswith("allposts"):
        query.answer()
        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        msg = query.edit_message_text(
            "Starting Downloading..\nThis may take longer time Depending upon number of posts."
        )
        directory = f"{OWNER_ID}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--igtv",
            "--highlights",
            "--stories",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login",
            current_user,
            "-f",
            session,
            "--dirname-pattern",
            directory,
            "--",
            username,
        ]
        download_insta(command,
                       msg,
                       directory,
                       username,
                       chat_id,
                       fetch="All Posts")

    elif query.data.startswith("igtv"):
        query.answer()
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("Yes", callback_data=f"yes#{username}"),
            InlineKeyboardButton("No", callback_data=f"no#{username}"),
        ]])
        bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Do you want to download IGTV Posts of {full_name}?",
            reply_markup=reply_markup,
        )

    elif query.data.startswith("yes"):
        query.answer()
        chat_id = query.message.chat.id
        if igtv_count == 0:
            query.edit_message_text("There are no IGTV posts by the user")

        msg = query.edit_message_text(
            "Starting Downloading..\nThis may take longer time Depending upon number of posts."
        )
        directory = f"{OWNER_ID}/{username}"

        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--igtv",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login",
            current_user,
            "-f",
            session,
            "--dirname-pattern",
            directory,
            "--",
            username,
        ]
        download_insta(command,
                       msg,
                       directory,
                       username,
                       chat_id,
                       fetch="IGTV")

    elif query.data.startswith("no"):
        query.answer()
        msg = bot.send_message(chat_id=query.message.chat.id,
                               text="Process Cancelled")
        bot.delete_message(chat_id=query.message.chat.id,
                           message_id=msg.message_id)

    elif query.data.startswith("followers"):
        query.answer()
        chat_id = query.message.chat.id
        msg = bot.send_message(chat_id,
                               f"Fetching Followers List of {full_name}")
        try:
            followers_json = {}
            followers_list = profile.get_followers()
            for follower in followers_list:
                followers_json[follower.username] = {
                    "full_name": follower.full_name,
                    "profile_pic_url": follower.profile_pic_url,
                    "profile_link": f"www.instagram.com/{follower.username}",
                }
            with open(f"{username}_followers.json", "w",
                      encoding="UTF-8") as file:
                json.dump(followers_json, file)
            msg.delete()
            with open(f"{username}_followers.json", "rb") as file:
                bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=f"Followers List for {full_name}",
                )
            LOGGER.info("Followers List for %s sent to %s", full_name, chat_id)
        except TelegramError as error:
            LOGGER.error(error)
            bot.send_message(chat_id=chat_id, text=f"Error Occurred: {error}")

    elif query.data.startswith("following"):
        query.answer()
        chat_id = query.message.chat.id
        msg = bot.send_message(chat_id,
                               f"Fetching Following list of {full_name}")
        try:
            following_json = {}
            following_list = profile.get_followees()
            for following in following_list:
                following_json[following.username] = {
                    "full_name": following.full_name,
                    "profile_pic_url": following.profile_pic_url,
                    "profile_link": f"www.instagram.com/{following.username}",
                }
            with open(f"{username}_following.json", "w",
                      encoding="UTF-8") as file:
                json.dump(following_json, file)

            msg.delete()
            with open(f"{username}_following.json", "rb") as file:
                bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=f"Following List for {full_name}",
                )
            LOGGER.info("Following List for %s sent to %s", full_name, chat_id)
        except TelegramError as error:
            LOGGER.error(error)
            bot.send_message(chat_id=chat_id, text=f"Error Occurred: {error}")

    else:
        directory = f"{OWNER_ID}/{username}"
        chat_id = query.message.chat.id
        query.answer()
        msg = bot.send_message(
            chat_id,
            "Starting Downloading..\nThis may take longer time Depending upon number of posts.",
        )
        cmd = query.data.split("#")[0]
        username = query.data.split("#")[1]
        if cmd == "feed":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login",
                current_user,
                "--sessionfile",
                session,
                "--dirname-pattern",
                directory,
                ":feed",
            ]
            download_insta(command,
                           msg,
                           directory,
                           username,
                           chat_id,
                           fetch="My Feed")

        elif cmd == "saved":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login",
                current_user,
                "-f",
                session,
                "--dirname-pattern",
                directory,
                ":saved",
            ]
            download_insta(command,
                           msg,
                           directory,
                           username,
                           chat_id,
                           fetch="My Saved")

        elif cmd == "tagged":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--tagged",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login",
                current_user,
                "-f",
                session,
                "--dirname-pattern",
                directory,
                "--",
                username,
            ]
            download_insta(command,
                           msg,
                           directory,
                           username,
                           chat_id,
                           fetch="Tagged")

        elif cmd == "stories":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--stories",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login",
                current_user,
                "-f",
                session,
                "--dirname-pattern",
                directory,
                "--",
                username,
            ]
            download_insta(command,
                           msg,
                           directory,
                           username,
                           chat_id,
                           fetch="Stories")

        elif cmd == "fstories":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-captions",
                "--no-posts",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login",
                current_user,
                "-f",
                session,
                "--dirname-pattern",
                directory,
                ":stories",
            ]
            download_insta(
                command,
                msg,
                directory,
                username,
                chat_id,
                fetch="Stories of My Following",
            )
        elif cmd == "highlights":
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-posts",
                "--highlights",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login",
                current_user,
                "-f",
                session,
                "--dirname-pattern",
                directory,
                "--",
                username,
            ]
            download_insta(command,
                           msg,
                           directory,
                           username,
                           chat_id,
                           fetch="Highlights")


callback_handler = CallbackQueryHandler(cb_handler)
dispatcher.add_handler(callback_handler)
