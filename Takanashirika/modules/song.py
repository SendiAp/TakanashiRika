import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message, Voice
from youtube_search import YoutubeSearch

from Takanashirika.modules.helper_funcs.chat_status import bot_admin
from Takanashirika import BOT_USERNAME, app
from Takanashirika.Inline import song_download_markup, song_markup
from Takanashirika.utils import get_url
from Takanashirika.utils import get_yt_info_query, get_yt_info_query_slider

loop = asyncio.get_event_loop()


@app.on_message(
    filters.command(["song", f"song@{BOT_USERNAME}"]) & filters.group
)
@bot_admin
async def play(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "You're an __Anonymous Admin__ in this Chat Group!\nRevert back to User Account From Admin Rights."
        )
    await message.delete()
    url = get_url(message)
    if url:
        mystic = await message.reply_text("🔄 Memproses URL... Harap Tunggu!")
        query = message.text.split(None, 1)[1]
        (
            title, 
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(None, get_yt_info_query, query)
        if str(duration_min) == "None":
            return await mystic.edit("Maaf! Ini Video Langsung")
        await mystic.delete()
        buttons = song_download_markup(videoid, message.from_user.id)
        return await message.reply_photo(
            photo=thumb,
            caption=f"📝 **Judul**:[{title}](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n\n⏳**Durasi:** {duration_min} Mins",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            await message.reply_text(
                "**Lagu tidak ditemukan.** Coba cari dengan judul lagu yang lebih jelas, Ketik `/help` bila butuh bantuan."
            )
            return
        mystic = await message.reply_text("🔍 Mencari Permintaan Anda...")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(None, get_yt_info_query, query)
        if str(duration_min) == "None":
            return await mystic.edit("Maaf! Ini Video Langsung")
        await mystic.delete()
        buttons = song_markup(
            videoid, duration_min, message.from_user.id, query, 0
        )
        return await message.reply_photo(
            photo=thumb,
            caption=f"📝 **Judul**:[{title}](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n\n⏳**Durasi:** {duration_min} Mins",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(filters.regex("qwertyuiopasdfghjkl"))
async def qwertyuiopasdfghjkl(_, CallbackQuery):
    print("234")
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = song_download_markup(videoid, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"song_right"))
async def song_right(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, type, query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Cari Musik Anda Sendiri. Anda tidak diperbolehkan menggunakan tombol ini!",
            show_alert=True,
        )
    what = str(what)
    type = int(type)
    if what == "F":
        if type == 9:
            query_type = 0
        else:
            query_type = int(type + 1)
        await CallbackQuery.answer("Mendapatkan Hasil Selanjutnya", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(
            None, get_yt_info_query_slider, query, query_type
        )
        buttons = song_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"📝 **Judul**:[{title}](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n\n⏳**Durasi:** {duration_min} Mins",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        await CallbackQuery.answer("Mendapatkan Hasil Sebelumnya", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(
            None, get_yt_info_query_slider, query, query_type
        )
        buttons = song_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"📝 **Judul**:[{title}](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n\n⏳**Durasi:** {duration_min} Mins",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
