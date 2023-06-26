import os
import pickle

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from telegram import InlineKeyboardMarkup

from bot import LOGGER, parent_id, TG_UPLOAD, bot
from bot.helper.ext_utils.bot_utils import (
    fcount,
    fsize,
    get_readable_file_size,
    progress_bar,
)
from bot.helper.tg_utils import button_build
from bot.helper.tg_utils.message_utils import editMessage
from bot.helper.tg_utils.tg_upload import tgup

DRIVE = parent_id


def upload_folder_to_drive(dir: str, m, username, fetch, folder_id=None):
    if not os.path.isdir(dir):
        editMessage(
            "Empty Directory, Upload Skips...!",
            m,
        )
    count = 0
    editMessage(
        "Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.",
        m,
    )

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            editMessage("No Token File Found..Upload stopped", m)

    drive_service = build('drive', 'v3', credentials=creds)

    folder_name = os.path.basename(dir)
    if not folder_id:
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{DRIVE}' in parents"
        existing_folders = drive_service.files().list(q=query, fields='files(id)').execute().get('files', [])
        if existing_folders:
            folder_id = existing_folders[0]['id']
        else:
            folder_metadata = {'name': folder_name, 'parents': [DRIVE],
                               'mimeType': 'application/vnd.google-apps.folder'}
            folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
            folder_id = folder.get('id')

    for file_name in os.listdir(dir):
        file_path = os.path.join(dir, file_name)
        if os.path.isdir(file_path):
            upload_folder_to_drive(file_path, m, username, fetch, folder_id=folder_id)
            continue

        try:
            query = f"name='{file_name}' and trashed=false and '{folder_id}' in parents"
            existing_files = drive_service.files().list(q=query, fields='files(id)').execute().get('files', [])
            if existing_files:
                file_metadata = {'name': file_name, 'addParents': [folder_id]}
                media = MediaFileUpload(file_path, resumable=True)
                file_id = existing_files[0]['id']
                LOGGER.info(f"File {file_name} already exists")
                file = drive_service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()
                LOGGER.info(f"File {file_name} is Successfully Updated")
            else:
                file_metadata = {'name': file_name, 'parents': [folder_id]}
                media = MediaFileUpload(file_path, resumable=True)
                file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                LOGGER.info(f"File {file_name} is Successfully Uploaded")

            count += 1
            msg = f"""
<b>Uploading: </b><code>{progress_bar(count, fcount(dir))}</code>                
<b>Files: </b><code>0{count}/{fcount(dir)}</code>
<b>File Name: </b><code>{file_name}</code>
<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>
"""
            editMessage(msg, m)
        except HttpError as error:
            if error.resp.status == 409:
                query = f"name='{file_name}' and trashed=false and '{folder_id}' in parents"
                existing_files = drive_service.files().list(q=query, fields='files(id)').execute().get('files', [])
                if existing_files:
                    file_metadata = {'name': file_name, 'addParents': [folder_id]}
                    media = MediaFileUpload(file_path, resumable=True)
                    file_id = existing_files[0]['id']
                    file = drive_service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()
                    LOGGER.info(f"File {file_name} is Successfully Updated")
                    count += 1
                    msg = f"""
<b>Uploading: </b><code>{progress_bar(count, fcount(dir))}</code>                
<b>Files: </b><code>0{count}/{fcount(dir)}</code>
<b>File Name: </b><code>{file_name}</code>
<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>
"""
                    editMessage(msg, m)
                else:
                    msg = f"An Error Occurred: {error}"
                    editMessage(msg, m)
            else:
                msg = f"An Error Occurred: {error}"
                editMessage(msg, m)

    LOGGER.info("All Files were Successfully Uploaded")
    msg = f"""
<b>Upload Completed: </b><code>{username}</code>
<b>Directory: </b><code>{dir}</code>
<b>Total Files: </b><code>{fcount(dir)}</code>
<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>
<b>Type: </b><code>{fetch}</code>
"""
    buttons = button_build.ButtonMaker()
    buttons.buildbutton(
        "Drive Link",
        f"https://drive.google.com/drive/u/1/folders/{folder_id}",
    )
    markup = InlineKeyboardMarkup(buttons.build_menu(1))
    LOGGER.info(f"Upload Completed: {username}")
    editMessage(msg, m, markup)
    if TG_UPLOAD:
        m = bot.send_message(
            chat_id=m.chat.id,
            text="Uploading to Telegram...",
            reply_to_message_id=m.message_id,
        )
        tgup(m, dir)
    return True
