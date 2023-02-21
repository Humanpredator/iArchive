import re

from instaloader import Profile
from telegram import InlineKeyboardButton
from telegram.ext import CommandHandler

from bot import INSTA, OWNER_ID, STATUS, dispatcher
from bot.helper.down_utilis.insta_down import download_insta
from bot.helper.ext_utils.bot_utils import acc_type, usercheck, yes_or_no
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import *


def account(update, context):
    if 1 in STATUS:
        m = sendMessage("Getting your data, please wait...!",
                        context.bot, update)
        profile = Profile.own_profile(INSTA.context)
        media_count = profile.mediacount
        name = profile.full_name
        bio = profile.biography
        ppic = profile.profile_pic_url
        username = profile.username
        igtv_count = profile.igtvcount
        followers = profile.followers
        following = profile.followees
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Download My Profile Pic", callback_data=f"ppic#{username}"
                    ),
                    InlineKeyboardButton(
                        "Go To Profile", url=f"https://www.instagram.com/{username}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "My Post", callback_data=f"post#{username}"),
                    InlineKeyboardButton(
                        "My Tagged Posts", callback_data=f"tagged#{username}"
                    ),
                    InlineKeyboardButton(
                        "Posts In My Feed", callback_data=f"feed#{username}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "My Saved Posts", callback_data=f"saved#{username}"
                    ),
                    InlineKeyboardButton(
                        "My IGTV Posts", callback_data=f"igtv#{username}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "My Highlights", callback_data=f"highlights#{username}"
                    ),
                    InlineKeyboardButton(
                        "My Stories ", callback_data=f"stories#{username}"
                    ),
                    InlineKeyboardButton(
                        "Stories of My Following", callback_data=f"fstories#{username}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "List Of My Followers", callback_data=f"followers#{username}"
                    ),
                    InlineKeyboardButton(
                        "List Of My Following", callback_data=f"following#{username}"
                    ),
                ],
            ]
        )
        bot.delete_message(chat_id=update.message.chat.id,
                           message_id=m.message_id)
        bot.send_photo(
            chat_id=update.message.chat_id,
            photo=ppic,
            caption=f"You are already logged in as {name}\n\n<b>Your Account Details</b>\n\n🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n📸 <b>Total Posts</b>: {media_count}\n📺 <b>IGTV Videos</b>: {igtv_count}",
            parse_mode="HTML",
            reply_markup=reply_markup,
        )
    else:
        sendMessage("You must /login", context.bot, update)


def mirror(update, context):
    USER = usercheck()
    session = f"./{USER}"
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        m = sendMessage(
            "Checking given details, please wait...!", context.bot, update)
        username = args[1]
        if 1 not in STATUS:
            editMessage("You must /login", m)
            return
        editMessage("Fetching data from Instagram🔗...!", m)
        if "https://instagram.com/stories/" in username:
            msg = "Stories from links are not yet supported🥴\n\nYou can download stories from Username."
            editMessage(msg, m)
            return
        link = r"^https://www\.instagram\.com/([A-Za-z0-9._]+/)?(p|tv|reel)/([A-Za-z0-9\-_]*)"
        result = re.search(link, username)
        if result:
            Post_type = {"p": "POST", "tv": "IGTV", "reel": "REELS"}
            supported = Post_type.get(result.group(2))
            if not supported:
                msg = "This link is not supported yet.\n\nSupported links are:\n\n<b>POST</b> - https://www.instagram.com/p/<code>post_id</code>\n<b>IGTV</b> - https://www.instagram.com/tv/<code>post_id</code>\n<b>REELS</b> - https://www.instagram.com/reel/<code>post_id</code>"
                editMessage(msg, m)
                return
            editMessage(f"Fetching {supported} content from Instagram.", m)
            shortcode = result.group(3)
            try:
                dir = f"{OWNER_ID}/Downloads"
                chat_id = update.message.chat.id
                command = [
                    "instaloader",
                    "--no-metadata-json",
                    "--no-compress-json",
                    "--no-captions",
                    "--no-video-thumbnails",
                    "--filename-pattern={profile}_UTC_{date_utc}",
                    "--dirname-pattern",
                    dir,
                    "--login",
                    USER,
                    "-f",
                    session,
                    "--",
                    f"-{shortcode}",
                ]
                download_insta(command, m, dir, username,
                               chat_id, fetch="posts")
            except Exception as e:
                LOGGER.error(e)
                editMessage(f"Error Occurred: {e}", m)
        else:
            msg = "Unsupported Format"
            editMessage(msg, m)
            return
    else:
        sendMessage("Send insta post links after /mirror ",
                    context.bot, update)


def ig(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        m = sendMessage(
            "Checking given details, please wait...!", context.bot, update)
        if 1 not in STATUS:
            editMessage("You must /login", m)
            return
        username = args[1]
        editMessage("Fetching data from Instagram🔗...!", m)
        if "https://" in username:
            username = re.split("[/?]", username)[3]
            msg = f"Fetching details for <code>@{username}</code>\nWait for a while🔗"
            editMessage(msg, m)
            try:
                profile = Profile.from_username(INSTA.context, username)
                media_count = profile.mediacount
                name = profile.full_name
                ppic = profile.profile_pic_url
                igtv_count = profile.igtvcount
                bio = profile.biography
                followers = profile.followers
                following = profile.followees
                is_followed = yes_or_no(profile.followed_by_viewer)
                is_following = yes_or_no(profile.follows_viewer)
                ac_type = acc_type(profile.is_private)
                if ac_type == "🔒Private🔒" and is_followed == "No":
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Download Profile Pic",
                                    callback_data=f"ppic#{username}",
                                ),
                                InlineKeyboardButton(
                                    "Go To Profile",
                                    url=f"https://www.instagram.com/{username}",
                                ),
                            ]
                        ]
                    )
                else:
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Profile Pic", callback_data=f"ppic#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Go To Profile",
                                    url=f"https://www.instagram.com/{username}",
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "All Post", callback_data=f"post#{username}"
                                ),
                                InlineKeyboardButton(
                                    "All Tagged Posts",
                                    callback_data=f"tagged#{username}",
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "All IGTV", callback_data=f"igtv#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Stories ", callback_data=f"stories#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Highlights", callback_data=f"highlights#{username}"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    f"{name}'s Followers",
                                    callback_data=f"followers#{username}",
                                ),
                                InlineKeyboardButton(
                                    f"{name}'s Following",
                                    callback_data=f"following#{username}",
                                ),
                            ],
                        ]
                    )
                deleteMessage(context.bot, m)
                try:
                    bot.send_photo(
                        chat_id=update.message.chat.id,
                        photo=ppic,
                        caption=f"🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n<b>👤 Is {name} Following You?</b>: {is_following}\n<b>👤 Is You Following {name} </b>: {is_followed}\n📸 <b>Total Posts</b>: {media_count}\n📺 <b>IGTV Videos</b>: {igtv_count}",
                        parse_mode="HTML",
                        reply_markup=reply_markup,
                    )
                except Exception as e:
                    LOGGER.error(e)
                    editMessage(f"Error Occurred: {e}", m)
            except Exception as e:
                LOGGER.error(e)
                editMessage(f"Error Occurred: {e}", m)
        else:
            msg = f"Fetching details for <code>@{username}</code>\nWait for a while🔗"
            editMessage(msg, m)
            try:
                profile = Profile.from_username(INSTA.context, username)
                media_count = profile.mediacount
                name = profile.full_name
                ppic = profile.profile_pic_url
                igtv_count = profile.igtvcount
                bio = profile.biography
                followers = profile.followers
                following = profile.followees
                is_followed = yes_or_no(profile.followed_by_viewer)
                is_following = yes_or_no(profile.follows_viewer)
                ac_type = acc_type(profile.is_private)
                if ac_type == "🔒Private🔒" and is_followed == "No":
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Download Profile Pic",
                                    callback_data=f"ppic#{username}",
                                ),
                                InlineKeyboardButton(
                                    "Go To Profile",
                                    url=f"https://www.instagram.com/{username}",
                                ),
                            ]
                        ]
                    )
                else:
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Profile Pic", callback_data=f"ppic#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Go To Profile",
                                    url=f"https://www.instagram.com/{username}",
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "All Post", callback_data=f"post#{username}"
                                ),
                                InlineKeyboardButton(
                                    "All Tagged Posts",
                                    callback_data=f"tagged#{username}",
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "All IGTV", callback_data=f"igtv#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Stories ", callback_data=f"stories#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Highlights", callback_data=f"highlights#{username}"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    f"{name}'s Followers",
                                    callback_data=f"followers#{username}",
                                ),
                                InlineKeyboardButton(
                                    f"{name}'s Following",
                                    callback_data=f"following#{username}",
                                ),
                            ],
                        ]
                    )
                deleteMessage(context.bot, m)
                try:
                    bot.send_photo(
                        chat_id=update.message.chat.id,
                        photo=ppic,
                        caption=f"🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n<b>👤 Is {name} Following You?</b>: {is_following}\n<b>👤 Is You Following {name} </b>: {is_followed}\n📸 <b>Total Posts</b>: {media_count}\n📺 <b>IGTV Videos</b>: {igtv_count}",
                        parse_mode="HTML",
                        reply_markup=reply_markup,
                    )
                except Exception as e:
                    LOGGER.error(e)
                    editMessage(f"Error Occurred: {e}", m)
            except Exception as e:
                LOGGER.error(e)
                editMessage(f"Error Occurred: {e}", m)
    else:
        sendMessage("Send username or profile link /ig ", context.bot, update)


account_handler = CommandHandler(
    BotCommands.IgAccountCommand,
    account,
    filters=CustomFilters.owner_filter | CustomFilters.sudo_user,
    run_async=True,
)
dispatcher.add_handler(account_handler)

iglink_handler = CommandHandler(
    BotCommands.IgSearchCommand,
    ig,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(iglink_handler)

mirrorlink_handler = CommandHandler(
    BotCommands.IgMirrorCommand,
    mirror,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(mirrorlink_handler)
