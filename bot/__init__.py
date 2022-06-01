import logging
import os
import time
import random
import string
import requests
import time
import telegram.ext as tg
from dotenv import load_dotenv
from pyrogram import Client
from telegraph import Telegraph
import psycopg2
from psycopg2 import Error
import socket
import faulthandler
from instaloader import Instaloader


faulthandler.enable()

socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

CONFIG_FILE_URL = os.environ.get('CONFIG_FILE_URL', None)
if CONFIG_FILE_URL is not None:
    res = requests.get(CONFIG_FILE_URL)
    if res.status_code == 200:
        with open('config.env', 'wb+') as f:
            f.write(res.content)
            f.close()
    else:
        logging.error(res.status_code)

load_dotenv('config.env')


def getConfig(name: str):
    return os.environ[name]

def mktable():
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        sql = "CREATE TABLE users (uid bigint, sudo boolean DEFAULT FALSE);"
        cur.execute(sql)
        conn.commit()
        logging.info("Table Created!")
    except Error as e:
        logging.error(e)
        exit(1)

BOT_TOKEN = None
# Stores list of users and chats the bot is authorized to use in
AUTHORIZED_CHATS = set()
SUDO_USERS = set()

if os.path.exists('authorized_chats.txt'):
    with open('authorized_chats.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            AUTHORIZED_CHATS.add(int(line.split()[0]))
if os.path.exists('sudo_users.txt'):
    with open('sudo_users.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            SUDO_USERS.add(int(line.split()[0]))
try:
    achats = getConfig('AUTHORIZED_CHATS')
    achats = achats.split(" ")
    for chats in achats:
        AUTHORIZED_CHATS.add(int(chats))
except:
    pass
try:
    schats = getConfig('SUDO_USERS')
    schats = schats.split(" ")
    for chats in schats:
        SUDO_USERS.add(int(chats))
except:
    pass
try:
    BOT_TOKEN = getConfig('BOT_TOKEN')
    parent_id = getConfig('GDRIVE_FOLDER_ID')
    DOWNLOAD_STATUS_UPDATE_INTERVAL = int(getConfig('DOWNLOAD_STATUS_UPDATE_INTERVAL'))
    OWNER_ID = int(getConfig('OWNER_ID'))
    TELEGRAM_API = getConfig('TELEGRAM_API')
    TELEGRAM_HASH = getConfig('TELEGRAM_HASH')
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)
try:
    DB_URI = getConfig('DATABASE_URL')
    if len(DB_URI) == 0:
        raise KeyError
except KeyError:
    DB_URI = None
if DB_URI is not None:
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        sql = "SELECT * from users;"
        cur.execute(sql)
        rows = cur.fetchall()  #returns a list ==> (uid, sudo)
        for row in rows:
            AUTHORIZED_CHATS.add(row[0])
            if row[1]:
                SUDO_USERS.add(row[0])
    except Error as e:
        if 'relation "users" does not exist' in str(e):
            mktable()
        else:
            LOGGER.error(e)
            exit(1)
    finally:
        cur.close()
        conn.close()

LOGGER.info("Generating USER_SESSION_STRING")
app = Client('insta_scrap', api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN,)

#IG CONFIG
S = "0"
STATUS = set(int(x) for x in (S).split())
L=Instaloader()


# Generate Telegraph Token
sname = ''.join(random.SystemRandom().choices(string.ascii_letters, k=8))
LOGGER.info("Generating TELEGRAPH_TOKEN using '" + sname + "' name")
telegraph = Telegraph()
telegraph.create_account(short_name=sname)
telegraph_token = telegraph.get_access_token()

try:
    IGNORE_PENDING_REQUESTS = getConfig("IGNORE_PENDING_REQUESTS")
    IGNORE_PENDING_REQUESTS = IGNORE_PENDING_REQUESTS.lower() == 'true'
except KeyError:
    IGNORE_PENDING_REQUESTS = False
try:
    INDEX_URL=getConfig("INDEX_URL")
except:
    INDEX_URL = False

try:
    TG_UPLOAD = getConfig("TG_UPLOAD")
    TG_UPLOAD = TG_UPLOAD.lower() == 'true'
except:
    TG_UPLOAD = False

updater = tg.Updater(token=BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher
