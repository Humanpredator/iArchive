import os

from instaloader import Profile
from telegram import InlineKeyboardButton
from telegram.ext import CommandHandler

from bot import dispatcher, OWNER_ID, INSTA, STATUS
from bot.helper.down_utilis.insta_down import download_insta
from bot.helper.ext_utils.bot_utils import usercheck, acc_type, is_link, yes_or_no
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import *


def post(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            username = args[1]
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.",
                    m)
                
            else:
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Pictures Only", callback_data=f"photos#{username}"),
                            InlineKeyboardButton("Videos Only", callback_data=f"videos#{username}")
                        ],
                        [
                            InlineKeyboardButton("Pictures and Videos", callback_data=f"picandvid#{username}"),
                            InlineKeyboardButton("ALL Posts", callback_data=f"allposts#{username}"),
                        ]
                    ]
                )
                editMessage("Select the type of posts you want to fetch?", m, reply_markup=reply_markup)
                
    else:
        sendMessage("Please send a username...!", context.bot, update)


def igtv(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        username = args[1]
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must login  /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.",
                    m)
                
        editMessage(f"Fetching IGTV from <code>@{username}</code>", m)
        profile = Profile.from_username(INSTA.context, username)
        igtv_count = profile.igtvcount
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yes", callback_data=f"yes#{username}"),
                    InlineKeyboardButton("No", callback_data=f"no#{username}")
                ]
            ]
        )
        editMessage(f"Do you want to download all IGTV posts?\nThere are {igtv_count} posts.", m,
                    reply_markup=reply_markup)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def followers(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        username = args[1]
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:

            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.",
                    m)
                
        profile = Profile.from_username(INSTA.context, username)
        name = profile.full_name
        editMessage(
            f"Fetching followers list of <code>@{username}</code>\n It may take few minutes, pls be patient...!", m)
        chat_id = update.message.chat_id
        try:
            followers = f"**Followers List for {name}**\n\n"
            f = profile.get_followers()
            for p in f:
                followers += f"\nName: {p.username}:Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s_followers_list.txt", mode='w', encoding='utf-8')
            text_file.write(followers)
            text_file.close()
            deleteMessage(context.bot, m)
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s_followers_list.txt", 'rb'),
                              caption=f"Followers List for {name}")
            os.remove(f"{username}'s_followers_list.txt")
            LOGGER.info("followers list removed")
        except Exception as e:
            LOGGER.error(e)
            editMessage(f"Error Occurred: {e}", m)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def following(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        username = args[1]
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.",
                    m)
                
        profile = Profile.from_username(INSTA.context, username)
        full_name = profile.full_name
        editMessage(
            f"Fetching following list of <code>@{username}</code>\n It may take few minutes, pls be patient...!", m)
        chat_id = update.message.chat_id
        try:
            followees = f"**Following List for {full_name}**\n\n"
            f = profile.get_followees()
            for p in f:
                followees += f"\nName: {p.username}:Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s_following_list.txt", mode='w', encoding='utf-8')
            text_file.write(followees)
            text_file.close()
            deleteMessage(context.bot, m)
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s_following_list.txt", 'rb'),
                              caption=f"Following List for {full_name}")
            os.remove(f"{username}'s_following_list.txt")
            LOGGER.info("following list removed")
        except Exception as e:
            LOGGER.error(e)
            editMessage(f"Error occurred: {e}", m)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def fans(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        username = args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.",
                    m)
                
        profile = Profile.from_username(INSTA.context, username)
        full_name = profile.full_name
        editMessage(f"Fetching fans list of <code>@{username}</code>\n It may take few minutes, pls be patient...!", m)
        chat_id = update.message.chat_id
        f = profile.get_followers()
        fl = profile.get_followees()
        flist = []
        fmlist = []
        for fn in f:
            u = fn.username
            flist.append(u)
        for fm in fl:
            n = fm.username
            fmlist.append(n)
        fans = [value for value in fmlist if value in flist]
        followers = f"**Fans List for {full_name}**\n\n"
        for p in fans:
            followers += f"\n[{p}](www.instagram.com/{p})"
        try:
            followers = f"**Fans List for {full_name}**\n\n"
            for p in fans:
                followers += f"\nName: {p}:Link to Profile: www.instagram.com/{p}"
            text_file = open(f"{username}'s_fans_list.txt", mode='w', encoding='utf-8')
            text_file.write(followers)
            text_file.close()
            deleteMessage(context.bot, m)
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s_fans_list.txt", 'rb'),
                              caption=f"<b>{full_name}'s fans</b>\n\n<b>Total Fans:</b> {len(fans)}\n\n<b>Total Followers:</b>  {len(flist)}\n\n<b>Total Following:</b>  {len(fmlist)}\n\n<b>Total Followers who follow {username}:</b>  {len(fans)}\n\nT<b>otal Following who follow {username}:</b> {len(flist)}",
                              parse_mode="HTML")
            os.remove(f"{username}'s_fans_list.txt")
            LOGGER.info(f"fans list of {full_name} removed")

        except Exception as e:
            LOGGER.error(e)
            editMessage(f"Error occurred: {e}", m)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def not_following(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        username = args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(
                    f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.",
                    m)
                
        profile = Profile.from_username(INSTA.context, username)
        full_name = profile.full_name
        editMessage(
            f"Fetching list of accounts who don't follow <code>@{username}</code>\n It may take few minutes, pls be patient...!",
            m)
        chat_id = update.message.chat_id
        f = profile.get_followers()
        fl = profile.get_followees()
        flist = []
        fmlist = []
        for fn in f:
            u = fn.username
            flist.append(u)
        for fm in fl:
            n = fm.username
            fmlist.append(n)

        fans = list(set(fmlist) - set(flist))

        try:
            followers = f"Following of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>\n\n"
            for p in fans:
                followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
            text_file = open(f"{username}'s_not_following_list.txt", mode='w', encoding='utf-8')
            text_file.write(followers)
            text_file.close()
            deleteMessage(context.bot, m)
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s_not_following_list.txt", 'rb'),
                              caption=f"<b>{full_name}'s Non_followers list</b>\n\n<b>Total Non_followers:</b> {len(fans)}\n\n<b>Total Followers:</b>  {len(flist)}\n\n<b>Total Following:</b>  {len(fmlist)}\n\n<b>Total Followers who follow {username}:</b>  {len(fans)}\n\n<b>Total Following who follow {username}:</b> {len(flist)}",
                              parse_mode="HTML")
            os.remove(f"{username}'s_not_following_list.txt")
            LOGGER.info("non_followers list removed")
        except Exception as e:
            LOGGER.error(e)
            editMessage(f"Error occurred: {e}", m)
    else:
        sendMessage("Please send a username...!", context.bot, update)


def feed(update, context):
    chat_id = update.message.chat_id
    USER = usercheck()
    session = f"./{USER}"
    args = update.message.text.split(" ", maxsplit=1)
    dir = f"{OWNER_ID}/{USER}"
    m = sendMessage("Checking the details, Please wait...!", context.bot, update)
    if len(args) > 1:
        if args[1].isdigit():
            count = args[1]
            if 1 not in STATUS:
                editMessage("You must /login ", m)
                
            editMessage(f"Fetching {count} posts from <code>@{USER}</code>'s feed.", m)
            editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.", m)
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
                ":feed",
                "--count", count
            ]

            download_insta(command, m, dir, USER, chat_id, fetch='My Feed')
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            editMessage("Please send a valid number...!", m)
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
            "--login", USER,
            "--sessionfile", session,
            "--dirname-pattern", dir,
            ":feed"
        ]
        download_insta(command, m, dir, USER, chat_id, fetch='My Feed')


def saved(update, context):
    chat_id = update.message.chat_id
    USER = usercheck()
    session = f"./{USER}"
    args = update.message.text.split(" ", maxsplit=1)
    dir = f"{OWNER_ID}/{USER}"
    m = sendMessage("Checking the details, Please wait...!", context.bot, update)
    if len(args) > 1:

        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        if args[1].isdigit():
            count = args[1]
            editMessage(f"Fetching {count} posts from saved.", m)
            editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.", m)
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
                ":saved",
                "--count", count
            ]
            download_insta(command, m, dir, USER, chat_id, fetch='My Saved')
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            editMessage("Please send a count...!", m)
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
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            ":saved"
        ]
        download_insta(command, m, dir, USER, chat_id, fetch='My Saved')


def tagged(update, context):
    chat_id = update.message.chat_id
    USER = usercheck()
    session = f"./{USER}"
    args = update.message.text.split(" ", maxsplit=1)
    dir = f"{OWNER_ID}/{USER}"
    m = sendMessage("Checking the details, please wait...!", context.bot, update)
    if len(args) > 1:
        username = args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"This account is private and you are not following {username}.", m)
                
        editMessage(f"Fetching posts from <code>@{username}</code>'s tagged", m)
        editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.", m)
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
    else:
        sendMessage("Please send a username...!", context.bot, update)


def story(update, context):
    chat_id = update.message.chat_id
    USER = usercheck()
    session = f"./{USER}"
    args = update.message.text.split(" ", maxsplit=1)
    m = sendMessage("Checking the details, please wait...!", context.bot, update)
    if len(args) > 1:
        username = args[1]
        dir = f"{OWNER_ID}/{username}"
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"This account is private and you are not following {username}.", m)
                
        editMessage(f"Fetching posts from <code>@{username}</code>'s story.", m)
        editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.", m)
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

    else:
        sendMessage("Please send a username...!", context.bot, update)


def stories(update, context):
    chat_id = update.message.chat_id
    USER = usercheck()
    session = f"./{USER}"
    username = USER
    dir = f"{OWNER_ID}/{username}"
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) < 1:
        m = sendMessage("Checking the details, Please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        editMessage(f"Fetching posts from your stories.", m)
        editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.", m)
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
        download_insta(command, m, dir, username, chat_id, fetch='My Following Stories')
    else:
        sendMessage("Please send command only..!", context.bot, update)


def highlights(update, context):
    chat_id = update.message.chat_id
    USER = usercheck()
    session = f"./{USER}"
    args = update.message.text.split(" ", maxsplit=1)

    if len(args) > 1:
        m = sendMessage("Checking the details, Please wait...!", context.bot, update)
        username = args[1]
        dir = f"{OWNER_ID}/{username}"
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            
        elif is_link(args[1]):
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(INSTA.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer)
            ac_type = acc_type(profile.is_private)
            if ac_type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"This account is private and you are not following {username}.", m)
                
        editMessage(f"Fetching posts from <code>@{username}</code>'s highlights.", m)
        editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.", m)
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
        download_insta(command, m, dir, username, chat_id, fetch=f'Highlights')
    else:
        sendMessage("Please send a username...!", context.bot, update)


post_handler = CommandHandler(BotCommands.IgPostCommand, post,
                              CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                              run_async=True)
dispatcher.add_handler(post_handler)

igtv_handler = CommandHandler(BotCommands.IgTvCommand, igtv,
                              CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                              run_async=True)
dispatcher.add_handler(igtv_handler)

followers_handler = CommandHandler(BotCommands.IgFollowersCommand, followers,
                                   CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                                   run_async=True)
dispatcher.add_handler(followers_handler)

followees_handler = CommandHandler(BotCommands.IgFollowingCommand, following,
                                   CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                                   run_async=True)
dispatcher.add_handler(followees_handler)

fans_handler = CommandHandler(BotCommands.IgFansCommand, fans,
                              CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                              run_async=True)
dispatcher.add_handler(fans_handler)

not_following_handler = CommandHandler(BotCommands.IgNotFollowingCommand, not_following,
                                       CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                                       run_async=True)
dispatcher.add_handler(not_following_handler)

feed_handler = CommandHandler(BotCommands.IgFeedCommand, feed,
                              CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                              run_async=True)
dispatcher.add_handler(feed_handler)

saved_handler = CommandHandler(BotCommands.IgSavedCommand, saved,
                               CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                               run_async=True)
dispatcher.add_handler(saved_handler)

tagged_handler = CommandHandler(BotCommands.IgTaggedCommand, tagged,
                                CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                                run_async=True)
dispatcher.add_handler(tagged_handler)

story_handler = CommandHandler(BotCommands.IgStoryCommand, story,
                               CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                               run_async=True)
dispatcher.add_handler(story_handler)

stories_handler = CommandHandler(BotCommands.IgStoriesCommand, stories,
                                 CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                                 run_async=True)
dispatcher.add_handler(stories_handler)

highlights_handler = CommandHandler(BotCommands.IgHighlightsCommand, highlights,
                                    CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,
                                    run_async=True)
dispatcher.add_handler(highlights_handler)
