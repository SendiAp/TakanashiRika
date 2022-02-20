import asyncio
import random
import time
from datetime import datetime

import redis
from speedtest import Speedtest

from Takanashirika import OWNER_NAME, bot

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

    while count < 4:
        count += 50
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@bot.on(outgoing=True, pattern='^.ping(?: |$)(.*)')
async def redis(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("__Pinging.__")
    await pong.edit("__Pinging..__")
    await pong.edit("__Pinging...__")
    await pong.edit("__Pinging....__")
    await pong.edit("😷")
    await asyncio.sleep(2)
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**Takanashirika - Project!!🎈**\n**Pinger** : %sms\n**Bot Uptime** : {uptime}🕛" % (duration))
