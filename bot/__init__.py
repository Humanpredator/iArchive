import faulthandler
import logging
import os
import socket
import time

import psycopg2
import requests
import telegram.ext as tg
from dotenv import load_dotenv
from instaloader import Instaloader
from psycopg2 import Error
from pyrogram import Client

faulthandler.enable()
socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'a+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(
                        'log.txt'), logging.StreamHandler()],
                    datefmt='%d-%b-%y %H:%M:%S',
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
    DOWNLOAD_STATUS_UPDATE_INTERVAL = int(
        getConfig('DOWNLOAD_STATUS_UPDATE_INTERVAL'))
    OWNER_ID = int(getConfig('OWNER_ID'))
    TELEGRAM_API = getConfig('TELEGRAM_API')
    TELEGRAM_HASH = getConfig('TELEGRAM_HASH')
except:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)
try:
    DB_URI = getConfig('DATABASE_URL')
    if len(DB_URI) == 0:
        raise KeyError
except:
    DB_URI = None
if DB_URI is not None:
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        sql = "SELECT * from users;"
        cur.execute(sql)
        rows = cur.fetchall()  # returns a list ==> (uid, sudo)
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
app = Client('Insta_Scrap', api_id=int(TELEGRAM_API),
             api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN, )

# IG CONFIG
S = "0"
STATUS = set(int(x) for x in S.split())
INSTA = Instaloader()

# Generate Telegraph Token
# sname = ''.join(random.SystemRandom().choices(string.ascii_letters, k=9))
# LOGGER.info("Generating TELEGRAPH_TOKEN using '" + sname + "' name")
# telegraph = Telegraph()
# telegraph_token = telegraph.create_account(short_name=sname).get_access_token()


try:
    IGNORE_PENDING_REQUESTS = getConfig("IGNORE_PENDING_REQUESTS")
    IGNORE_PENDING_REQUESTS = IGNORE_PENDING_REQUESTS.lower() == 'true'
except:
    IGNORE_PENDING_REQUESTS = False
try:
    INDEX_URL = getConfig("INDEX_URL")
except:
    INDEX_URL = "drive.teamplague.com"

try:
    TG_UPLOAD = getConfig("TG_UPLOAD")
    TG_UPLOAD = TG_UPLOAD.lower() == 'true'
except:
    TG_UPLOAD = False

updater = tg.Updater(token=BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher
