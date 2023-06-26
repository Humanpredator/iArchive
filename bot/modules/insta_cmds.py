"""InstaDL-Bot, Telegram Bot to download Instagram Posts and Reels"""

from instaloader import Profile
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler

from bot import INSTA, STATUS, dispatcher, bot
from bot.helper.ext_utils.bot_utils import is_link, allow_access
from bot.helper.ig_utils.ig_down import download_content, check_username, download_highlights, download_stories, \
    fetch_followers, fetch_following, mutual_follow, download_tagged, download_feed, download_saved, \
    download_following_stories
from bot.helper.tg_utils.bot_commands import BotCommands
from bot.helper.tg_utils.filters import CustomFilters
from bot.helper.tg_utils.message_utils import sendMessage, editMessage, deleteMessage


def my_account(update, context):
    if 1 not in STATUS:
        sendMessage(f"You must /{BotCommands.LoginCommand}", context.bot, update)
        return
    msg = sendMessage(
        f"Checking Given Details...!, Please Wait...!", context.bot, update
    )

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
                    "Download My Profile Pic", callback_data=f"PPIC#{username}"
                ),
                InlineKeyboardButton(
                    "Go To Profile", url=f"https://www.instagram.com/{username}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "My Post", callback_data=f"POST#{username}"),
                InlineKeyboardButton(
                    "My Tagged Posts", callback_data=f"TAG#{username}"
                ),
                InlineKeyboardButton(
                    "Posts In My Feed", callback_data=f"FEED#{username}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "My Saved Posts", callback_data=f"SAVED#{username}"
                ),
                InlineKeyboardButton(
                    "My IGTV Posts", callback_data=f"IGTV#{username}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "My Highlights", callback_data=f"HIGHLIGHT#{username}"
                ),
                InlineKeyboardButton(
                    "My Stories ", callback_data=f"STORY#{username}"
                ),
                InlineKeyboardButton(
                    "Stories of My Following", callback_data=f"FSTORY#{username}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "List Of My Followers", callback_data=f"FOLLOWER#{username}"
                ),
                InlineKeyboardButton(
                    "List Of My Following", callback_data=f"FOLLOWING#{username}"
                ),
            ],
        ]
    )
    deleteMessage(context.bot, msg)
    bot.send_photo(
        chat_id=update.message.chat_id,
        photo=ppic,
        caption=f"You are already logged in as {name}\n\n<b>Your Account Details</b>\n\n🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {profile.is_private}\n🏭 <b>Is Business Account?</b>: {profile.is_business_account}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n📸 <b>Total Posts</b>: {media_count}\n📺 <b>IGTV Videos</b>: {igtv_count}",
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


def dl_content(update, context):
    args = update.message.text.strip().split(" ", maxsplit=1)
    if len(args) <= 1:
        sendMessage("Send insta post links after /mirror ",
                    context.bot, update)
    else:
        url = args[1]
        msg = sendMessage(
            f"Checking Given Details...!, Please Wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage(f"You must /{BotCommands.LoginCommand}", msg)
            return
        editMessage("Fetching data from Instagram🔗...!", msg)
        download_content(url, msg)


def ig(update, context):
    args = update.message.text.strip().split(" ", maxsplit=1)

    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgPostCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            f"Checking IG Username <b>@{username}</b>, Please Wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage(f"You must /{BotCommands.LoginCommand}", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
            else:
                media_count = profile.mediacount
                name = profile.full_name
                ppic = profile.profile_pic_url
                igtv_count = profile.igtvcount
                bio = profile.biography
                followers = profile.followers
                following = profile.followees
                if not allow_access(profile):
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Download Profile Pic",
                                    callback_data=f"PPIC#{username}",
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
                                    "Profile Pic", callback_data=f"PPIC#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Go To Profile",
                                    url=f"https://www.instagram.com/{username}",
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "All Post", callback_data=f"POST#{username}"
                                ),
                                InlineKeyboardButton(
                                    "All Tagged Posts",
                                    callback_data=f"TAG#{username}",
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "All IGTV", callback_data=f"IGTV#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Stories ", callback_data=f"STORY#{username}"
                                ),
                                InlineKeyboardButton(
                                    "Highlights", callback_data=f"HIGHLIGHT#{username}"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    f"{name}'s Followers",
                                    callback_data=f"FOLLOWER#{username}",
                                ),
                                InlineKeyboardButton(
                                    f"{name}'s Following",
                                    callback_data=f"FOLLOWING#{username}",
                                ),
                            ],
                        ]
                    )
                deleteMessage(context.bot, msg)
                bot.send_photo(
                    chat_id=update.message.chat.id,
                    photo=ppic,
                    caption=f"🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {'Private' if profile.is_private else 'Public'}\n🏭 <b>Is Business Account?</b>: {'Yes' if profile.is_business_account else 'No'}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n📸 <b>Total Posts</b>: {media_count}\n📺 <b>IGTV Videos</b>: {igtv_count}",
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                )


def post(update, context):
    """Download Instagram Posts"""
    args = update.message.text.strip().split(" ", maxsplit=1)

    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgPostCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            f"Checking IG Username <b>@{username}</b>, Please Wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage(f"You must /{BotCommands.LoginCommand}", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
            else:
                if not allow_access(profile):
                    editMessage(f"Please follow <code>@{username}</code>", msg)
                else:
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Picture Posts", callback_data=f"PIC#{profile.username}"
                                ),
                                InlineKeyboardButton(
                                    "Video Posts", callback_data=f"VID#{profile.username}"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "Picture & Video Posts",
                                    callback_data=f"PICVID#{profile.username}",
                                ),
                                InlineKeyboardButton(
                                    "ALL Posts", callback_data=f"ALLPOST#{profile.username}"
                                ),
                            ],
                        ]
                    )
                    editMessage(
                        f"Choose the type of post to download from <code>@{profile.username}</code>",
                        msg,
                        reply_markup=reply_markup,
                    )


def igtv(update, context):
    """Download IGTV from a given username"""
    args = update.message.text.strip().split(" ", maxsplit=1)
    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgPostCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            f"Checking IG Username {username}, Please Wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage(f"You Must login /{BotCommands.LoginCommand}", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
            else:
                if not allow_access(profile):
                    editMessage(
                        f"Please follow <code>@{username}</code>",
                        msg,
                    )
                else:
                    profile = Profile.from_username(INSTA.context, username)
                    igtv_count = profile.igtvcount
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Yes", callback_data=f"YES#{username}"),
                                InlineKeyboardButton("No", callback_data=f"NO#{username}"),
                            ]
                        ]
                    )
                    editMessage(
                        f"Total IGTV Count: <code>{igtv_count}</code>\nDo you want to download all IGTV videos of <code>@{username}</code>?",
                        msg,
                        reply_markup=reply_markup,
                    )


def highlights(update, context):
    """Download posts from a given username"""

    args = update.message.text.strip().split(" ", maxsplit=1)

    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgHighlightsCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            f"Checking IG Username <b>@{username}</b>, Please Wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage(f"You must /{BotCommands.LoginCommand}", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
            else:
                if not allow_access(profile):
                    editMessage(f"Please follow <code>@{username}</code>", msg)

                else:
                    download_highlights(profile, msg)


def story(update, context):
    args = update.message.text.strip().split(" ", maxsplit=1)
    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgStoryCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            f"Checking IG Username <b>@{username}</b>, Please Wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage(f"You must /{BotCommands.LoginCommand}", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
            else:
                if not allow_access(profile):
                    editMessage(f"Please follow <code>@{username}</code>", msg)

                else:
                    download_stories(profile, msg)


def followers(update, context):
    """Get followers list of a given username"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgPostCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            f"Checking IG Username {username}, Please Wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage(f"You Must login /{BotCommands.LoginCommand}", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
            else:
                if not allow_access(profile):
                    editMessage(
                        f"Please follow <code>@{username}</code>",
                        msg,
                    )
                else:

                    editMessage(
                        f"Fetching followers list of <code>@{username}</code>",
                        msg,
                    )
                    fetch_followers(profile, msg)


def following(update, context):
    """Get following list of a given username"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgPostCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            "Checking the given username, please wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
            else:
                if not allow_access(profile):
                    editMessage(
                        f"Please follow <code>@{username}</code>",
                        msg,
                    )
                else:
                    editMessage(
                        f"Fetching following list of <code>@{username}</code>",
                        msg,
                    )
                    fetch_following(profile, msg)


def mutual_following(update, context):
    """Get fans list of a given username"""
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgPostCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            "Checking the given username, please wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage("You must /login ", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)
        else:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
            else:
                if not allow_access(profile):
                    editMessage(
                        f"Please follow <code>@{username}</code>",
                        msg,
                    )
                else:
                    editMessage(
                        f"Fetching fans list of <code>@{username}</code>",
                        msg,
                    )
                    mutual_follow(profile, msg)


def tagged(update, context):
    """Download posts from a given username"""
    args = update.message.text.strip().split(" ", maxsplit=1)
    if len(args) <= 1:
        sendMessage(f"Please Send IG Username After /{BotCommands.IgPostCommand}", context.bot, update)
    else:
        username = args[1]
        msg = sendMessage(
            f"Checking IG Account, Please Wait...!", context.bot, update
        )
        if 1 not in STATUS:
            editMessage(f"You must /{BotCommands.LoginCommand}", msg)

        elif is_link(args[1]):
            editMessage("Please send a username only...!", msg)

        else:
            profile, error = check_username(username)
            if error:
                editMessage(f"Sorry...! <b>{error}</b>!", msg)
                return
            download_tagged(profile, msg)


def feed(update, context):
    """Download posts from a given username"""
    msg = sendMessage(
        f"Checking IG Account, Please Wait...!", context.bot, update
    )
    if 1 not in STATUS:
        editMessage(f"You must /{BotCommands.LoginCommand}", msg)


    else:
        download_feed(msg)


def saved(update, context):
    """Download posts from a given username"""
    msg = sendMessage(
        f"Checking IG Account, Please Wait...!", context.bot, update
    )
    if 1 not in STATUS:
        editMessage(f"You must /{BotCommands.LoginCommand}", msg)

    else:
        profile, error = check_username(INSTA.context.username)
        if error:
            editMessage(f"Sorry...! <b>{error}</b>!", msg)
            return
        download_saved(profile, msg)


def following_stories(update, context):
    """Download posts from a given username"""
    args = update.message.text.strip().split(" ", maxsplit=1)

    msg = sendMessage(
        f"Checking IG Account, Please Wait...!", context.bot, update
    )
    if 1 not in STATUS:
        editMessage(f"You must /{BotCommands.LoginCommand}", msg)

    else:
        profile, error = check_username(INSTA.context.username)
        if error:
            editMessage(f"Sorry...! <b>{error}</b>!", msg)
            return
        download_following_stories(msg)


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

following_handler = CommandHandler(
    BotCommands.IgFollowingCommand,
    following,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(following_handler)

mutual_follow_handler = CommandHandler(
    BotCommands.IgMutualCommand,
    mutual_following,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(mutual_follow_handler)

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
    following_stories,
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

account_handler = CommandHandler(
    BotCommands.IgAccountCommand,
    my_account,
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
    dl_content,
    CustomFilters.authorized_chat
    | CustomFilters.owner_filter
    | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(mirrorlink_handler)
