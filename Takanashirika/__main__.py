import time
import os
import importlib
import re
import datetime
from typing import Optional, List
import resource
import platform
import sys
import traceback
import requests
import Takanashirika.modules.sql.users_sql as sql
from parsel import Selector
from requests import get
import json
from urllib.request import urlopen
from sys import argv
from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop, Dispatcher
from telegram.utils.helpers import escape_markdown
from Takanashirika import (
    dispatcher,
    updater,
    TOKEN,
    WEBHOOK,
    SUDO_USERS,
    OWNER_ID, 
    CERT_PATH,
    PORT,
    URL,
    LOGGER,
    OWNER_NAME,
    ALLOW_EXCL,
    telethn,
    StartTime,
)
from Takanashirika.modules import ALL_MODULES
from Takanashirika.modules.helper_funcs.chat_status import is_user_admin
from Takanashirika.modules.helper_funcs.misc import paginate_modules
from Takanashirika.modules.connection import connected
from Takanashirika.modules.connection import connect_button

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

PM_START_TEXT = """
Hello *{}*!
────────────────────────
📡 *Takanashi Rika:* `{}`
────────────────────────
Hit the /help to see available command.
"""

buttons = [
    [
        InlineKeyboardButton(text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅ​", callback_data="Sendi_"),
    ],
    [
        InlineKeyboardButton(
            text="ᴄʜᴀɴɴᴇʟ", url="t.me/fckyoupeople1"
        ),
        InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ​", url=f"https://t.me/Rose_Userbot"),
    ],
    [
        InlineKeyboardButton(
            text="➗ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ​ ➗",
            url=f"t.me/{dispatcher.bot.username}?startgroup=new",
        ),
    ],
]

HELP_STRINGS = """
Click the button below for a description of a specific command.
""".format(dispatcher.bot.first_name, "" if not ALLOW_EXCL else "\nAll commands can either be used with / or !.\n")



VERSION = "7.0"

def vercheck() -> str:
    return str(VERSION)



IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []
    
    
for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Takanashirika.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(chat_id=chat_id,
                                text=text,
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=keyboard)


@run_async
def test(bot: Bot, update: Update):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
def start(bot: Bot, update: Update, args: List[str]):
    print("Start")
    uptime = get_readable_time((time.time() - StartTime))
    chat = update.effective_chat  # type: Optional[Chat]
    query = update.callback_query
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Go Back", callback_data="help_back"
                                )
                            ]
                        ]
                    ),
                )

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_text(
                PM_START_TEXT.format(
                    escape_markdown(first_name),
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats(),
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=True,
            )
     
# for test purposes
def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors

@run_async
def help_button(bot: Bot, update: Update):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__,
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🔙", callback_data="help_back")]],
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help"),
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help"),
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help"),
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)

    except BadRequest:
        pass

@run_async
def Takanashi_about_callback(bot: Bot, update: Update):
    query = update.callback_query
    if query.data == "Sendi_":
        query.message.edit_text(
            text="You know how hard it is to manage groups where too many inappropriate messages should be sent?."
            "\n\n• Sometimes we want to send a welcome to a new group member, I have a solution for you."
            "\n\n• Takanashirika is a bot manager or helps manage your groups, this bot is an anime-themed developer named after an anime that we have often watched before."
            "\n\n• Use this bot well, don't ever abuse this bot, if there are problems, please report this bot developer so that the bot will be fixed soon."
            "\n\n• Use the /help command to get all the required commands for your groups..",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ꜱᴘᴇꜱɪᴀʟɪꜱ​", callback_data="Sendi_admin"
                        ),
                        InlineKeyboardButton(
                            text="ʜᴇʟᴘᴍᴇ​", callback_data="help_back"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="sᴜᴘᴘᴏʀᴛ​", callback_data="Sendi_notes"
                        ),
                        InlineKeyboardButton(
                            text="ɢɪᴛʜᴜʙ​", callback_data="Sendi_github"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴄʟᴏꜱᴇ", callback_data="Sendi_back"
                        ),
                    ],
                ]
            ),
        )

    elif query.data == "Sendi_admin":
        query.message.edit_text(
            text=f"*All members can use it.*"
            "\n✘ /tr (language code) as reply to a long message."
            "\n✘ /tm :Dapatkan Tautan Telegraf Media Balasan."
            "\n✘ /txt :Dapatkan Tautan Telegraf dari Teks Balasan.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ​", callback_data="Sendi_")]]
            ),
        )

    elif query.data == "Sendi_notes":
        query.message.edit_text(
            text=f"<b>Terimakasih Atas Semua Kerjasamanya❤️</b>"
            f"\n\n👼 [Sendi](t.me/pikyus1) [Developer]"
            f"\n🥳 [CurhatBarengBottyBot](t.me/CurhatBarengBottyBot) [Support]"
            f"\n🥰 [Rose-Userbot](https://t.me/Rose_Userbot) [Support]"
            f"\n🦾 [Kopi](https://t.me/KetikaOtakPerluInspirasi) [Support]"
            f"\n🫂 [Kopicu](t.me/Kopicubot) [Support]"
            f"\n🔥 [BottyCu](https://t.me/BottyCu) [Support]"
            f"\n☠️ [KopiChannel](https://t.me/kopi_channel) [Support]"
            f"\n🤖 [MenuBottyCuBot](https://t.me/MenuBottyCuBot) [Support]"
            f"\n🔐 [SM•Project](https://t.me/fckyoupeople1) [Support]",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ​", callback_data="Sendi_")]]
            ),
        )

    elif query.data == "Sendi_github":
        query.message.edit_text(
            text=f"*Support Me As Your Friend💋*",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ɢɪᴛʜᴜʙ", url="https://github.com/SendiAp"),
                    ],
                    [
                        InlineKeyboardButton(text="ɢᴏ ʙᴀᴄᴋ​", callback_data="Sendi_"),
                    ],
                ]
            ),
        )

@run_async
def get_help(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:

        update.effective_message.reply_text("Contact me in PM to get the list of possible commands.",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="[► ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ◄]",url="t.me/{}?start=help".format(bot.username))],  
                                                [InlineKeyboardButton(text="[► ᴏᴡɴᴇʀ ◄]",url="https://t.me/pikyus1")]]))
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = "Here is the available help for the *{}* module:\n".format(HELPABLE[module].__mod_name__) \
               + HELPABLE[module].__help__
        send_help(chat.id, text, InlineKeyboardMarkup([[InlineKeyboardButton(text="🚶‍♂️Back🚶‍♂️", callback_data="help_back")]]))

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id)) for mod in USER_SETTINGS.values())
            dispatcher.bot.send_message(user_id, "These are your current settings:" + "\n\n" + settings,
                                        parse_mode=ParseMode.MARKDOWN)

        else:
            dispatcher.bot.send_message(user_id, "Seems like there aren't any user specific settings available :'(",
                                        parse_mode=ParseMode.MARKDOWN)

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(user_id,
                                        text="Which module would you like to check {}'s settings for?".format(
                                            chat_name),
                                        reply_markup=InlineKeyboardMarkup(
                                            paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)))
        else:
            dispatcher.bot.send_message(user_id, "Seems like there aren't any chat settings available :'(\nSend this "
                                                 "in a group chat you're admin in to find its current settings!",
                                        parse_mode=ParseMode.MARKDOWN)


@run_async
def settings_button(bot: Bot, update: Update):
    query = update.callback_query
    user = update.effective_user
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(escape_markdown(chat.title),
                                                                                     CHAT_SETTINGS[
                                                                                         module].__mod_name__) + \
                   CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(text=text,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton(text="🔙",
                                                                callback_data="stngs_back({})".format(chat_id))]]))

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text("Hi there! There are quite a few settings for {} - go ahead and pick what "
                                     "you're interested in.".format(chat.title),
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(curr_page - 1, CHAT_SETTINGS, "stngs",
                                                          chat=chat_id)))

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text("Hi there! There are quite a few settings for {} - go ahead and pick what "
                                     "you're interested in.".format(chat.title),
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(next_page + 1, CHAT_SETTINGS, "stngs",
                                                          chat=chat_id)))

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                                          "you're interested in.".format(escape_markdown(chat.title)),
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(paginate_modules(0, CHAT_SETTINGS, "stngs",
                                                                                        chat=chat_id)))

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))

@run_async
def get_settings(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
    args = msg.text.split(None, 1)

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(text,
                           reply_markup=InlineKeyboardMarkup(
                               [[InlineKeyboardButton(text="⚙️ꜱᴇᴛᴛɪɴɢꜱ⚙️",
                                                      url="t.me/{}?start=stngs_{}".format(
                                                          bot.username, chat.id))]]))
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


def migrate_chats(bot: Bot, update: Update):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop

            
# Avoid memory dead
def memory_limit(percentage: float):
    if platform.system() != "Linux":
        print('Only works on linux!')
        return
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (int(get_memory() * 1024 * percentage), hard))

def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory

def memory(percentage=0.5):
    def decorator(function):
        def wrapper(*args, **kwargs):
            memory_limit(percentage)
            try:
                function(*args, **kwargs)
            except MemoryError:
                mem = get_memory() / 1024 /1024
                print('Remain: %.2f GB' % mem)
                sys.stderr.write('\n\nERROR: Memory Exception\n')
                sys.exit(1)
        return wrapper
    return decorator


@memory(percentage=0.8)
def main():
    test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start, pass_args=True)
    
    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")
   
    about_callback_handler = CallbackQueryHandler(Takanashi_about_callback, pattern=r"Sendi_")
    

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)


    # dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="127.0.0.1",
                              port=PORT,
                              url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN,
                                    certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("TakanashiRika running...")
        updater.start_polling(timeout=15, read_latency=4)
        
    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()
      
      
    updater.idle()

    
if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    main()
