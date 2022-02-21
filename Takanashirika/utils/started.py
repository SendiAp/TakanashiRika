import io
import re
import time
from datetime import datetime
from os import remove

from Takanashirika.modules.sql.bot_starters import (
    add_starter_to_db,
    get_all_starters,
    get_starter_details,
)

from Takanashirika import LOGGRUB, SUDO_USERS, OWNER_ID, pbot

async def check_bot_started_users(pbot, event):
    if user.id == OWNER_ID:
        return
    check = get_starter_details(user.id)
    if check is None:
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        notification = f"🔮 **#BOT_START**\n**First Name:** {_format.mentionuser(user.first_name , user.id)} \
                \n**User ID: **`{user.id}`\
                \n**Action: **Telah Memulai saya."
    else:
        start_date = check.date
        notification = f"🔮 **#BOT_RESTART**\n**First Name:** {_format.mentionuser(user.first_name , user.id)}\
                \n**ID: **`{user.id}`\
                \n**Action: **Telah Me-Restart saya"
    try:
        add_starter_to_db(user.id, get_display_name(user), start_date, user.username)
    except Exception as e:
        LOGS.error(str(e))
    if LOGGRUB:
        await event.client.send_message(LOGGRUB, notification)
