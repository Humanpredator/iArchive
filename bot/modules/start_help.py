from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from telegraph import Telegraph

from bot import dispatcher, telegraph_token
from bot.helper.tg_utils import button_build
from bot.helper.tg_utils.bot_commands import BotCommands
from bot.helper.tg_utils.filters import CustomFilters
from bot.helper.tg_utils.message_utils import sendMarkup


def start(update, context):
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("Insta-Scrap Repo",
                        "https://github.com/Humanpredator/iScrap")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(1))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(
            update):
        start_string = f"""
Thanks to Slam and SUBIN\n
This bot can download all the Instagram Accounts posts..!
Type /{BotCommands.HelpCommand} to get a list of available commands..!
"""
        sendMarkup(start_string, context.bot, update, reply_markup)
    else:
        sendMarkup(
            "Oops! not a Authorized user.\nPlease deploy your own <b>Insta-Scrap Bot</b>.",
            context.bot,
            update,
            reply_markup,
        )


help_string_telegraph = f"""
<b>/{BotCommands.HelpCommand}</b>: To get this message
<br><br>
<b>/{BotCommands.IgAccountCommand}</b>: To get Details to Currently logged Account.
<br><br>
<b>/{BotCommands.IgSearchCommand}</b>: Get Details of Given username  <b>eg: /{BotCommands.IgSearchCommand} username</b>
<br><br>
<b>/{BotCommands.IgMirrorCommand}</b>: To download Instagram post/reel/igtv/stories. <b> Eg: /{BotCommands.IgMirrorCommand} post/reel/igtv/stories link </b>
<br><br>
<b>/{BotCommands.IgPostCommand}</b>: To get Download Posts of Given Username <b>eg: /{BotCommands.IgPostCommand} username.</b>
<br><br>
<b>/{BotCommands.IgStoryCommand}</b>: To Download given Username's Story <b>eg: /{BotCommands.IgStoryCommand} username.</b>
<br><br>
<b>/{BotCommands.IgHighlightsCommand}</b>: To Download Highlights of given username <b>eg: /{BotCommands.IgHighlightsCommand} username.</b>
<br><br>
<b>/{BotCommands.IgTvCommand}</b>: To Download IGTV Posts of given username <b>eg: /{BotCommands.IgTvCommand} username.</b>
<br><br>
<b>/{BotCommands.IgFollowingCommand}</b>: To get Following list of given username in JSON <b>eg: /{BotCommands.IgFollowingCommand} username.</b>
<br><br>
<b>/{BotCommands.IgFollowersCommand}</b>: To get Followers list of given username <b>eg: /{BotCommands.IgFollowersCommand} username.</b>
<br><br>
<b>/{BotCommands.IgMutualCommand}</b>: To get list user whom she/he following and following his/her back. <br> Eg: <code>/{BotCommands.IgMutualCommand}  <b>username</b> </code>
<br><br>
<b>/{BotCommands.IgTaggedCommand}</b>: To Download Tagged posts of any username's in Instagram <b>eg: /{BotCommands.IgTaggedCommand} username.</b>
<br><br>


<b>/{BotCommands.IgFeedCommand}</b>: To download your Feed Post, limit:10. <br> Eg: <code>/{BotCommands.IgFeedCommand}</code>
<br><br>
<b>/{BotCommands.IgSavedCommand}</b>: To download All your Saved Posts. <br> Eg: <code>/{BotCommands.IgSavedCommand}</code>
<br><br>
<b>/{BotCommands.IgStoriesCommand}</b>: To download your following users story. <br> Eg: <code>/{BotCommands.IgStoriesCommand} </code>
<br><br>

"""

ighelp = Telegraph(access_token=telegraph_token,
                   domain="graph.org").create_page(
                       title="Instagram Bot Help",
                       author_name="Humanpredator",
                       author_url="https://github.com/Humanpredator",
                       html_content=help_string_telegraph,
)["path"]

help_string = f"""
/{BotCommands.PingCommand}: Check how long it takes to Ping the Bot

/{BotCommands.AuthorizeCommand}: Authorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)

/{BotCommands.UnAuthorizeCommand}: Unauthorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)

/{BotCommands.AuthorizedUsersCommand}: Show authorized users (Only Owner & Sudo)

/{BotCommands.AddSudoCommand}: Add sudo user (Only Owner)

/{BotCommands.RmSudoCommand}: Remove sudo users (Only Owner)

/{BotCommands.RestartCommand}: Restart the bot

/{BotCommands.LogCommand}: Get a log file of the bot. Handy for getting crash reports

/{BotCommands.SpeedCommand}: Check Internet Speed of the Host

/{BotCommands.ShellCommand}: Run commands in Shell (Only Owner)

/{BotCommands.StatsCommand}: Get Stats of the bot
"""


def igbot_help(update, context):
    button = button_build.ButtonMaker()
    button.buildbutton("Other Commands", f"https://graph.org/{ighelp}")
    reply_markup = InlineKeyboardMarkup(button.build_menu(1))
    sendMarkup(help_string, context.bot, update, reply_markup)


ighelp_handler = CommandHandler(
    BotCommands.HelpCommand,
    igbot_help,
    filters=CustomFilters.authorized_chat
    | CustomFilters.authorized_user
    | CustomFilters.owner_filter,
    run_async=True,
)

start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)

dispatcher.add_handler(ighelp_handler)

dispatcher.add_handler(start_handler)
