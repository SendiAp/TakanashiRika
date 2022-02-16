import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)
from youtube_search import YoutubeSearch

from Takanashirika import BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN, app
from Takanashirika.Decorators.permission import PermissionCheck
from Takanashirika.Inline import song_download_markup, song_markup
from Takanashirika.Utilities.url import get_url
from Takanashirika.Utilities.youtube import (get_yt_info_query,
                                     get_yt_info_query_slider)

loop = asyncio.get_event_loop()
