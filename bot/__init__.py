"""Telegram Bot for downloading Instagram media"""
import faulthandler
import logging
import os
import socket
import sys
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

if os.path.exists("log.txt"):
    with open("log.txt", "a+", encoding="UTF-8") as file:
        file.truncate(0)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"),
              logging.StreamHandler()],
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

CONFIG_FILE_URL = os.environ.get("CONFIG_FILE_URL")
if CONFIG_FILE_URL is not None:
    res = requests.get(CONFIG_FILE_URL, timeout=200)
    if res.status_code == 200:
        with open("config.env", "wb+") as f:
            f.write(res.content)
            f.close()
    else:
        logging.error(res.status_code)

load_dotenv("config.env")


def get_config(name: str):
    """Get config from environment variables or config file"""
    return os.environ[name]


def mktable():
    """Create table in database"""
    try:
        connection = psycopg2.connect(DB_URI)
        cursor = connection.cursor()
        create_query = "CREATE TABLE users (uid bigint, sudo boolean DEFAULT FALSE);"
        cursor.execute(create_query)
        connection.commit()
        logging.info("Table Created!")
    except Error as error:
        logging.error(error)
        sys.exit(1)


BOT_TOKEN = None
# Stores list of users and chats the bot is authorized to use in
AUTHORIZED_CHATS = set()
SUDO_USERS = set()

if os.path.exists("authorized_chats.txt"):
    with open("authorized_chats.txt", "r+", encoding="UTF-8") as file:
        lines = file.readlines()
        for line in lines:
            AUTHORIZED_CHATS.add(int(line.split()[0]))
if os.path.exists("sudo_users.txt"):
    with open("sudo_users.txt", "r+", encoding="UTF-8") as file:
        lines = file.readlines()
        for line in lines:
            SUDO_USERS.add(int(line.split()[0]))
try:
    achats = get_config("AUTHORIZED_CHATS")
    achats = achats.split(" ")
    for chats in achats:
        AUTHORIZED_CHATS.add(int(chats))
except ValueError:
    pass
try:
    schats = get_config("SUDO_USERS")
    schats = schats.split(" ")
    for chats in schats:
        SUDO_USERS.add(int(chats))
except ValueError:
    pass
try:
    BOT_TOKEN = get_config("BOT_TOKEN")
    parent_id = get_config("GDRIVE_FOLDER_ID")
    DOWNLOAD_STATUS_UPDATE_INTERVAL = int(
        get_config("DOWNLOAD_STATUS_UPDATE_INTERVAL"))
    OWNER_ID = int(get_config("OWNER_ID"))
    TELEGRAM_API = get_config("TELEGRAM_API")
    TELEGRAM_HASH = get_config("TELEGRAM_HASH")
except KeyError:
    LOGGER.error("One or more env variables missing! Exiting now")
    sys.exit(1)
try:
    DB_URI = get_config("DATABASE_URL")
    if len(DB_URI) == 0:
        raise KeyError
except KeyError:
    DB_URI = None
if DB_URI is not None:
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        SELECT_QUERY = "SELECT * from users;"
        cur.execute(SELECT_QUERY)
        rows = cur.fetchall()  # returns a list ==> (uid, sudo)
        for row in rows:
            AUTHORIZED_CHATS.add(row[0])
            if row[1]:
                SUDO_USERS.add(row[0])
        cur.close()
        conn.close()
    except Error as e:
        if 'relation "users" does not exist' in str(e):
            mktable()
        else:
            LOGGER.error(e)
            sys.exit(1)

LOGGER.info("Generating USER_SESSION_STRING")
app = Client(
    "Insta_Scrap",
    api_id=int(TELEGRAM_API),
    api_hash=TELEGRAM_HASH,
    bot_token=BOT_TOKEN,
)

# IG CONFIG
S = "0"
STATUS = {int(x) for x in S.split()}
INSTA = Instaloader()

# Generate Telegraph Token
# sname = ''.join(random.SystemRandom().choices(string.ascii_letters, k=9))
# LOGGER.info("Generating TELEGRAPH_TOKEN using '" + sname + "' name")
# telegraph = Telegraph()
# telegraph_token = telegraph.create_account(short_name=sname).get_access_token()

try:
    IGNORE_PENDING_REQUESTS = get_config("IGNORE_PENDING_REQUESTS")
    IGNORE_PENDING_REQUESTS = IGNORE_PENDING_REQUESTS.lower() == "true"
except KeyError:
    IGNORE_PENDING_REQUESTS = False
try:
    INDEX_URL = get_config("INDEX_URL")
except KeyError:
    INDEX_URL = "drive.teamplague.com"

try:
    TG_UPLOAD = get_config("TG_UPLOAD")
    TG_UPLOAD = TG_UPLOAD.lower() == "true"
except KeyError:
    TG_UPLOAD = False

updater = tg.Updater(token=BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher
