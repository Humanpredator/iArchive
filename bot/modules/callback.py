import os


from instaloader import Profile
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

from bot import dispatcher, OWNER_ID, INSTA
from bot.helper.down_utilis.insta_down import download_insta
from bot.helper.ext_utils.bot_utils import usercheck
from bot.helper.telegram_helper.message_utils import *


def cb_handler(update, context):
    USER = usercheck()
    session = f"./{USER}"
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
        bot.send_document(query.message.chat.id, ppic_hd, caption=f"<b>Name:</b>{full_name}\n<b>Username:</b>{username}",
                          parse_mode="HTML")

    elif query.data.startswith("post"):
        query.answer()
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Pictures Only", callback_data=f"photos#{username}"),
                    InlineKeyboardButton(
                        "Videos Only", callback_data=f"videos#{username}")
                ],
                [
                    InlineKeyboardButton(
                        "Pictures and videos", callback_data=f"picandvid#{username}"),
                    InlineKeyboardButton(
                        "All Posts", callback_data=f"allposts#{username}"),
                ]
            ]
        )
        bot.send_message(chat_id=query.message.chat.id, text="Select the type of posts you want to fetch?",
                         reply_markup=reply_markup, parse_mode="HTML")

    elif query.data.startswith("photos"):
        query.answer()
        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        else:
            m = query.edit_message_text(
                "Starting Downloading..\nThis may take time depending upon number of Posts.")
            dir = f"{OWNER_ID}/{username}"
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-videos",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", username
            ]
            download_insta(command, m, dir, username, chat_id, fetch='Photos')

    elif query.data.startswith("videos"):
        query.answer()
        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        m = query.edit_message_text(
            "Starting Downloading..\nThis may take time depending upon number of Posts.")
        dir = f"{OWNER_ID}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-pictures",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
        ]
        download_insta(command, m, dir, username, chat_id, fetch='Videos')

    elif query.data.startswith("picandvid"):
        query.answer()
        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        m = query.edit_message_text(
            "Starting Downloading..\nThis may take time depending upon number of Posts.")
        dir = f"{OWNER_ID}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
        ]
        download_insta(command, m, dir, username,
                       chat_id, fetch='Photos and Videos')

    elif query.data.startswith("allposts"):
        query.answer()
        chat_id = query.message.chat.id
        if media_count == 0:
            query.edit_message_text("There are no posts by the user")

        m = query.edit_message_text(
            "Starting Downloading..\nThis may take longer time Depending upon number of posts.")
        dir = f"{OWNER_ID}/{username}"
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
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
        ]
        download_insta(command, m, dir, username, chat_id, fetch='All Posts')

    elif query.data.startswith("igtv"):
        query.answer()
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Yes", callback_data=f"yes#{username}"),
                    InlineKeyboardButton("No", callback_data=f"no#{username}")
                ]
            ]
        )
        bot.send_message(chat_id=query.message.chat.id,
                         text=f"Do you want to download IGTV Posts of {full_name}?", reply_markup=reply_markup)

    elif query.data.startswith("yes"):
        query.answer()
        chat_id = query.message.chat.id
        if igtv_count == 0:
            query.edit_message_text("There are no IGTV posts by the user")

        m = query.edit_message_text(
            "Starting Downloading..\nThis may take longer time Depending upon number of posts.")
        dir = f"{OWNER_ID}/{username}"

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
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
        ]
        download_insta(command, m, dir, username, chat_id, fetch='IGTV')

    elif query.data.startswith("no"):
        query.answer()
        m = bot.send_message(chat_id=query.message.chat.id,
                             text="Process Cancelled")
        bot.delete_message(chat_id=query.message.chat.id,
                           message_id=m.message_id)

    elif query.data.startswith("followers"):
        query.answer()
        chat_id = query.message.chat.id
        m = bot.send_message(
            chat_id, f"Fetching Followers List of {full_name}")
        try:
            followers = f"**Followers List for {full_name}**\n\n"
            f = profile.get_followers()
            for p in f:
                followers += f"\nName: {p.username}:Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s_followers_list.txt",
                             mode='w', encoding='utf-8')
            text_file.write(followers)
            text_file.close()
            m.delete()
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s_followers_list.txt", 'rb'),
                              caption=f"Followers List for {full_name}")
            os.remove(f"{username}'s_followers_list.txt")
            LOGGER.info(f"Followers list of {full_name} removed")
        except Exception as e:
            LOGGER.error(e)
            bot.send_message(chat_id=chat_id, text=f"Error Occurred: {e}")


    elif query.data.startswith("following"):
        query.answer()
        chat_id = query.message.chat.id
        m = bot.send_message(
            chat_id, f"Fetching Following list of {full_name}")
        try:
            followees = f"**Following List for {full_name}**\n\n"
            f = profile.get_followees()
            for p in f:
                followees += f"\nName: {p.username}:Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s_following_list.txt",
                             mode='w', encoding='utf-8')
            text_file.write(followees)
            text_file.close()
            m.delete()
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s_following_list.txt", 'rb'),
                              caption=f"Following List for {full_name}")
            os.remove(f"{username}'s_following_list.txt")
            LOGGER.info(f"Following list of {full_name} removed")
        except Exception as e:
            LOGGER.error(e)
            bot.send_message(chat_id=chat_id, text=f"Error Occurred: {e}")


    else:
        dir = f"{OWNER_ID}/{username}"
        chat_id = query.message.chat.id
        query.answer()
        m = bot.send_message(
            chat_id, "Starting Downloading..\nThis may take longer time Depending upon number of posts.")
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
                "--login", USER,
                "--sessionfile", session,
                "--dirname-pattern", dir,
                ":feed"
            ]
            download_insta(command, m, dir, username, chat_id, fetch='My Feed')

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
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                ":saved"
            ]
            download_insta(command, m, dir, username,
                           chat_id, fetch='My Saved')

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
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", username
            ]
            download_insta(command, m, dir, username, chat_id, fetch='Tagged')

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
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", username
            ]
            download_insta(command, m, dir, username, chat_id, fetch='Stories')

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
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                ":stories"
            ]
            download_insta(command, m, dir, username, chat_id,
                           fetch='Stories of My Following')
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
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", username
            ]
            download_insta(command, m, dir, username,
                           chat_id, fetch='Highlights')


callback_handler = CallbackQueryHandler(cb_handler)
dispatcher.add_handler(callback_handler)
