
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


#post handler
def post(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            username=args[1] 
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.", context.bot, update)
                return
            else:
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Pictures Only", callback_data=f"photos#{username}"),
                            InlineKeyboardButton("Videos Only", callback_data=f"videos#{username}")
                        ],
                        [
                            InlineKeyboardButton("Pic+vid", callback_data=f"picandvid#{username}"),
                            InlineKeyboardButton("ALL Posts", callback_data=f"allposts#{username}"),
                        ]
                    ]
                )
                sendMarkup("Select the type of posts you want to fetch", context.bot, update, reply_markup=reply_markup)
    else:
        sendMessage("Please send a username", context.bot, update)


#igtv handler
def igtv(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ")
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            username=args[1]
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.", context.bot, update)
                return
        m = sendMessage(f"Fetching IGTV from <code>@{username}</code>", context.bot, update)
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
        editMessage(f"Do you Want to download all IGTV posts?\nThere are {igtvcount} posts.", context.bot, update, m, reply_markup=reply_markup)
    else:
        sendMessage("Please send a username", context.bot, update)
    


#followers handler
def followers(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            username=args[1]
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.", context.bot, update)
                return
        profile = Profile.from_username(insta.context, username)
        name=profile.full_name
        m=sendMessage(f"Fetching Followers list of <code>@{username}</code>\n It may take few minutes, pls be patient...!" , context.bot, update)
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
            sendMessage("Error Occured", context.bot, update)
    else:
        sendMessage("Please send a username", context.bot, update)

#followings handler
def following(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            username=args[1]
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.", context.bot, update)
                return
        profile = Profile.from_username(insta.context, username)
        name=profile.full_name
        m= sendMessage(f"Fetching Following list of <code>@{username}</code>\n It may take few minutes, pls be patient...!" , context.bot, update)
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
            sendMessage("Error Occured", context.bot, update)
    else:
        sendMessage("Please send a username", context.bot, update)




def fans(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        username=args[1]
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.", context.bot, update)
                return
        profile = Profile.from_username(insta.context, username)
        name=profile.full_name
        m=sendMessage(f"Fetching Fans list of <code>@{username}</code>\n It may take few minutes, pls be patient...!" , context.bot, update)
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
            sendMessage("Error Occured", context.bot, update)
    else:
        sendMessage("Please send a username", context.bot, update)



def notfollowing(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        username=args[1]
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.", context.bot, update)
                return
        profile = Profile.from_username(insta.context, username)
        name=profile.full_name
        m=sendMessage(f"Fetching list of accounts who don't follow <code>@{username}</code>\n It may take few minutes, pls be patient...!", context.bot, update)
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
            sendMessage("Error Occured", context.bot, update)
    else:
        sendMessage("Please send a username", context.bot, update)





def feed(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    username=USER
    count=None
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        if args[1].isdigit():
            count=int(args[1])
            if 1 not in STATUS:
                sendMessage("You Must Login First /login ", context.bot, update)
                return
            m=sendMessage(f"Fetching {count} posts from <code>@{username}</code>'s feed.", context.bot, update)
            editMessage("Starting Downloading..\nThis may take longer time Depending upon number of posts.",m)
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
            download_insta(command, m, dir,username,fetch='My Feed')
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            sendMessage("Please send a number", context.bot, update)
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
        download_insta(command, m, dir,username,fetch='My Feed')




def saved(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        count=None
        if args[1].isdigit():
            count=int(args[1])
            username=USER
            m=sendMessage(f"Fetching {count} posts from <code>@{username}</code>'s saved.", context.bot, update)
            editMessage("Starting Downloading..\nThis may take longer time Depending upon number of posts.",m)
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
            download_insta(command, m, dir,username,fetch='My Saved')
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            sendMessage("Please send a number", context.bot, update)
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
        download_insta(command, m, dir,username,fetch='My Saved')






def tagged(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        username=args[1]
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"This account is private and you are not following {username}.", context.bot, update)
                return
        m=sendMessage(f"Fetching posts from <code>@{username}</code>'s tagged.", context.bot, update)
        editMessage("Starting Downloading..\nThis may take longer time Depending upon number of posts.",m)
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
        download_insta(command, m, dir,username,fetch='Tagged')

    else:
        sendMessage("Please send a username.", context.bot, update)




def story(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        username=args[1]
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:
            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"This account is private and you are not following {username}.", context.bot, update)
                return
        m=sendMessage(f"Fetching posts from <code>@{username}</code>'s story.", context.bot, update)
        editMessage("Starting Downloading..\nThis may take longer time Depending upon number of posts.",m)
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
        download_insta(command, m, dir,username,fetch='Stories')      

    else:
        sendMessage("Please send a username.", context.bot, update)



def stories(update, context):
    USER=usercheck()
    session=f"./{USER}"
    username=USER
    dir=f"{OWNER_ID}/{username}"
    if 1 not in STATUS:
        sendMessage("You Must Login First /login ", context.bot, update)
        return
    m=sendMessage(f"Fetching posts from <code>@{username}</code>'s stories.", context.bot, update)
    editMessage("Starting Downloading..\nThis may take longer time Depending upon number of posts.",m)
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
    download_insta(command, m, dir,username,fetch='My Following Stories')








def highlights(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    dir=f"{OWNER_ID}/{username}"
    if len(args)>1:
        username=args[1]
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        elif is_link(args[1])==True:
            sendMessage("Please send a username not link use /ig <b>link</b> ", context.bot, update)
        else:

            profile = Profile.from_username(insta.context, username)
            is_followed = yes_or_no(profile.followed_by_viewer) 
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                sendMessage(f"This account is private and you are not following {username}.", context.bot, update)
                return
        m=sendMessage(f"Fetching posts from <code>@{username}</code>'s highlights.", context.bot, update)
        editMessage("Starting Downloading..\nThis may take longer time Depending upon number of posts.",m)
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
        download_insta(command, m, dir,username,fetch=f'Highlights')
    else:
        sendMessage("Please send a username.", context.bot, update)



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