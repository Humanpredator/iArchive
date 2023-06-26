import json
import os
import time

import instaloader
import shortuuid
from instaloader import Profile

from bot import DOWNLOAD_STATUS_UPDATE_INTERVAL, INSTA, LOGGER, OWNER_ID
from bot.helper.ext_utils.bot_utils import check_instagram_url
from bot.helper.ext_utils.fs_utils import clean_download, datetime_india
from bot.helper.ext_utils.gdrive import upload_folder_to_drive
from bot.helper.tg_utils.message_utils import editMessage, sendDoc
from bot.helper.tg_utils.tg_upload import tgup


def check_username(username):
    try:
        if username == str(INSTA.context.username):
            result = Profile.own_profile(INSTA.context)
            return result, None
        result = Profile.from_username(INSTA.context, username)
        return result, None

    except Exception as e:
        return None, e


def download_posts(profile, msg, picture: bool = False, video: bool = False):
    directory = f"{OWNER_ID}/{profile.username}"
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.dirname_pattern = directory
    if picture:
        INSTA.download_pictures = True
        INSTA.download_videos = False
    if video:
        INSTA.download_videos = True
        INSTA.download_pictures = False

    for index, post in enumerate(profile.get_posts()):
        try:
            response = INSTA.download_post(post, target=directory)
            res_msg = f"""<b>Filename</b> : <code>{profile.username}_{post.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>{"Pictures" if picture else "Videos"}</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)

        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    cmp_msg = "Successfully Downloaded Posts"
    LOGGER.info("Download Completed-%s", profile.username)
    editMessage(cmp_msg, msg)
    INSTA.close()
    upload_folder_to_drive(directory, msg, profile.username, "Posts")
    clean_download(directory)


def download_all_posts(profile, msg):
    directory = f"{OWNER_ID}/{profile.username}"
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.download_videos = True
    INSTA.download_pictures = True
    INSTA.dirname_pattern = directory
    INSTA.download_profile(profile.username, profile_pic_only=True)
    for index, post in enumerate(profile.get_posts()):
        try:
            response = INSTA.download_post(post, target=directory)
            res_msg = f"""<b>Filename</b> : <code>{profile.username}_{post.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>{"AllPosts"}</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    LOGGER.info(f"User Posts Download Completed-{profile.username}")

    for user_highlight in INSTA.get_highlights(profile):
        try:
            for index, highlights in enumerate(user_highlight.get_items()):
                try:
                    response = INSTA.download_storyitem(highlights, directory)
                    res_msg = f"""<b>Filename</b> : <code>{profile.username}_{highlights.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Highlights: {user_highlight.title}</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    editMessage(res_msg, msg)

                except Exception as e:
                    LOGGER.info(str(e))
                    editMessage(str(e), msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
        LOGGER.info(f"User Highlights Download Completed-{profile.username}")

    for i, user_story in enumerate(
            INSTA.get_stories(userids=[profile.userid])):
        try:
            for index, story in enumerate(user_story.get_items()):
                try:
                    response = INSTA.download_storyitem(story, directory)
                    res_msg = f"""<b>Filename</b> : <code>{profile.username}_{story.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Stories</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    editMessage(res_msg, msg)
                except Exception as e:
                    LOGGER.info(str(e))
                    editMessage(str(e), msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    LOGGER.info(f"User Stories Download Completed-{profile.username}")

    for i, igtv in enumerate(profile.get_igtv_posts()):
        try:
            response = INSTA.download_post(igtv, target=directory)
            res_msg = f"""<b>Filename</b> : <code>{profile.username}_{igtv.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>IGTV</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{i + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    LOGGER.info(f"User IGTV Download Completed-{profile.username}")

    INSTA.close()
    cmp_msg = "Successfully Downloaded Posts"
    LOGGER.info("Download Completed-%s", profile.username)
    editMessage(cmp_msg, msg)

    upload_folder_to_drive(directory, msg, profile.username, "All Posts")
    clean_download(directory)


def download_highlights(profile, msg):
    directory = f"{OWNER_ID}/{profile.username}"
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.download_videos = True
    INSTA.download_pictures = True
    INSTA.dirname_pattern = directory
    for user_highlight in INSTA.get_highlights(profile):
        try:
            for index, highlights in enumerate(user_highlight.get_items()):
                try:
                    response = INSTA.download_storyitem(highlights, directory)
                    res_msg = f"""<b>Filename</b> : <code>{profile.username}_{highlights.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Highlights: {user_highlight.title}</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    editMessage(res_msg, msg)

                except Exception as e:
                    LOGGER.info(str(e))
                    editMessage(str(e), msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
        LOGGER.info(f"User Highlights Download Completed-{profile.username}")
    upload_folder_to_drive(directory, msg, profile.username, "Highlights")
    clean_download(directory)


def download_stories(profile, msg):
    directory = f"{OWNER_ID}/{profile.username}"
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.download_videos = True
    INSTA.download_pictures = True
    INSTA.dirname_pattern = directory
    for i, user_story in enumerate(
            INSTA.get_stories(userids=[profile.userid])):
        try:
            for index, story in enumerate(user_story.get_items()):
                try:
                    response = INSTA.download_storyitem(story, directory)
                    res_msg = f"""<b>Filename</b> : <code>{profile.username}_{story.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Stories</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    editMessage(res_msg, msg)
                except Exception as e:
                    LOGGER.info(str(e))
                    editMessage(str(e), msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    LOGGER.info(f"User Stories Download Completed-{profile.username}")
    upload_folder_to_drive(directory, msg, profile.username, "Stories")
    clean_download(directory)


def download_igtv(profile, msg):
    directory = f"{OWNER_ID}/{profile.username}"
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.download_videos = True
    INSTA.download_pictures = True
    INSTA.dirname_pattern = directory
    for index, media in enumerate(profile.get_igtv_posts()):
        try:
            response = INSTA.download_post(media, directory)
            res_msg = f"""<b>Filename</b> : <code>{profile.username}_{media.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>IGTV</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    LOGGER.info(f"User IGTV Download Completed-{profile.username}")
    upload_folder_to_drive(directory, msg, profile.username, "IGTV")
    clean_download(directory)


def fetch_followers(profile, msg):
    followers_json = {}
    folder_path = os.path.join(os.getcwd(), str(OWNER_ID), "Followers")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, f"{profile.username}_followers.json")
    followers_list = profile.get_followers()
    for index, follower in enumerate(followers_list, start=1):
        try:
            followers_json[follower.username] = {
                "full_name": str(follower.full_name),
                "profile_link": f"www.instagram.com/{follower.username}",
            }
            res_msg = f"""<b>Follower</b> : <code>{follower.username}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Followers</code>
<b>DL Status</b> : <code>N/A</code>
<b>Progress</b> : <code>{index}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)

    LOGGER.info(f"User Followers Download Completed-{profile.username}")
    editMessage("Etching Followers to JSON...!", msg)
    with open(file_path, "w", encoding="UTF-8") as file:
        json.dump(followers_json, file)
    sendDoc(file_path, msg, f"Followers List for {profile.full_name}")


def fetch_following(profile, msg):
    following_json = {}
    folder_path = os.path.join(os.getcwd(), str(OWNER_ID), "Following")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, f"{profile.username}_following.json")
    following_list = profile.get_followees()
    for index, following in enumerate(following_list, start=1):
        try:
            following_json[following.username] = {
                "full_name": following.full_name,
                "profile_link": f"www.instagram.com/{following.username}",
            }
            res_msg = f"""<b>Follower</b> : <code>{following.username}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Followers</code>
<b>DL Status</b> : <code>N/A</code>
<b>Progress</b> : <code>{index}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)

    LOGGER.info(f"User Following Download Completed-{profile.username}")
    editMessage("Etching Following to JSON...!", msg)
    with open(file_path, "w", encoding="UTF-8") as file:
        json.dump(following_json, file)
    sendDoc(file_path, msg, f"Following List for {profile.full_name}")


def mutual_follow(profile, msg):
    folder_path = os.path.join(os.getcwd(), str(OWNER_ID), "Mutual")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, f"{profile.username}_mutual.json")
    follower_list = []
    following_list = []
    mutual_json = {}

    followers = profile.get_followers()
    followings = profile.get_followees()

    for index, follower in enumerate(followers, start=1):
        try:
            follower_list.append(follower)
            res_msg = f"""<b>Follower</b> : <code>{follower.username}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Followers</code>
<b>DL Status</b> : <code>Fetching Follower List..!</code>
<b>Progress</b> : <code>{index}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    LOGGER.info(f"User Follower Download Completed-{profile.username}")

    for index, following in enumerate(followings, start=1):
        try:
            following_list.append(following)
            res_msg = f"""<b>Follower</b> : <code>{following.username}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Followers</code>
<b>DL Status</b> : <code>Fetching Following List..!</code>
<b>Progress</b> : <code>{index}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    LOGGER.info(f"User Following Download Completed-{profile.username}")

    mutuals = set(follower_list) & set(following_list)

    for index, mutual in enumerate(mutuals, start=1):
        try:
            mutual_json[mutual.username] = {
                "full_name": mutual.full_name,
                "profile_link": f"www.instagram.com/{mutual.username}",
            }
            res_msg = f"""<b>Follower</b> : <code>{mutual.username}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Followers</code>
<b>DL Status</b> : <code>Fetching Mutual Follow List..!</code>
<b>Progress</b> : <code>{index}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    LOGGER.info(
        f"User Mutual Follow List Download Completed-{profile.username}")

    editMessage("Etching Mutual Follow List to JSON...!", msg)
    with open(file_path, "w", encoding="UTF-8") as file:
        json.dump(mutual_json, file)
    sendDoc(file_path, msg, f"Following List for {profile.full_name}")


def download_tagged(profile, msg):
    directory = f"{OWNER_ID}/{profile.username}"
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.download_pictures = True
    INSTA.download_videos = True
    INSTA.dirname_pattern = directory

    for index, post in enumerate(profile.get_tagged_posts()):
        try:
            response = INSTA.download_post(post, target=directory)
            res_msg = f"""<b>Filename</b> : <code>{profile.username}_{post.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>Saved</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    cmp_msg = "Successfully Downloaded Posts"
    LOGGER.info("Download Completed-%s", INSTA.context.username)
    editMessage(cmp_msg, msg)
    INSTA.close()
    upload_folder_to_drive(directory, msg, INSTA.context.username, "Posts")
    clean_download(directory)


def download_content(url, msg):
    response = check_instagram_url(url)
    if not response:
        editMessage("URL Content Is Not Supported...!", msg)
    else:
        directory = f"{OWNER_ID}/Downloads/{str(shortuuid.uuid())}"
        INSTA.dirname_pattern = directory
        INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
        INSTA.download_video_thumbnails = False
        INSTA.download_geotags = False
        INSTA.download_comments = False
        INSTA.save_metadata = False
        INSTA.compress_json = False
        content_type = response.get("content_type")
        short_code = response.get("shortcode")
        username = response.get("username")
        if content_type in ("POST", "IGTV", "REEL"):
            build_post = instaloader.Post.from_shortcode(
                INSTA.context, short_code)
            if not build_post:
                LOGGER.info("Post is Unavailable")
                editMessage("Instagram Content is Unavailable", msg)
                return

            x = INSTA.download_post(build_post,
                                    target=build_post.owner_username)
            res_msg = f"""<b>Filename</b> : <code>{build_post.owner_username}_{build_post.date_utc}</code>
<b>Username</b> : <code>{build_post.owner_username}</code>
<b>Downloading</b> : <code>{content_type}</code>
<b>DL Status</b> : <code>{x}</code>
<b>Progress</b> : <code>N/A</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
            tgup(msg, directory)
            clean_download(directory)
            return
        if content_type in ["STORY"]:
            profile, error = check_username(username)
            if error:
                editMessage(
                    f"Sorry...! <b>{error}</b>!",
                    msg,
                )
                return
            for index, user_story in enumerate(
                    INSTA.get_stories(userids=[profile.userid])):
                try:
                    for i, story in enumerate(user_story.get_items()):
                        try:
                            if str(story.mediaid) == short_code:
                                x = INSTA.download_storyitem(
                                    story, target=INSTA.dirname_pattern)
                                res_msg = f"""<b>Filename</b> : <code>{profile.username}_{story.date_utc}</code>
<b>Username</b> : <code>{profile.username}</code>
<b>Downloading</b> : <code>{content_type}</code>
<b>DL Status</b> : <code>{x}</code>
<b>Progress</b> : <code>N/A</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
                                time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                                editMessage(res_msg, msg)
                                tgup(msg, directory)
                                clean_download(directory)
                                return
                        except Exception as e:
                            LOGGER.info(str(e))
                            editMessage(str(e), msg)
                except Exception as e:
                    LOGGER.info(str(e))
                    editMessage(str(e), msg)
            editMessage("Story is Unavailable", msg)


def download_saved(profile, msg):
    directory = f"{OWNER_ID}/My_Saved"
    INSTA.dirname_pattern = directory
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.download_pictures = True
    INSTA.download_videos = True
    for index, post in enumerate(profile.get_saved_posts()):
        try:
            response = INSTA.download_post(post, target=directory)
            res_msg = f"""<b>Filename</b> : <code>{INSTA.context.username}_{post.date_utc}</code>
<b>Username</b> : <code>{INSTA.context.username}</code>
<b>Downloading</b> : <code>Saved</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    cmp_msg = "Successfully Downloaded Posts"
    LOGGER.info("Download Completed-%s", INSTA.context.username)
    editMessage(cmp_msg, msg)
    INSTA.close()
    upload_folder_to_drive(directory, msg, INSTA.context.username, "Posts")
    clean_download(directory)


def download_feed(msg, max_count=10):
    directory = f"{OWNER_ID}/My_Feed"
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.download_pictures = True
    INSTA.download_videos = True
    INSTA.dirname_pattern = directory
    count = 0
    for index, post in enumerate(INSTA.get_feed_posts()):
        if count == max_count:
            break
        try:
            response = INSTA.download_post(post, target=directory)
            res_msg = f"""<b>Filename</b> : <code>{INSTA.context.username}_{post.date_utc}</code>
<b>Username</b> : <code>{INSTA.context.username}</code>
<b>Downloading</b> : <code>Feed</code>
<b>DL Status</b> : <code>{response}</code>
<b>Progress</b> : <code>{index + 1}</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
            time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
            editMessage(res_msg, msg)
            count += 1
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    cmp_msg = "Successfully Downloaded Posts"
    LOGGER.info("Download Completed-%s", INSTA.context.username)
    editMessage(cmp_msg, msg)
    INSTA.close()
    upload_folder_to_drive(directory, msg, INSTA.context.username, "Posts")
    clean_download(directory)


def download_following_stories(msg):
    directory = f"{OWNER_ID}/following_stories"
    INSTA.dirname_pattern = directory
    INSTA.filename_pattern = "{profile}_UTC_{date_utc}"
    INSTA.download_video_thumbnails = False
    INSTA.download_geotags = False
    INSTA.download_comments = False
    INSTA.save_metadata = False
    INSTA.compress_json = False
    INSTA.download_pictures = True
    INSTA.download_videos = True
    for index, user_story in enumerate(INSTA.get_stories()):
        try:
            for i, story in enumerate(user_story.get_items()):
                try:
                    x = INSTA.download_storyitem(story, target=directory)
                    res_msg = f"""<b>Filename</b> : <code>{story.owner_username}_{story.date_utc}</code>
<b>Username</b> : <code>{story.owner_username}</code>
<b>Downloading</b> : <code>Following Stories</code>
<b>DL Status</b> : <code>{x}</code>
<b>Progress</b> : <code>N/A</code>
<b>Last Updated</b> : <code>{datetime_india()}</code>"""
                    time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                    editMessage(res_msg, msg)
                except Exception as e:
                    LOGGER.info(str(e))
                    editMessage(str(e), msg)
        except Exception as e:
            LOGGER.info(str(e))
            editMessage(str(e), msg)
    cmp_msg = "Successfully Downloaded Posts"
    LOGGER.info("Download Completed-%s", INSTA.context.username)
    editMessage(cmp_msg, msg)
    INSTA.close()
    upload_folder_to_drive(directory, msg, INSTA.context.username, "Stories")
    clean_download(directory)
