from telegram.ext import CommandHandler
from telegraph import Telegraph
from bot import  dispatcher,telegraph_token
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper import button_build



help_string_telegraph=f'''
<b>/{BotCommands.HelpCommand}</b>: To get this message
<br><br>
<b>/{BotCommands.IgLogoutCommand}</b>: To Logout Default Account.
<br><br>
<b>/{BotCommands.LoginCommand}</b>: To Login Custom User Account.<br> Eg: <code>/{BotCommands.LoginCommand}  <b>username</b> <b>password</b> </code>
<br><br>
<b>/{BotCommands.IgFansCommand}</b>: To get User Instagram Fans List. <br> Eg: <code>/{BotCommands.IgFansCommand}  <b>username</b> </code>
<br><br>
<b>/{BotCommands.IgNotFollowingCommand}</b>: To get User Instagram Not Following List.  <br> Eg: <code>/{BotCommands.IgNotFollowingCommand}  <b>username</b> </code>
<br><br>
<b>/{BotCommands.IgFeedCommand}</b>: To download your Instagram Feed. <br> Eg: <code>/{BotCommands.IgFeedCommand}  <b>mention count or leave it empty to download all</b> </code>
<br><br>
<b>/{BotCommands.IgSavedCommand}</b>: To download your Instagram Saved. <br> Eg: <code>/{BotCommands.IgSavedCommand}  <b>mention count or leave it empty to download all</b> </code>
<br><br>
<b>/{BotCommands.IgStoriesCommand}</b>: To download your Instagram Stories.
<br><br>
<b>/{BotCommands.IgPostCommand}</b>: To get post of any username's in Instagram <b>eg: /{BotCommands.IgPostCommand} username.</b>
<br><br>
<b>/{BotCommands.IgMirrorCommand}</b>: To download Instagram post. <b> Eg: /{BotCommands.IgMirrorCommand} posts link </b>
<br><br>
<b>/{BotCommands.IgTvCommand}</b>: To get IGTV Posts of any username's in Instagram <b>eg: /{BotCommands.IgTvCommand} username.</b>
<br><br>
<b>/{BotCommands.IgStoryCommand}</b>: To get Story of any username's in Instagram <b>eg: /{BotCommands.IgStoryCommand} username.</b>
<br><br>
<b>/{BotCommands.IgHighlightsCommand}</b>: To get Highlights of any username's in Instagram <b>eg: /{BotCommands.IgHighlightsCommand} username.</b>
<br><br>
<b>/{BotCommands.IgSearchCommand}</b>: send IG  username's or post link  <b>eg: /{BotCommands.IgSearchCommand} username to get user details or /{BotCommands.IgSearchCommand} post links to download.</b>
<br><br>
<b>/{BotCommands.IgAccountCommand}</b>: To get Details to Currently logged Account.
<br><br>
<b>/{BotCommands.IgFollowersCommand}</b>: To get Followers list of any username's in Instagram <b>eg: /{BotCommands.IgFollowersCommand} username.</b>
<br><br>
<b>/{BotCommands.IgFollowingCommand}</b>: To get Following list of any username's in Instagram <b>eg: /{BotCommands.IgFollowingCommand} username.</b>
<br><br>
<b>/{BotCommands.IgTaggedCommand}</b>: To Download Tagged posts of any username's in Instagram <b>eg: /{BotCommands.IgTaggedCommand} username.</b>
<br><br>
'''

ighelp = Telegraph(access_token=telegraph_token).create_page(
        title='Instagram Bot Help',
        author_name='SUBIN',
        author_url='https://github.com/subinps',
        html_content=help_string_telegraph,
    )["path"]




help_string=f'''
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
'''


def igbot_help(update, context):
    button = button_build.ButtonMaker()
    button.buildbutton("Other Commands", f"https://telegra.ph/{ighelp}")
    reply_markup = InlineKeyboardMarkup(button.build_menu(1))
    sendMarkup(help_string, context.bot, update, reply_markup)


ighelp_handler = CommandHandler(BotCommands.HelpCommand, igbot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user | CustomFilters.owner_filter, run_async=True)
dispatcher.add_handler(ighelp_handler)
