#import Modules
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os,time
import shutil
from bot import LOGGER,parent_id
from os import path
from pyrogram import *
from bot.helper.ext_utils.bot_utils import fcount, get_readable_file_size
from bot.helper.telegram_helper.message_utils import *

DRIVE= parent_id

#gdrive upload function
def gup(dir, m):
    #Route the modules
    gauth = GoogleAuth()
    #check if the credentials file exists
    if path.exists("credentials.json"):
        gauth.LoadCredentialsFile("credentials.json")
        if gauth.access_token_expired:
            gauth.Refresh()
        else:
            pass
    
        drive = GoogleDrive(gauth)

        count = 0
        editMessage(f"Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.",m)
        #Main gfolder id where store all the ig profile archive 
        gFolderID= DRIVE#Gdrive Folder id to store all the user posts conatining files  Folder
        directory = dir #Route the main dir to function directory variables
        
        #Getting Gdrive Details
        gListFolderstr = "\'" + gFolderID + "\'" + " in parents and trashed=false" #Get list the Files in Given gUserFolderID 
        gfile_list = drive.ListFile({'q': gListFolderstr,'supportsAllDrives': True,'includeItemsFromAllDrives': True}).GetList() #List the Files using gListFolderstr
        if gfile_list == []:
            folderid = None
            foldername = None
        else:
            #Get All the folder inside the given main gfolder  
            for glistfile in gfile_list: #List and store  files in glistfile to get title or id
                LOGGER.info(f'All Folder Title in Given GDrive Folder ID: {glistfile["title"]}')
                if glistfile['title'] == dir: #Intial check Whether the user dir is already present.
                    folderid = glistfile ['id'] #Store already presented user gfolder id
                    foldername = glistfile ['title'] #Store already presented user gfolder title
                    break #Break the loop
                else:
                    folderid = None
                    foldername = None

        #set folder variables
        matchedFolderID = folderid #Store already presented user gfolder id to the matchedFolderID
        matchedFoldername = foldername #Store already presented user gfolder title to matchedFoldername
        
        #upload section
        if matchedFoldername == dir: #validate Again
            LOGGER.info(f'The matched Folder is: {matchedFoldername} : {matchedFolderID}')
            
            
            #compare files in matchFolderId with Local Files
            gcmpListFolderstr = "\'" +  matchedFolderID + "\'" + " in parents and trashed=false" #get list the Files in Given MatchedFolderID
            gcmpfile_list = drive.ListFile({'q': gcmpListFolderstr,'supportsAllDrives': True,'includeItemsFromAllDrives': True}).GetList()#list the Files using gListFolderstr
            
            #get list Of Files in both Dir
            for gfilelist in gcmpfile_list: 
                LOGGER.info(f'The Matched Drive File list are: {gfilelist["title"]}') #list files in Gdrive dir in gfilelist
            for localfilelist in os.listdir(directory): #list files in Local dir 
                LOGGER.info(f'The Matched Local Dir File list are: {localfilelist}') #list files in Local dir in localfilelist
                
                #overwrite the files if Exists by deletin existing file
                try:
                    for file1 in gcmpfile_list:
                        if file1['title'] == localfilelist:
                            tfile = file1['title']
                            file1.Delete()
                            LOGGER.info(f'File {tfile} is Successfully deleted')                                  
                except:
                    pass
                
            #Upload the Deleted Files
                filename = os.path.join(directory, localfilelist) #filename allocation
                gfile = drive.CreateFile({'parents' : [{'id' : matchedFolderID}], 'title' : localfilelist}) #where the files will be uploaded
                gfile.SetContentFile(filename) #set gfilename 
                count += 1
                msg = f'<b>Uploading: </b><code>0{count}</code>\n<b>File Name: </b><code>{localfilelist}</code>\n<b>Total Files: </b><code>{fcount(dir)}</code>\n<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>'
                gfile.Upload() #upload
                try:
                    time.sleep(3)
                    editMessage(msg,m)
                except:
                    pass
                LOGGER.info(f'File {localfilelist} is Successfully Uploaded') 
            gid = (f'https://drive.google.com/drive/u/1/folders/{matchedFolderID}')
            msg = f'<b>Uploaded: </b><code>{dir}</code>\n<b>Total Files: </b><code>{fcount(dir)}</code>\n<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>\n<b>Drive Link: </b><code>{gid}</code>'
            LOGGER.info(gid)
            editMessage(msg,m)
        
    #else part To Create New GFolde for the Dir And Upload the Files...!
        else:
            #Create folder for the title dir 
            folder_metadata = {'title' : dir,"parents":  [{"id": gFolderID}], 'mimeType' : 'application/vnd.google-apps.folder'} #meta data for gfolder
            gFolderCreate = drive.CreateFile(folder_metadata) #set gfolderename
            gFolderCreate.Upload() #upload
            
            #Get new folder id
            newgFolderID = gFolderCreate['id']
            LOGGER.info(f'{gFolderCreate["title"]} -->Successfully created')

            #Upload all the new files to the newly created gfolder
            for localfilelist in os.listdir(directory):
                filename = os.path.join(directory, localfilelist) #filename allocation
                gfile = drive.CreateFile({'parents' : [{'id' : newgFolderID}], 'title' : localfilelist}) #where the files will be uploaded
                gfile.SetContentFile(filename) #set gfilename
                count += 1
                msg = f'<b>Uploading: </b><code>0{count}</code>\n<b>File Name: </b><code>{localfilelist}</code>\n<b>Total Files: </b><code>{fcount(dir)}</code>\n<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>'
                gfile.Upload() #upload
                try:
                    time.sleep(3)
                    editMessage(msg,m)
                except:
                    pass
                LOGGER.info(f'File {localfilelist} is Successfully Uploaded') 
            LOGGER.info(f'All Files was Successfully Uploaded')
            gid = (f'https://drive.google.com/drive/u/1/folders/{newgFolderID}')
            LOGGER.info(gid)
            msg = f'<b>Uploaded Completed: </b><code>{dir}</code>\n<b>Total Files: </b><code>{fcount(dir)}</code>\n<b>Folder Size: </b><code>{get_readable_file_size(fsize(dir))}</code>\n<b>Drive Link: </b><code>{gid}</code>'
            editMessage(msg,m)
        shutil.rmtree(dir)
        LOGGER.info(f'Clearing Downloads: {dir}')
    else:
        LOGGER.warning("No Credentials File Found..Upload stopped")







def fsize(dir):
    # assign size
    size = 0
    
    # assign folder path
    Folderpath = dir 
    
    # get size
    for ele in os.scandir(Folderpath):
        size+=os.stat(ele).st_size
        
    return size

