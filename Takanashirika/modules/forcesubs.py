import logging
import time

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from telegram.ext import CommandHandler, MessageHandler, Filters, run_async
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from Takanashirika import SUDO_USERS
from Takanashirika import pbot
from Takanashirika.modules.sql import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@run_async
def _onUnMuteRequest(bot: Bot, update: Update):
    user_id = update.from_user.id
    chat_id = update.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = update.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (update.get_me()).id:
                try:
                    bot.get_chat_member(channel, user_id)
                    bot.unban_chat_member(chat_id, user_id)
                    bot.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    update.answer_callback_query(
                        bot.id,
                        text=f"❗ Join our @{channel} channel and press 'Unmute Me' button.",
                        show_alert=True,
                    )
            else:
                update.answer_callback_query(
                    bot.id,
                    text="❗ You have been muted by admins due to some other reason.",
                    show_alert=True,
                )
        else:
            if (
                not client.get_chat_member(chat_id, (client.get_me()).id).status
                == "administrator"
            ):
                update.send_message(
                    chat_id,
                    f"❗ **{cb.from_user.mention} is trying to UnMute himself but i can't unmute him because i am not an admin in this chat add me as admin again.**\n__#Leaving this chat...__",
                )

            else:
                update.answer_callback_query(
                    bot.id,
                    text="❗ Warning! Don't press the button when you cn talk.",
                    show_alert=True,
                )


@run_async
def _check_member(bot: Bot, update: Update):
    chat_id = update.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = update.from_user.id
        if (
            not bot.get_chat_member(chat_id, user_id).status
            in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                bot.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "Welcome {} 🙏 \n **You haven't joined our @{} Channel yet**👷 \n \nPlease Join [Our Channel](https://t.me/{}) and hit the **UNMUTE ME** Button. \n \n ".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Join Channel",
                                        url="https://t.me/{}".format(channel),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "Unmute Me", callback_data="onUnMuteRequest"
                                    )
                                ],
                            ]
                        ),
                    )
                    bot.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        "😕 **Skyzuo is not admin here..**\n__Give me ban permissions and retry.. \n#Ending FSub...__"
                    )

            except ChatAdminRequired:
                bot.send_message(
                    chat_id,
                    text=f"😕 **I not an admin of @{channel} channel.**\n__Give me admin of that channel and retry.\n#Ending FSub...__",
                )


@run_async
def foce_sub(bot: Bot, update: Update):
    user = update.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator" or user.user.id in SUDO_USERS:
        chat_id = update.chat.id
        if len(message.command) > 1:
            input_str = update.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                update.reply_text("❌ **Force Subscribe is Disabled Successfully.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**Unmuting all members who are muted by me...**"
                )
                try:
                    for chat_member in bot.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            bot.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("✅ **Unmuted all members who are muted by me.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "😕 **I am not an admin in this chat.**\n__I can't unmute members because i am not an admin in this chat make me admin with ban user permission.__"
                    )
            else:
                try:
                    bot.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    bot.reply_text(
                        f"✅ **Force Subscribe is Enabled**\n__Force Subscribe is enabled, all the group members have to subscribe this [channel](https://t.me/{input_str}) in order to send messages in this group.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    bot.reply_text(
                        f"😕 **Not an Admin in the Channel**\n__I am not an admin in the [channel](https://t.me/{input_str}). Add me as a admin in order to enable ForceSubscribe.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    bot.reply_text(f"❗ **Invalid Channel Username.**")
                except Exception as err:
                    bot.reply_text(f"❗ **ERROR:** ```{err}```")
        else:
            if sql.fs_settings(chat_id):
                bot.reply_text(
                    f"✅ **Force Subscribe is enabled in this chat.**\n__For this [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                bot.reply_text("❌ **Force Subscribe is disabled in this chat.**")
    else:
        bot.reply_text(
            "❗ **Group Creator Required**\n__You have to be the group creator to do that.__"
        )


FORCE_HANDLER = CommandHandler("force",foce_sub)

dispatcher.add_handler(FORCE_HANDLER)
