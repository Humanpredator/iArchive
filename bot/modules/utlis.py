import re
from bot.helper.ext_utils.bot_utils import usercheck,acc_type, yes_or_no
from instaloader import Profile
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher,L,STATUS
from bot.helper.telegram_helper.bot_commands import BotCommands
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.helper.down_utilis.insta_down import download_insta



insta = L

def account(update, context):
    USER=usercheck()
    session=f"./{USER}"
    if 1 in STATUS:
        m=sendMessage("Getting Your data", context.bot, update)
        try:
            profile = Profile.own_profile(insta.context)
            mediacount = profile.mediacount
            name = profile.full_name
            bio = profile.biography
            profilepic = profile.profile_pic_url
            username = profile.username
            igtvcount = profile.igtvcount
            followers = profile.followers
            following = profile.followees
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Download My Profile Pic", callback_data=f"ppic#{username}"),
                        InlineKeyboardButton("Go To Profile", url=f'https://www.instagram.com/{username}')       
                    ],
                    [
                        InlineKeyboardButton("My Post", callback_data=f"post#{username}"),
                        InlineKeyboardButton("My Tagged Posts", callback_data=f"tagged#{username}"),
                        InlineKeyboardButton("Posts In My Feed", callback_data=f"feed#{username}")
                    ],
                    [
                        
                        InlineKeyboardButton("My Saved Posts", callback_data=f"saved#{username}"),
                        InlineKeyboardButton("My IGTV Posts", callback_data=f"igtv#{username}")
                    ],
                    [
                        
                        InlineKeyboardButton("My Highlights", callback_data=f"highlights#{username}"),
                        InlineKeyboardButton("My Stories ", callback_data=f"stories#{username}"),
                        InlineKeyboardButton("Stories of My Followees", callback_data=f"fstories#{username}")
                    ],

                    [
                        InlineKeyboardButton("List Of My Followers", callback_data=f"followers#{username}"),
                        InlineKeyboardButton("List Of My Followees", callback_data=f"followees#{username}")
                    ]
                ]
                )
            deleteMessage(context.bot, m)
            bot.send_photo(
                chat_id=update.message.chat.id,
                photo=profilepic,
                caption=f"You are already Logged In as {name}\n\n<b>Your Account Details</b>\n\n🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n📸 <b>Total Posts</b>: {mediacount}\n📺 <b>IGTV Videos</b>: {igtvcount}",parse_mode="HTML",
                reply_markup=reply_markup
                )
        except Exception as e:
            editMessage(f"Error: {e}", context.bot, m)

    else:
        sendMessage("You must login first by /login", context.bot, update)

#get Ig user Data 

def mirror(update, context):
    USER=usercheck()
    session=f"./{USER}"
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1:
        username=args[1]   
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        m = sendMessage("Fetching data from Instagram🔗",context.bot, update)

        if "https://instagram.com/stories/" in username:
            msg="Stories from links are not yet supported🥴\n\nYou can download stories from Username."
            editMessage(msg, m)
            return
        
        link = r'^https://www\.instagram\.com/([A-Za-z0-9._]+/)?(p|tv|reel)/([A-Za-z0-9\-_]*)'
        result = re.search(link, username)
        
        if result:
            Post_type = {
                'p': 'POST',
                'tv': 'IGTV',
                'reel': 'REELS'
            }
            supported = Post_type.get(result.group(2))
            if not supported:
                msg="This link is not supported yet.\n\nSupported links are:\n\n<b>POST</b> - https://www.instagram.com/p/<code>post_id</code>\n<b>IGTV</b> - https://www.instagram.com/tv/<code>post_id</code>\n<b>REELS</b> - https://www.instagram.com/reel/<code>post_id</code>"
                editMessage(msg, m)
                return
            deleteMessage(context.bot, m)
            m = sendMessage(f'Fetching {supported} Content from Instagram.',context.bot, update)
            shortcode = result.group(3)
            try:
                dir='Downloads'
                chat_id= update.message.chat.id
                command = [
                    "instaloader",
                    "--no-metadata-json",
                    "--no-compress-json",
                    "--no-captions",
                    "--no-video-thumbnails",
                    "--filename-pattern={profile}_UTC_{date_utc}",
                    "--dirname-pattern", dir,
                    "--login", USER,
                    "-f", session,
                    "--", f"-{shortcode}"
                    ]
                download_insta(command, m, dir,username,fetch='posts')
            except Exception as e:
                print(e)
                sendMessage(f"Error: {e}", context.bot, update)
                pass
        else:
            msg= "Unsupported Format"
            editMessage(msg, m)
            return

    else:
        sendMessage("send insta posts links after /mirror ", context.bot, update)
       
def ig(update, context):
    args=update.message.text.split(" ", maxsplit=1)
    if len(args)>1: 
        if 1 not in STATUS:
            sendMessage("You Must Login First /login ", context.bot, update)
            return
        username=args[1]
        m = sendMessage("Fetching data from Instagram🔗",context.bot, update)
        if 'https://' in username:
            username=re.split("[/?]",username)[3]
            msg=f"Fetching details for <code>@{username}</code>\nWait for a while🔗"
            editMessage(msg, m)
            try:
                profile = Profile.from_username(insta.context, username)
                mediacount = profile.mediacount
                name = profile.full_name
                profilepic = profile.profile_pic_url
                igtvcount = profile.igtvcount
                bio = profile.biography
                followers = profile.followers
                following = profile.followees
                is_followed = yes_or_no(profile.followed_by_viewer) 
                is_following = yes_or_no(profile.follows_viewer)
                type = acc_type(profile.is_private)
                if type == "🔒Private🔒" and is_followed == "No":
                    print("reached")
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Download Profile Pic", callback_data=f"ppic#{username}"),
                                InlineKeyboardButton("Go To Profile", url=f'https://www.instagram.com/{username}')
                            ]
                        ]
                    )
                else:
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Profile Pic", callback_data=f"ppic#{username}"),
                                InlineKeyboardButton("Go To Profile", url=f'https://www.instagram.com/{username}')
                            ],
                            [
                                InlineKeyboardButton("All Post", callback_data=f"post#{username}"),
                                InlineKeyboardButton("All Tagged Posts", callback_data=f"tagged#{username}")
                            ],
                            [
                                InlineKeyboardButton("All IGTV", callback_data=f"igtv#{username}"),
                                InlineKeyboardButton("Stories ", callback_data=f"stories#{username}"),
                                InlineKeyboardButton("Highlights", callback_data=f"highlights#{username}")
                            ],
                            [
                                InlineKeyboardButton(f"{name}'s Followers", callback_data=f"followers#{username}"),
                                InlineKeyboardButton(f"{name}'s Followees", callback_data=f"followees#{username}")
                            ]
                        ]
                    )
                deleteMessage(context.bot, m)
                try:
                    bot.send_photo(
                        chat_id=update.message.chat.id,
                        photo=profilepic,
                        caption=f"🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n<b>👤 Is {name} Following You?</b>: {is_following}\n<b>👤 Is You Following {name} </b>: {is_followed}\n📸 <b>Total Posts</b>: {mediacount}\n📺 <b>IGTV Videos</b>: {igtvcount}",parse_mode="HTML",
                        reply_markup=reply_markup
                    )
                except Exception as e:
                    print(e)
                    editMessage(e, m)
            except Exception as e:
                print(e)
                editMessage(e, m)
                pass
        else:
            msg=f"Fetching details for <code>@{username}</code>\nWait for a while🔗"
            editMessage(msg, m)
            try:
                profile = Profile.from_username(insta.context, username)
                mediacount = profile.mediacount
                name = profile.full_name
                profilepic = profile.profile_pic_url
                igtvcount = profile.igtvcount
                bio = profile.biography
                followers = profile.followers
                following = profile.followees
                is_followed = yes_or_no(profile.followed_by_viewer) 
                is_following = yes_or_no(profile.follows_viewer)
                type = acc_type(profile.is_private)
                if type == "🔒Private🔒" and is_followed == "No":
                    print("reached")
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Download Profile Pic", callback_data=f"ppic#{username}"),
                                InlineKeyboardButton("Go To Profile", url=f'https://www.instagram.com/{username}')
                            ]
                        ]
                    )
                else:
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Profile Pic", callback_data=f"ppic#{username}"),
                                InlineKeyboardButton("Go To Profile", url=f'https://www.instagram.com/{username}')
                            ],
                            [
                                InlineKeyboardButton("All Post", callback_data=f"post#{username}"),
                                InlineKeyboardButton("All Tagged Posts", callback_data=f"tagged#{username}")
                            ],
                            [
                                InlineKeyboardButton("All IGTV", callback_data=f"igtv#{username}"),
                                InlineKeyboardButton("Stories ", callback_data=f"stories#{username}"),
                                InlineKeyboardButton("Highlights", callback_data=f"highlights#{username}")
                            ],
                            [
                                InlineKeyboardButton(f"{name}'s Followers", callback_data=f"followers#{username}"),
                                InlineKeyboardButton(f"{name}'s Followees", callback_data=f"followees#{username}")
                            ]
                        ]
                    )
                deleteMessage(context.bot, m)
                try:
                    bot.send_photo(
                        chat_id=update.message.chat.id,
                        photo=profilepic,
                        caption=f"🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n<b>👤 Is {name} Following You?</b>: {is_following}\n<b>👤 Is You Following {name} </b>: {is_followed}\n📸 <b>Total Posts</b>: {mediacount}\n📺 <b>IGTV Videos</b>: {igtvcount}",parse_mode="HTML",
                        reply_markup=reply_markup
                    )
                except Exception as e:
                    print(e)
                    editMessage(e, m)
            except Exception as e:
                print(e)
                editMessage(e, m)
                pass
    else:
        sendMessage("send username or profile link /ig ", context.bot, update)       



account_handler = CommandHandler(BotCommands.IgAccountCommand, account, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
dispatcher.add_handler(account_handler)

iglink_handler = CommandHandler(BotCommands.IgSearchCommand, ig, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,  run_async=True)
dispatcher.add_handler(iglink_handler)

mirrorlink_handler = CommandHandler(BotCommands.IgMirrorCommand, mirror, CustomFilters.authorized_chat | CustomFilters.owner_filter | CustomFilters.authorized_user,  run_async=True)
dispatcher.add_handler(mirrorlink_handler)
