from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.helper.down_utilis.insta_down import download_insta
from bot.helper.ext_utils.bot_utils import usercheck

import os
from instaloader import Profile
from bot.helper.telegram_helper.message_utils import *
from bot import dispatcher,OWNER_ID,L
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


insta =L

def cb_handler(update, context):
    USER = usercheck()
    session=f"./{USER}"  
    query = update.callback_query
    username = query.data.split("#")[1]
    profile = Profile.from_username(insta.context, username)
    mediacount = profile.mediacount
    name = profile.full_name
    profilepic = profile.profile_pic_url
    igtvcount = profile.igtvcount
    followers = profile.followers
    folllowing = profile.followees
    
    
    if query.data.startswith("ppic"):
        profile = Profile.from_username(insta.context, username)
        profilepichd = profile.profile_pic_url
        query.answer()
        bot.send_document(query.message.chat.id,profilepichd,caption=f"<b>Name:</b>{name}\n<b>Username:</b>{username}",parse_mode="HTML")
    
    elif query.data.startswith("post"):
        query.delete_message()
        query.answer()
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Pictures Only", callback_data=f"photos#{username}"),
                        InlineKeyboardButton("Videos Only", callback_data=f"videos#{username}")
                    ],
                    [
                        InlineKeyboardButton("Pictures and videos", callback_data=f"picandvid#{username}"),
                        InlineKeyboardButton("All Posts", callback_data=f"allposts#{username}"),
                    ]
                ]
            )
        bot.send_message(chat_id=query.message.chat.id, text="Select the type of posts you want to fetch",reply_markup=reply_markup,parse_mode="HTML")
    
    elif query.data.startswith("photos"):
        chat_id=query.message.chat.id
        if mediacount==0:
            query.edit_message_text("There are no posts by the user")
            return
        else: 
            m = query.edit_message_text("Starting Downloading..\nThis may take time depending upon number of Posts.")      
            dir=f"{OWNER_ID}/{username}"
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-profile-pic",
                "--no-videos",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", username
                ]
            download_insta(command, m, dir,username,chat_id,fetch='Photos')

    elif query.data.startswith("videos"):
        chat_id=query.message.chat.id
        if mediacount==0:
            query.edit_message_text("There are no posts by the user")
            return
        m= query.edit_message_text("Starting Downloading..\nThis may take time depending upon number of Posts.")      
        dir=f"{OWNER_ID}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-pictures",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
            ]
        download_insta(command, m, dir,username,chat_id,fetch='Videos')
  
    elif query.data.startswith("picandvid"):
        chat_id=query.message.chat.id
        if mediacount==0:
            query.edit_message_text("There are no posts by the user")
            return
        m= query.edit_message_text("Starting Downloading..\nThis may take time depending upon number of Posts.")      
        dir=f"{OWNER_ID}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
            ]
        download_insta(command, m, dir,username,chat_id,fetch='Photos+Videos')

    elif query.data.startswith("allposts"):
        chat_id=query.message.chat.id
        if mediacount==0:
            query.edit_message_text("There are no posts by the user")
            return
        m= query.edit_message_text("Starting Downloading..\nThis may take longer time Depending upon number of posts.")    
        dir=f"{OWNER_ID}/{username}"
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--igtv",
            "--highlights",
            "--stories",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
            ]
        download_insta(command, m, dir,username,chat_id,fetch='All Posts')

    elif query.data.startswith("igtv"):
        query.delete_message()
        query.answer()
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yes", callback_data=f"yes#{username}"),
                    InlineKeyboardButton("No", callback_data=f"no#{username}")
                ]
            ]
        )
        bot.send_message(chat_id=query.message.chat.id, text=f"Do you want to download IGTV Posts of {name}?", reply_markup=reply_markup)
    
    elif query.data.startswith("yes"):
        chat_id=query.message.chat.id
        if igtvcount==0:
            query.edit_message_text("There are no IGTV posts by the user")
            return
        m= query.edit_message_text("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
        dir=f"{OWNER_ID}/{username}"

        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--igtv",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            "--", username
            ]
        download_insta(command, m, dir,username,chat_id,fetch='IGTV')
   
    elif query.data.startswith("no"):
        query.delete_message()
        query.answer()
        bot.send_message(chat_id=query.message.chat.id, text=f"Process Cancelled posts")
        bot.delete_message(chat_id=query.message.chat.id, message_id=m.message_id, timeout=5)

    elif query.data.startswith("followers"):
        query.delete_message()
        chat_id=query.message.chat.id
        m=bot.send_message(chat_id, f"Fetching Followers List of {name}")
        try:
            followers=f"**Followers List for {name}**\n\n"
            f = profile.get_followers()
            for p in f:
                followers += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s followers.txt", "w")
            text_file.write(followers)
            text_file.close()
            m.delete()           
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s followers.txt", "rb"))
            os.remove(f"./{username}'s followers.txt")
        except:
            bot.send_message(chat_id=chat_id, text=f"Error Occured")
            return
 
    elif query.data.startswith("following"):
        query.delete_message()
        chat_id=query.message.chat.id
        m=bot.send_message(chat_id, f"Fetching Following list of {name}")
        try: 
            followees=f"**Following List for {name}**\n\n"
            f = profile.get_followees()
            for p in f:
                followees += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
            text_file = open(f"{username}'s following.txt", "w")
            text_file.write(followees)
            text_file.close()
            m.delete()
            bot.send_document(chat_id=chat_id, document=open(f"{username}'s following.txt", 'rb'),caption=f"<b>{name}'s following</b>", parse_mode='HTML')
            os.remove(f"./{username}'s following.txt")
            LOGGER.info("following list removed")
        except:
            bot.send_message(chat_id=chat_id, text=f"Error Occured")
            return
    
    else:
        dir=f"{OWNER_ID}/{username}"
        chat_id=query.message.chat.id   
        query.delete_message()
        m= bot.send_message(chat_id, "Starting Downloading..\nThis may take longer time Depending upon number of posts.") 
        cmd = query.data.split("#")[0] 
        username = query.data.split("#")[1]   
        if cmd == "feed":
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
           
        elif cmd=="saved":
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
            
        elif cmd=="tagged":
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
            
        elif cmd=="stories":
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
            
        elif cmd=="fstories":
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
            download_insta(command, m, dir,username,chat_id,fetch='Stories of My Following')
        elif cmd=="highlights":
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
            download_insta(command, m, dir,username,chat_id,fetch='Highlights')
       
callback_handler = CallbackQueryHandler(cb_handler)
dispatcher.add_handler(callback_handler)

