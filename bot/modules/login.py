from bot.helper.ext_utils.bot_utils import acc_type,usercheck,usersave,is_link,yes_or_no
import os
from instaloader import Profile, TwoFactorAuthRequiredException, BadCredentialsException
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot import  dispatcher,L,STATUS
from bot.helper.telegram_helper.bot_commands import BotCommands
from telegram.ext import  CommandHandler, MessageHandler, Filters,ConversationHandler


insta = L
CODE_SAVE = range(2) 

def user_login(update, context):
    USER=usercheck()
    args=update.message.text.split(" ", maxsplit=2)
    if len(args)>2:
        username=args[1]
        usersave(username)
        password=args[2]
        deleteMessage(context.bot, update.message)
        m = sendMessage(f"Checking user @{username} \n Please Wait..!", context.bot, update)
        if 1 in STATUS:
            editMessage(f"Default @{USER} is Already Logged In,Try To Remove By /logout", m)
        elif is_link(args[1])==True:
            editMessage("Please send a username not link use /ig <b>link</b> ", m)
        else:
            try:
                insta.login(username, password)
                insta.save_session_to_file(filename=f"./{username}")
                STATUS.add(1)
                m = bot.edit_message_text(f"Fetching the details of @{username}\n please wait...!", m.chat_id, m.message_id)
                profile = Profile.from_username(insta.context, username)
                mediacount = profile.mediacount
                name = profile.full_name
                bio = profile.biography
                profilepic = profile.profile_pic_url
                igtvcount = profile.igtvcount
                followers = profile.followers
                following = profile.followees
                deleteMessage(context.bot, m)
                bot.send_photo(
                chat_id=update.message.chat.id,
                caption=f"You are successfully Logged In as {name}\n\n<b>Your Account Details</b>\n\n🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n📸 <b>Total Posts</b>: {mediacount}\n📺 <b>IGTV Videos</b>: {igtvcount}",parse_mode="HTML",
                photo=profilepic
                )
                return ConversationHandler.END
            
            except BadCredentialsException:
                editMessage("Wrong Credentials\n\n/login again", m)
                pass
                return ConversationHandler.END
           
            except TwoFactorAuthRequiredException:
                editMessage("Send your 2F Code within 60sec...!", m)
                return CODE_SAVE

            except Exception as e:
                editMessage(f"{e}\nTry /login again", m)
                return ConversationHandler.END
    else:
        if 1 in STATUS:
            sendMessage(f"@{USER} Already Logged In try to Logout by /logout\nUse /account to see Current User", context.bot, update)
            return ConversationHandler.END
        else:
            sendMessage(f'Send Your Ig Username and Password\n\n/login <b>username</b> <b>password</b>', context.bot, update)
            return ConversationHandler.END

def timeout(update, context):
    update.message.reply_text('Oh! TimeOut\nTry Again /login')
    return ConversationHandler.END

def codei (update, context):
    username=usercheck()
    codei= update.message.text
    if codei.isdigit()==True:
        codei=int(codei)
        try:
            insta.two_factor_login(codei)
            insta.save_session_to_file(filename=f"./{username}")
            STATUS.add(1)
            m= sendMessage( "Fetching details from Instagram", context.bot, update)
            profile = Profile.from_username(insta.context, username)
            mediacount = profile.mediacount
            name = profile.full_name
            bio = profile.biography
            profilepic = profile.profile_pic_url
            igtvcount = profile.igtvcount
            followers = profile.followers
            following = profile.followees
            deleteMessage(context.bot, m)
            bot.send_photo(
            chat_id=update.message.chat.id,
            caption=f"You are successfully In as {name}\n\n<b>Your Account Details</b>\n\n🏷 <b>Name</b>: {name}\n🔖 <b>Username</b>: {profile.username}\n📝 <b>Bio</b>: {bio}\n📍 <b>Account Type</b>: {acc_type(profile.is_private)}\n🏭 <b>Is Business Account?</b>: {yes_or_no(profile.is_business_account)}\n👥 <b>Total Followers</b>: {followers}\n👥 <b>Total Following</b>: {following}\n📸 <b>Total Posts</b>: {mediacount}\n📺 <b>IGTV Videos</b>: {igtvcount}",parse_mode="HTML",
            photo=profilepic
            )
        except BadCredentialsException:
            sendMessage("Wrong Credentials\n\n/iglogin again", context.bot, update)
            pass
        except Exception as e:
            sendMessage(f"{e}\nTry /login again", context.bot, update)
            pass
    else:
        sendMessage("Please Enter a valid code", context.bot, update)
    
    return ConversationHandler.END

            

def logout(update, context):
    USER=usercheck()
    if 1 in STATUS:
        sendMessage("Succesfully Logged Out", context.bot, update)
        STATUS.remove(1)
        os.remove(f"./{USER}")
    else:
        sendMessage("You are not Logged in\nTry to Login /login ", context.bot, update)



logout_handler = CommandHandler(BotCommands.IgLogoutCommand, logout, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)

userlogin_handler = ConversationHandler(entry_points=[CommandHandler( BotCommands.LoginCommand, user_login, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)], 
    states={CODE_SAVE: [MessageHandler(Filters.text, codei)],
    ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command,timeout)]},
    fallbacks=[],conversation_timeout=60)

dispatcher.add_handler(logout_handler)

dispatcher.add_handler(userlogin_handler)
