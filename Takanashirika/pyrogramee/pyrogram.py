import logging
from pyrogram import Client
from Takanashirika.conf import get_int_key, get_str_key
from Takanashirika import TELETHON_ID, TELETHON_HASH, TOKEN

TOKEN = get_str_key("TOKEN", required=True)
TELETHON_ID = get_int_key("TELETHON_ID", required=True)
TELETHON_HASH = get_str_key("TELETHON_HASH", required=True)
session_name = TOKEN.split(":")[0]
pbot = Client(
    session_name,
    api_id=TELETHON_ID,
    api_hash=TELETHON_HASH,
    bot_token=TOKEN,
)

# disable logging for pyrogram [not for ERROR logging]
logging.getLogger("pyrogram").setLevel(level=logging.ERROR)

pbot.start()
