import os
from os import path

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from telegram import InlineKeyboardMarkup

from bot import parent_id, LOGGER
from bot.helper.ext_utils.bot_utils import fcount, get_readable_file_size, fsize, progress_bar
from bot.helper.telegram_helper import button_build
from bot.helper.telegram_helper.message_utils import editMessage

DRIVE = parent_id


# gdrive upload function
def gup(dir: str, m, username, fetch):
    # Route the modules
    global folderid, foldername

    # Main gfolder id where store all the ig profile archive
    gFolderID = DRIVE  # Gdrive Folder id to store all the user posts conatining files  Folder
    directory = dir  # Route the main dir to function directory variables

    gauth = GoogleAuth()
    # check if the credentials file exists
    if path.exists("credentials.json"):
        gauth.LoadCredentialsFile("credentials.json")
        if gauth.access_token_expired:
            gauth.Refresh()
        else:
            pass

        drive = GoogleDrive(gauth)

        count = 0
        editMessage(
            f"Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.", m)

        # Getting Gdrive Details
        # Get list the Files in Given gUserFolderID
        gListFolderstr = "\'" + gFolderID + "\'" + " in parents and trashed=false"
        gfile_list = drive.ListFile({'q': gListFolderstr, 'supportsAllDrives': True,
                                     'includeItemsFromAllDrives': True}).GetList()  # List the Files using gListFolderstr
        if not gfile_list:
            folderid = None
            foldername = None
        else:
            # Get All the folder inside the given main gfolder
            for glistfile in gfile_list:  # List and store  files in glistfile to get title or id
                LOGGER.info(
                    f'All Folder Title in Given GDrive Folder ID: {glistfile["title"]}')
                # Intial check Whether the user dir is already present.
                if glistfile['title'] == dir.split('/')[1]:
                    # Store already presented user gfolder id
                    folderid = glistfile['id']
                    # Store already presented user gfolder title
                    foldername = glistfile['title']
                    break  # Break the loop
                folderid = None
                foldername = None

        # set folder variables
        # Store already presented user gfolder id to the matchedFolderID
        matchedFolderID = folderid
        # Store already presented user gfolder title to matchedFoldername
        matchedFoldername = foldername

        # upload section
        if matchedFoldername == dir.split('/')[1]:  # validate Again
            LOGGER.info(
                f'The matched Folder is: {matchedFoldername} : {matchedFolderID}')

            # compare files in matchFolderId with Local Files
            gcmpListFolderstr = "\'" + matchedFolderID + "\'" + \
                                " in parents and trashed=false"  # get list the Files in Given MatchedFolderID
            gcmpfile_list = drive.ListFile({'q': gcmpListFolderstr, 'supportsAllDrives': True,
                                            'includeItemsFromAllDrives': True}).GetList()  # list the Files using gListFolderstr

            # get list Of Files in both Dir
            for gfilelist in gcmpfile_list:
                # list files in Gdrive dir in gfilelist
                LOGGER.info(
                    f'The Matched Drive File list are: {gfilelist["title"]}')
            # list files in Local dir
            for localfilelist in os.listdir(directory):
                # list files in Local dir in localfilelist
                LOGGER.info(
                    f'The Matched Local Dir File list are: {localfilelist}')

                # overwrite the files if Exists by deletin existing file
                try:
                    for file1 in gcmpfile_list:
                        if file1['title'] == localfilelist:
                            tfile = file1['title']
                            file1.Delete()
                            LOGGER.info(
                                f'File {tfile} is Successfully deleted')
                except FileNotFoundError:
                    pass

                # Upload the Deleted Files
                # filename allocation
                filename = os.path.join(directory, localfilelist)
                # where the files will be uploaded
                gfile = drive.CreateFile(
                    {'parents': [{'id': matchedFolderID}], 'title': localfilelist})
                gfile.SetContentFile(filename)  # set gfilename
                count += 1
                msg = f'''
<b>Uploading: </b><code>{progress_bar(count, fcount(dir))}</code>                
<b>Files: </b><code>0{count}/{fcount(dir)}</code>
<b>File Name: </b><code>{localfilelist}</code>
<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>
'''
                gfile.Upload()  # upload
                try:
                    editMessage(msg, m)
                except Exception as e:
                    LOGGER.info(e)
                LOGGER.info(f'File {localfilelist} is Successfully Uploaded')
            msg = f'''
<b>Upload Completed: </b><code>{username}</code>
<b>Directory: </b><code>{dir}</code>
<b>Total Files: </b><code>{fcount(dir)}</code>
<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>
<b>Type: </b><code>{fetch}</code>
'''
            buttons = button_build.ButtonMaker()
            buttons.buildbutton('Drive Link', f'https://drive.google.com/drive/u/1/folders/{matchedFolderID}')
            markup = InlineKeyboardMarkup(buttons.build_menu(1))
            LOGGER.info(f'Uploaded Completed: {username}')
            editMessage(msg, m, markup)
            return True
        # Create folder for the title dir
        folder_metadata = {'title': dir.split('/')[1], "parents": [
            {"id": gFolderID}], 'mimeType': 'application/vnd.google-apps.folder'}  # meta data for gfolder
        gFolderCreate = drive.CreateFile(
            folder_metadata)  # set gfolderename
        gFolderCreate.Upload()  # upload

        # Get new folder id
        newgFolderID = gFolderCreate['id']
        LOGGER.info(f'{gFolderCreate["title"]} -->Successfully created')

        # Upload all the new files to the newly created gfolder
        for localfilelist in os.listdir(directory):
            # filename allocation
            filename = os.path.join(directory, localfilelist)
            # where the files will be uploaded
            gfile = drive.CreateFile(
                {'parents': [{'id': newgFolderID}], 'title': localfilelist})
            gfile.SetContentFile(filename)  # set gfilename
            count += 1
            msg = f'''
<b>Uploading: </b><code>{progress_bar(count, fcount(dir))}</code>                
<b>Files: </b><code>0{count}/{fcount(dir)}</code>
<b>File Name: </b><code>{localfilelist}</code>
<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>
'''
            gfile.Upload()  # upload
            try:
                editMessage(msg, m)
            except Exception as e:
                LOGGER.info(e)
            LOGGER.info(f'File {localfilelist} is Successfully Uploaded')
        LOGGER.info(f'All Files was Successfully Uploaded')
        msg = f'''
<b>Upload Completed: </b><code>{username}</code>
<b>Directory: </b><code>{dir}</code>
<b>Total Files: </b><code>{fcount(dir)}</code>
<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>
<b>Type: </b><code>{fetch}</code>
'''
        buttons = button_build.ButtonMaker()
        buttons.buildbutton('Drive Link', f'https://drive.google.com/drive/u/1/folders/{matchedFolderID}')
        markup = InlineKeyboardMarkup(buttons.build_menu(1))
        LOGGER.info(f'Uploaded Completed: {username}')
        editMessage(msg, m, markup)
        return True
    editMessage("No Credentials File Found..Upload stopped", m)
    LOGGER.warning("No Credentials File Found..Upload stopped")
