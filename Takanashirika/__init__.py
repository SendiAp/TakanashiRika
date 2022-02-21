import logging
import os
import sys
import time
import aiohttp
import telegram.ext as tg
import spamwatch
from pyrogram import Client, errors
from telethon import TelegramClient
from telethon.sessions import StringSession
from aiohttp import ClientSession
from Python_ARQ import ARQ
from telethon.sync import TelegramClient

StartTime = time.time()


def get_user_list(__init__, key):
    with open("{}/Takanashirika/{}".format(os.getcwd(), __init__), "r") as json_file:
        return json.load(json_file)[key]


# enable logging
FORMAT = "[TakanashiRika] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)
LOGGER.info("Takanashirika mulai. | Sendi Projects. | Licensed under GPLv3.")
LOGGER.info("Tidak berafiliasi dengan Shie Hashaikai atau Penjahat dengan cara apa pun.")
LOGGER.info("Proyek dipertahankan by: github.com/SendiAp (t.me/pikyus1)")

VERSION = "7.0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    sys.exit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)

    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP', None)
    OWNER_NAME = os.environ.get("OWNER_NAME", None)

    try:
        SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = {int(x) for x in os.environ.get("SUPPORT_USERS", "").split()}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        SPAMMERS = {int(x) for x in os.environ.get("SPAMMERS", "").split()}
    except ValueError:
        raise Exception("Your spammers users list does not contain valid integers.")

    try:
        WHITELIST_USERS = {int(x) for x in os.environ.get("WHITELIST_USERS", "").split()}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")


    GBAN_LOGS = os.environ.get('GBAN_LOGS', None)
    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")

    DB_URI = os.environ.get('DATABASE_URL')
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    ARQ_API_URL = "https://thearq.tech"
    ARQ_API_KEY = "KCSRHS-PQHEIE-PKEMJV-ABJKYU-ARQ"
    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    DONATION_LINK = os.environ.get('DONATION_LINK')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', True))  
    STRICT_GMUTE = bool(os.environ.get('STRICT_GMUTE', True))
    WORKERS = int(os.environ.get('WORKERS', 8))
    BAN_STICKER = os.environ.get('BAN_STICKER', 'CAADAgADOwADPPEcAXkko5EB3YGYAg')
    KICK_STICKER = os.environ.get('KICK_STICKER', 'CAACAgQAAxkBAAEEUYRelpQPawgDzWA0kbOucFeqf8xdAQACigAD_OoIAAF1UohdVTwBsRgE')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', 'V7NS1NBFEL4X24L6')
    CASH_API_KEY = os.environ.get('CASH_API_KEY', None)
    TIME_API_KEY = os.environ.get('TIME_API_KEY', '2AS711XS1O9B')
    WALL_API = os.environ.get('WALL_API',None)
    LASTFM_API_KEY = os.environ.get('LASTFM_API_KEY',None)
    LYDIA_API = os.environ.get('LYDIA_API', '632740cd2395c73b58275b54ff57a02b607a9f8a4bbc0e37a24e7349a098f95eaa6569e22e2d90093e9c1a9cc253380a218bfc2b7af2e407494502f6fb76f97e')
    API_WEATHER  = os.environ.get('API_OPENWEATHER',None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)    
    SW_API = os.environ.get('SW_API', None)
    TELETHON_ID = int(os.environ.get("APP_ID", None))
    TELETHON_HASH = os.environ.get("APP_HASH", None)
    AI_API_KEY = os.environ.get("AI_API_KEY", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    LOGGRUB = = os.environ.get("LOGGRUB", None)

else:
    from Takanashirika.config import Development as Config
    TOKEN = Config.API_KEY

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    MESSAGE_DUMP = Config.MESSAGE_DUMP
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or []) 
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or []) 
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or []) 
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        SPAMMERS = set(int(x) for x in Config.SPAMMERS or []) 
    except ValueError:
        raise Exception("Your spammers users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or []) 
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    GBAN_LOGS = Config.GBAN_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    HEROKU_API_KEY = Config.HEROKU_API_KEY
    HEROKU_APP_NAME = Config.HEROKU_APP_NAME
    ARQ_API = Config.ARQ_API_KEY
    ARQ_API_URL = Config.ARQ_API_URL
    BOT_USERNAME = Config.BOT_USERNAME
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    STRICT_GMUTE = Config.STRICT_GMUTE
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    KICK_STICKER = Config.KICK_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    LASTFM_API_KEY = Config.LASTFM_API_KEY
    LYDIA_API = Config.LYDIA_API
    API_OPENWEATHER = Config.API_OPENWEATHER
    SW_API = Config.SW_API
    TELETHON_HASH = Config.TELETHON_HASH
    TELETHON_ID = Config.TELETHON_ID
    UPDATES_CHANNEL = Config.UPDATES_CHANNEL
    LOG_CHANNEL = Config.LOG_CHANNEL
    AI_API_KEY = Config.AI_API_KEY
    STRING_SESSION = Config.STRING_SESSION
    LOGGRUB = Config.LOGGRUB

# Don't Remove my ID from DEV and SUDO list..It Took many months to set up a bot like this..I have added many features in this bot ..by @xflicks     
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(1307579425)
DEV_USERS.add(1307579425)
SUDO_USERS.add(OWNER_ID)
SUDO_USERS.add(1307579425)
SUDO_USERS.add(1307579425)

updater = tg.Updater(TOKEN, workers=WORKERS)
dispatcher = updater.dispatcher
print("[TakanashiRika]: TELETHON CLIENT STARTING")
telethn = TelegramClient("Takanashirika", api_id=TELETHON_ID, api_hash=TELETHON_HASH)
print("[TakanashiRika]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
print("[TakanashiRika]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
pbot = Client("Takanashirika", api_id=TELETHON_ID, api_hash=TELETHON_HASH, bot_token=TOKEN)

apps = []
apps.append(pbot)

SUDO_USERS = list(SUDO_USERS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SPAMMERS = list(SPAMMERS)

# SpamWatch
if SW_API == "None":
    spam_watch = None
    LOGGER.warning("SpamWatch API key is missing! Check your config var")
else:
    try:
        spam_watch = spamwatch.Client(SW_API)
    except Exception:
        spam_watch = None
        
if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION), TELETHON_ID, TELETHON_HASH)
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("Takanashirika", TELETHON_ID, TELETHON_HASH)

# Load at end to ensure all prev variables have been set
from Takanashirika.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler, CustomMessageHandler

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

def spamfilters(text, user_id, chat_id):
    #print("{} | {} | {}".format(text, user_id, chat_id))
    if int(user_id) in SPAMMERS:
        print("This user is a spammer!")
        return True
    else:
        return False
