import asyncio
from configs import Config
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from Takanashirika import BOT_USERNAME, TOKEN, API_ID, API_HASH, UPDATES_CHANNEL, LOG_CHANNEL

TRBot = Client(Config.BOT_USERNAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)


async def handle_force_subscribe(bot, cmd):
    try:
        invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return 400
    try:
        user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
                    ]
                ]
            ),
            parse_mode="markdown"
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
            parse_mode="markdown",
            disable_web_page_preview=True
        )
        return 400


@TRBot.on_message(filters.command(["start", "help"]) & filters.private)
async def HelpForcesub(bot, cmd):
	if not await bot.send_message(
			Config.LOG_CHANNEL,
			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
		)
	if Config.UPDATES_CHANNEL:
		fsub = await handle_force_subscribe(bot, cmd)
		if fsub == 400:
			return
	await cmd.reply_text(
		parse_mode="Markdown",
		reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/AbirHasan2005"), InlineKeyboardButton("Support Group", url="https://t.me/DevsZone")], [InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")], [InlineKeyboardButton("Source Code", url="https://github.com/AbirHasan2005/Watermark-Bot")]]),
		disable_web_page_preview=True
	)
