"""InstaDL-Bot, Telegram Bot to download Instagram Posts and Reels"""
import json

from instaloader import Profile
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from telegram.ext import CommandHandler

from bot import INSTA, LOGGER, OWNER_ID, STATUS, bot, dispatcher
from bot.helper.down_utilis.insta_down import download_insta
from bot.helper.ext_utils.bot_utils import acc_type, is_link, usercheck, yes_or_no
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import (
    deleteMessage,
    editMessage,
    sendMessage,
)


def post(update, context):
    """Download Instagram Posts"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        msg = sendMessage("Checking the given username, please wait...!",
                          context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            username = args[1]
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Please follow <code>@{username}</code> to download posts from that account.",
                    msg,
                )

            else:
                reply_markup = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "Pictures Only",
                            callback_data=f"photos#{username}"),
                        InlineKeyboardButton(
                            "Videos Only", callback_data=f"videos#{username}"),
                    ],
                    [
                        InlineKeyboardButton(
                            "Pictures and Videos",
                            callback_data=f"picandvid#{username}",
                        ),
                        InlineKeyboardButton(
                            "ALL Posts", callback_data=f"allposts#{username}"),
                    ],
                ])
                editMessage(
                    "Select the type of posts you want to fetch?",
                    msg,
                    reply_markup=reply_markup,
                )

    else:
        sendMessage("Please send a username...!", context.bot, update)


def igtv(update, context):
    """Download IGTV from a given username"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        username = args[1]
        msg = sendMessage("Checking the given username, please wait...!",
                          context.bot, update)
        if 1 not in STATUS:
            editMessage("You must login  /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Please follow <code>@{username}</code> to download IGTV from that account.",
                    msg,
                )

        editMessage(f"Fetching IGTV from <code>@{username}</code>", msg)
        profile = Profile.from_username(INSTA.context, username)
        igtv_count = profile.igtvcount
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("Yes", callback_data=f"yes#{username}"),
            InlineKeyboardButton("No", callback_data=f"no#{username}"),
        ]])
        editMessage(
            f"Do you want to download all IGTV posts?\nThere are {igtv_count} posts.",
            msg,
            reply_markup=reply_markup,
        )
    else:
        sendMessage("Please send a username...!", context.bot, update)


def followers(update, context):
    """Get followers list of a given username"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        username = args[1]
        msg = sendMessage("Checking the given username, please wait...!",
                          context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Please follow <code>@{username}</code>",
                    msg,
                )

        profile = Profile.from_username(INSTA.context, username)
        name = profile.full_name
        editMessage(
            f"Fetching followers list of <code>@{username}</code>",
            msg,
        )
        chat_id = update.message.chat_id
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
            deleteMessage(context.bot, msg)

            with open(f"{username}_followers.json", "r",
                      encoding="UTF-8") as file:
                context.bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=f"Followers list of @{name}",
                )
            LOGGER.info("Followers list of %s sent to %s", name, chat_id)
        except TelegramError as error:
            LOGGER.error(error)
            editMessage(f"Error Occurred: {error}", msg)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def following_(update, context):
    """Get following list of a given username"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        username = args[1]
        msg = sendMessage("Checking the given username, please wait...!",
                          context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Please follow <code>@{username}</code>",
                    msg,
                )

        profile = Profile.from_username(INSTA.context, username)
        full_name = profile.full_name
        editMessage(
            f"Fetching following list of <code>@{username}</code>",
            msg,
        )
        chat_id = update.message.chat_id
        try:
            following_json = {}
            following_list = profile.get_following()
            for following in following_list:
                following_json[following.username] = {
                    "full_name": following.full_name,
                    "profile_pic_url": following.profile_pic_url,
                    "profile_link": f"www.instagram.com/{following.username}",
                }
            with open(f"{username}_following.json", "w",
                      encoding="UTF-8") as file:
                json.dump(following_json, file)
            deleteMessage(context.bot, msg)

            with open(f"{username}_following.json", "r",
                      encoding="UTF-8") as file:
                context.bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=f"Following list of @{full_name}",
                )
            LOGGER.info("Following list of %s sent to %s", full_name, chat_id)
        except TelegramError as error:
            LOGGER.error(error)
            editMessage(f"Error Occurred: {error}", msg)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def fans_(update, context):
    """Get fans list of a given username"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        msg = sendMessage("Checking the given username, please wait...!",
                          context.bot, update)
        username = args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Please follow <code>@{username}</code>",
                    msg,
                )

        profile = Profile.from_username(INSTA.context, username)
        full_name = profile.full_name
        editMessage(
            f"Fetching fans list of <code>@{username}</code>",
            msg,
        )
        chat_id = update.message.chat_id
        followers_records = profile.get_followers()
        following_records = profile.get_followees()
        follower_list = []
        following_list = []
        for follower_detail in followers_records:
            users = follower_detail.username
            follower_list.append(users)
        for following_detail in following_records:
            users = following_detail.username
            following_list.append(users)
        fans = [value for value in following_list if value in follower_list]
        try:
            fans_json = {}
            for fan in fans:
                fans_json[fan] = {
                    "user_name": fan,
                    "profile_link": f"www.instagram.com/{fan}",
                }
            with open(f"{username}_fans.json", "w", encoding="UTF-8") as file:
                json.dump(fans_json, file)

            deleteMessage(context.bot, msg)

            with open(f"{username}_fans.json", "r", encoding="UTF-8") as file:
                bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=f"Fans list of @{full_name}",
                )
            LOGGER.info("Fans list of %s sent to %s", full_name, chat_id)
        except TelegramError as error:
            LOGGER.error(error)
            editMessage(f"Error occurred: {error}", msg)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def not_following(update, context):
    """Get not following list of a given username"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        msg = sendMessage("Checking the given username, please wait...!",
                          context.bot, update)
        username = args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Please follow <code>@{username}</code>",
                    msg,
                )

        profile = Profile.from_username(INSTA.context, username)
        full_name = profile.full_name
        editMessage(
            f"Fetching not following list of <code>@{username}</code>",
            msg,
        )
        chat_id = update.message.chat_id
        followers_records = profile.get_followers()
        following_records = profile.get_followees()
        followers_list = []
        following_list = []
        for follower in followers_records:
            users = follower.username
            followers_list.append(users)
        for following in following_records:
            users = following.username
            following_list.append(users)

        fans = list(set(followers_list) - set(following_list))

        try:
            fans_json = {}
            for fan in fans:
                fans_json[fan] = {
                    "user_name": fan,
                    "profile_link": f"www.instagram.com/{fan}",
                }
            with open(f"{username}_not_following.json", "w",
                      encoding="UTF-8") as file:
                json.dump(fans_json, file)
            deleteMessage(context.bot, msg)
            with open(f"{username}_not_following.json", "r",
                      encoding="UTF-8") as file:
                bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=f"<b>{full_name}'s Non_followers list</b>\n\n\
                    <b>Total Non_followers:</b> {len(fans)}\n\n\
                    <b>Total Followers:</b>  {len(followers_list)}\n\n\
                    <b>Total Following:</b>  {len(following_list)}",
                    parse_mode="HTML",
                )
            LOGGER.info("Not following list of %s sent to %s", full_name,
                        chat_id)
        except TelegramError as error:
            LOGGER.error(error)
            editMessage(f"Error occurred: {error}", msg)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def feed(update, context):
    """Download posts from a given username"""
    chat_id = update.message.chat_id
    current_user = usercheck()
    session = f"./{current_user}"
    args = update.message.text.split(" ", maxsplit=1)
    directory = f"{OWNER_ID}/{current_user}"
    msg = sendMessage("Checking the details, Please wait...!", context.bot,
                      update)
    if len(args) > 1:
        if args[1].isdigit():
            count = args[1]
            if 1 not in STATUS:
                editMessage("You must /login ", msg)

            editMessage(
                f"Fetching {count} posts from <code>@{current_user}</code>'s feed.",
                msg)
            editMessage(
                "Starting downloading..\nThis may take longer time depending upon number of posts.",
                msg,
            )
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
                "--count",
                count,
            ]

            download_insta(command,
                           msg,
                           directory,
                           current_user,
                           chat_id,
                           fetch="My Feed")
        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            editMessage("Please send a valid number...!", msg)
    else:
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
                       current_user,
                       chat_id,
                       fetch="My Feed")


def saved(update, context):
    """Download posts from a given username"""
    chat_id = update.message.chat_id
    current_user = usercheck()
    session = f"./{current_user}"
    args = update.message.text.split(" ", maxsplit=1)
    directory = f"{OWNER_ID}/{current_user}"
    msg = sendMessage("Checking the details, Please wait...!", context.bot,
                      update)
    if len(args) > 1:
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        if args[1].isdigit():
            count = args[1]
            editMessage(f"Fetching {count} posts from saved.", msg)
            editMessage(
                "Starting downloading..\nThis may take longer time depending upon number of posts.",
                msg,
            )
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
                "--count",
                count,
            ]
            download_insta(command,
                           msg,
                           directory,
                           current_user,
                           chat_id,
                           fetch="My Saved")
        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            editMessage("Please send a count...!", msg)
    else:
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
                       current_user,
                       chat_id,
                       fetch="My Saved")


def tagged(update, context):
    """Download posts from a given username"""
    chat_id = update.message.chat_id
    current_user = usercheck()
    session = f"./{current_user}"
    args = update.message.text.split(" ", maxsplit=1)
    directory = f"{OWNER_ID}/{current_user}"
    msg = sendMessage("Checking the details, please wait...!", context.bot,
                      update)
    if len(args) > 1:
        username = args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"This account is private and you are not following {username}.",
                    msg,
                )

        editMessage(f"Fetching posts from <code>@{username}</code>'s tagged",
                    msg)
        editMessage(
            "Starting downloading..\nThis may take longer time depending upon number of posts.",
            msg,
        )
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
    else:
        sendMessage("Please send a username...!", context.bot, update)


def story(update, context):
    """Download posts from a given username"""
    chat_id = update.message.chat_id
    current_user = usercheck()
    session = f"./{current_user}"
    args = update.message.text.split(" ", maxsplit=1)
    msg = sendMessage("Checking the details, please wait...!", context.bot,
                      update)
    if len(args) > 1:
        username = args[1]
        directory = f"{OWNER_ID}/{username}"
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"This account is private and you are not following {username}.",
                    msg,
                )

        editMessage(f"Fetching posts from <code>@{username}</code>'s story.",
                    msg)
        editMessage(
            "Starting downloading..\nThis may take longer time depending upon number of posts.",
            msg,
        )
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

    else:
        sendMessage("Please send a username...!", context.bot, update)


def stories(update, context):
    """Download posts from a given username"""
    chat_id = update.message.chat_id
    current_user = usercheck()
    session = f"./{current_user}"
    username = current_user
    directory = f"{OWNER_ID}/{username}"
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) < 1:
        msg = sendMessage("Checking the details, Please wait...!", context.bot,
                          update)
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        editMessage("Fetching posts from your stories.", msg)
        editMessage(
            "Starting downloading..\nThis may take longer time depending upon number of posts.",
            msg,
        )
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
        download_insta(command,
                       msg,
                       directory,
                       username,
                       chat_id,
                       fetch="My Following Stories")
    else:
        sendMessage("Please send command only..!", context.bot, update)


def highlights(update, context):
    """Download posts from a given username"""
    chat_id = update.message.chat_id
    current_user = usercheck()
    session = f"./{current_user}"
    args = update.message.text.split(" ", maxsplit=1)

    if len(args) > 1:
        msg = sendMessage("Checking the details, Please wait...!", context.bot,
                          update)
        username = args[1]
        directory = f"{OWNER_ID}/{username}"
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"This account is private and you are not following {username}.",
                    msg,
                )

        editMessage(
            f"Fetching posts from <code>@{username}</code>'s highlights.", msg)
        editMessage(
            "Starting downloading..\nThis may take longer time depending upon number of posts.",
            msg,
        )
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
    else:
        sendMessage("Please send a username...!", context.bot, update)


post_handler = CommandHandler(
    BotCommands.IgPostCommand,
    post,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(post_handler)

igtv_handler = CommandHandler(
    BotCommands.IgTvCommand,
    igtv,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(igtv_handler)

followers_handler = CommandHandler(
    BotCommands.IgFollowersCommand,
    followers,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(followers_handler)

followees_handler = CommandHandler(
    BotCommands.IgFollowingCommand,
    following_,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(followees_handler)

fans_handler = CommandHandler(
    BotCommands.IgFansCommand,
    fans_,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(fans_handler)

not_following_handler = CommandHandler(
    BotCommands.IgNotFollowingCommand,
    not_following,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(not_following_handler)

feed_handler = CommandHandler(
    BotCommands.IgFeedCommand,
    feed,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(feed_handler)

saved_handler = CommandHandler(
    BotCommands.IgSavedCommand,
    saved,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(saved_handler)

tagged_handler = CommandHandler(
    BotCommands.IgTaggedCommand,
    tagged,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(tagged_handler)

story_handler = CommandHandler(
    BotCommands.IgStoryCommand,
    story,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(story_handler)

stories_handler = CommandHandler(
    BotCommands.IgStoriesCommand,
    stories,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(stories_handler)

highlights_handler = CommandHandler(
    BotCommands.IgHighlightsCommand,
    highlights,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(highlights_handler)
