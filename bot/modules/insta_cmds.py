from instaloader import Profile
from bot.helper.down_utilis.insta_down import download_insta
from bot.helper.ext_utils.bot_utils import usercheck,acc_type,is_link, yes_or_no
import os
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher,OWNER_ID,L,STATUS
from bot.helper.telegram_helper.bot_commands import BotCommands
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
insta = L

def post(update, context):
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            username=args[1] 
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.", m)
                return
            else:
                reply_markup=InlineKeyboardMarkup(
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
                return
    else:
        sendMessage("Please send a username...!", context.bot, update)

def igtv(update, context):
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must login  /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            username=args[1]
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.", m)
                return
        editMessage(f"Fetching IGTV from <code>@{username}</code>", m)
        profile = Profile.from_username(insta.context, username)
        igtvcount = profile.igtvcount
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Yes", callback_data=f"yes#{username}"),
                        InlineKeyboardButton("No", callback_data=f"no#{username}")
                    ]
                ]
            )
        editMessage(f"Do you want to download all IGTV posts?\nThere are {igtvcount} posts.", m, reply_markup=reply_markup)
    else:
        sendMessage("Please send a username...!", context.bot, update)
    
def followers(update, context):
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            username=args[1]
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.", m)
                return
        profile = Profile.from_username(insta.context, username)
        name=profile.full_name
        editMessage(f"Fetching followers list of <code>@{username}</code>\n It may take few minutes, pls be patient...!" , m)
        chat_id=update.message.chat_id
        try:
            followers=f"**Followers List for {name}**\n\n"
            f = profile.get_followers()
            for p in f:
                followers += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s followers.txt", "w")
            text_file.write(followers)
            text_file.close()
            deleteMessage(context.bot, m)
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s followers.txt", 'rb'),caption=f"<b>{name}'s followers</b>", parse_mode='HTML')
            os.remove(f"./{username}'s followers.txt")
            LOGGER.info("followers list removed")
        except:
            editMessage("Error occured, try again...!", context.bot, update, m)
    else:
        sendMessage("Please send a username...!", context.bot, update)

def following(update, context):
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            username=args[1]
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.", m)
                return
        profile = Profile.from_username(insta.context, username)
        name=profile.full_name
        editMessage(f"Fetching following list of <code>@{username}</code>\n It may take few minutes, pls be patient...!", m)
        chat_id=update.message.chat_id
        try :
            followees=f"**Following List for {name}**\n\n"
            f = profile.get_followees()
            for p in f:
                followees += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s following.txt", "w")
            text_file.write(followees)
            text_file.close()
            deleteMessage(context.bot, m)
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s following.txt", 'rb'),caption=f"<b>{name}'s following</b>", parse_mode='HTML')
            os.remove(f"./{username}'s following.txt")
            LOGGER.info("following list removed")
        except:
            editMessage("Error occured, try again...!", m)
    else:
        sendMessage("Please send a username...!", context.bot, update)

def fans(update, context):
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        username=args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.", m)
                return
        profile = Profile.from_username(insta.context, username)
        name=profile.full_name
        editMessage(f"Fetching fans list of <code>@{username}</code>\n It may take few minutes, pls be patient...!", m)
        chat_id=update.message.chat_id
        f = profile.get_followers()
        fl = profile.get_followees()
        flist=[]
        fmlist=[]
        for fn in f:
            u=fn.username
            flist.append(u)
        for fm in fl:
            n=fm.username
            fmlist.append(n)
        fans = [value for value in fmlist if value in flist]
        followers=f"**Fans List for {name}**\n\n"
        for p in fans:
            followers += f"\n[{p}](www.instagram.com/{p})"
        try:
            followers=f"**Fans List for {name}**\n\n"
            for p in fans:
                followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
            text_file = open(f"{username}'s fans.txt", "w")
            text_file.write(followers)
            text_file.close()
            deleteMessage(context.bot, m)
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s fans.txt", 'rb'),caption=f"<b>{name}'s fans</b>\n\n<b>Total Fans:</b> {len(fans)}\n\n<b>Total Followers:</b>  {len(flist)}\n\n<b>Total Following:</b>  {len(fmlist)}\n\n<b>Total Followers who follow {username}:</b>  {len(fans)}\n\nT<b>otal Following who follow {username}:</b> {len(flist)}",parse_mode="HTML")
            os.remove(f"./{username}'s fans.txt")
            LOGGER.info("fans list removed")
            
        except:
            editMessage("Error occured, try again...!",m)
    else:
        sendMessage("Please send a username...!", context.bot, update)

def notfollowing(update, context):
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        m = sendMessage("Checking the given username, please wait...!", context.bot, update)
        username=args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a private account and you are not following <code>@{username}</code>.", m)
                return
        profile = Profile.from_username(insta.context, username)
        name=profile.full_name
        editMessage(f"Fetching list of accounts who don't follow <code>@{username}</code>\n It may take few minutes, pls be patient...!", m)
        chat_id=update.message.chat_id
        f = profile.get_followers()
        fl = profile.get_followees()
        flist=[]
        fmlist=[]
        for fn in f:
            u=fn.username
            flist.append(u)
        for fm in fl:
            n=fm.username
            fmlist.append(n)

        fans = list(set(fmlist) - set(flist))
        print(len(fans))
        try:
            followers=f"Following of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>\n\n"
            for p in fans:
                followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
            text_file = open(f"{username}'s Non_followers.txt", "w")
            text_file.write(followers)
            text_file.close()
            deleteMessage(context.bot, m)
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s Non_followers.txt", 'rb'),caption=f"<b>{name}'s Non_followers list</b>\n\n<b>Total Non_followers:</b> {len(fans)}\n\n<b>Total Followers:</b>  {len(flist)}\n\n<b>Total Following:</b>  {len(fmlist)}\n\n<b>Total Followers who follow {username}:</b>  {len(fans)}\n\nT<b>otal Following who follow {username}:</b> {len(flist)}",parse_mode="HTML")
            os.remove(f"./{username}'s Non_followers.txt")
            LOGGER.info("non_followers list removed")
        except:
            editMessage("Error occured, try again...!", m)
    else:
        sendMessage("Please send a username...!", context.bot, update)

def feed(update, context):
    chat_id = update.message.chat_id
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    username=USER
    count=None
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        m = sendMessage("Checking the details, Please wait...!", context.bot, update)
        if args[1].isdigit():
            count= args[1]
            if 1 not in STATUS:
                editMessage("You must /login ", m)
                return
            editMessage(f"Fetching {count} posts from <code>@{username}</code>'s feed.", m)
            editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.",m)
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

            download_insta(command, m, dir,username ,chat_id,fetch='My Feed')
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            editMessage("Please send a count...!", context.bot, update, m)
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
        download_insta(command, m, dir,username,chat_id,fetch='My Feed')

def saved(update, context):
    chat_id = update.message.chat_id
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        m = sendMessage("Checking the details, Please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        if args[1].isdigit():
            count=args[1]
            username=USER
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
            download_insta(command, m, dir,username,chat_id,fetch='My Saved')
        elif is_link(args[1])==True:
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
        download_insta(command, m, dir,username,chat_id,fetch='My Saved')

def tagged(update, context):
    chat_id = update.message.chat_id
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        m = sendMessage("Checking the details, please wait...!", context.bot, update)
        username=args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"This account is private and you are not following {username}.", m)
                return
        editMessage(f"Fetching posts from <code>@{username}</code>'s tagged", m)
        editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.",m)
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
        download_insta(command, m, dir,username,chat_id,fetch='Tagged')
    else:
        sendMessage("Please send a username...!", context.bot, update)

def story(update, context):
    chat_id = update.message.chat_id
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        m = sendMessage("Checking the details, please wait...!", context.bot, update)
        username=args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"This account is private and you are not following {username}.", m)
                return
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
        download_insta(command, m, dir,username,chat_id,fetch='Stories')      

    else:
        sendMessage("Please send a username...!", context.bot, update)

def stories(update, context):
    chat_id = update.message.chat_id
    USER=usercheck()
    session=f"./{USER}"
    username=USER
    dir=f"{OWNER_ID}/{username}"
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)<1:
        m = sendMessage("Checking the details, Please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return 
        editMessage(f"Fetching posts from your stories.", m)
        editMessage("Starting downloading..\nThis may take longer time depending upon number of posts.",m)
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
        download_insta(command, m, dir,username,chat_id,fetch='My Following Stories')
    else:
        sendMessage("Please send command only..!", context.bot, update)


def highlights(update, context):
    chat_id = update.message.chat_id
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        m = sendMessage("Checking the details, Please wait...!", context.bot, update)
        username=args[1]
        if 1 not in STATUS:
            editMessage("You must /login ", m)
            return
        elif is_link(args[1])==True:
            editMessage("Please send a username only...!", m)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                editMessage(f"This account is private and you are not following {username}.", m)
                return
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
        download_insta(command, m, dir,username,chat_id,fetch=f'Highlights')
    else:
        sendMessage("Please send a username...!", context.bot, update)



post_handler = CommandHandler(BotCommands.IgPostCommand, post, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(post_handler)

igtv_handler = CommandHandler(BotCommands.IgTvCommand, igtv, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(igtv_handler)

followers_handler = CommandHandler(BotCommands.IgFollowersCommand, followers, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(followers_handler)

followees_handler = CommandHandler(BotCommands.IgFollowingCommand, following, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(followees_handler)

fans_handler = CommandHandler(BotCommands.IgFansCommand, fans, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(fans_handler)

nonfollowing_handler = CommandHandler(BotCommands.IgNotFollowingCommand, notfollowing, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(nonfollowing_handler)

feed_handler = CommandHandler(BotCommands.IgFeedCommand, feed, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(feed_handler)

saved_handler = CommandHandler(BotCommands.IgSavedCommand, saved, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(saved_handler)

tagged_handler = CommandHandler(BotCommands.IgTaggedCommand, tagged, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(tagged_handler)

story_handler = CommandHandler(BotCommands.IgStoryCommand, story, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(story_handler)

stories_handler = CommandHandler(BotCommands.IgStoriesCommand, stories, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(stories_handler)

highlights_handler = CommandHandler(BotCommands.IgHighlightsCommand, highlights, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(highlights_handler)