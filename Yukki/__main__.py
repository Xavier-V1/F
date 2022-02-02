import asyncio
import importlib
import os
import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytgcalls import idle
from rich.console import Console
from rich.table import Table
from youtubesearchpython import VideosSearch

from config import (LOG_GROUP_ID, LOG_SESSION, STRING1, STRING2, STRING3,
                    STRING4, STRING5)
from Yukki import (ASS_CLI_1, ASS_CLI_2, ASS_CLI_3, ASS_CLI_4, ASS_CLI_5,
                   ASSID1, ASSID2, ASSID3, ASSID4, ASSID5, ASSNAME1, ASSNAME2,
                   ASSNAME3, ASSNAME4, ASSNAME5, BOT_ID, BOT_NAME, LOG_CLIENT,
                   OWNER_ID, app)
from Yukki.Core.Clients.cli import LOG_CLIENT
from Yukki.Core.PyTgCalls.Yukki import (pytgcalls1, pytgcalls2, pytgcalls3,
                                        pytgcalls4, pytgcalls5)
from Yukki.Database import (get_active_chats, get_active_video_chats,
                            get_sudoers, is_on_off, remove_active_chat,
                            remove_active_video_chat)
from Yukki.Inline import private_panel
from Yukki.Plugins import ALL_MODULES
from Yukki.Utilities.inline import paginate_modules

loop = asyncio.get_event_loop()
console = Console()
HELPABLE = {}


async def initiate_bot():
    with console.status(
        "[magenta] تم بدء تنصيب سورس زينه ميوزك...",
    ) as status:
        try:
            chats = await get_active_video_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_video_chat(chat_id)
        except Exception as e:
            pass
        try:
            chats = await get_active_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_chat(chat_id)
        except Exception as e:
            pass
        status.update(
            status="[bold blue]يتم فحص المميوات", spinner="earth"
        )
        console.print("Found {} Plugins".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]يتم تحميل المميزات...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "Yukki.Plugins." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f">> [bold cyan]تم تحميل ملف : [green]{all_module}.py"
            )
        console.print("")
        status.update(
            status="[bold blue]تم اكتمال التحميل!",
        )
    console.print(
        "[bold green]مبروك تم تنصيب البوت بنجاح!\n"
    )
    try:
        await app.send_message(
            LOG_GROUP_ID,
            "<b>Congrats!! تم بدء بوت اغاني علي سورس زينه بنجاح!</b>",
        )
    except Exception as e:
        print(
            "\nفشل البوت في القناه تأكد من رفعك للبوت ادمن بالقناة!"
        )
        console.print(f"\n[red]تم ايقاف البوت")
        return
    a = await app.get_chat_member(LOG_GROUP_ID, BOT_ID)
    if a.status != "administrator":
        print("قم برفع البوت ادمن بقناة الدخول")
        console.print(f"\n[red]تم ايقاف البوت")
        return
    console.print(f"\n┌[red] Bot Started as {BOT_NAME}!")
    console.print(f"├[green] الايدي :- {BOT_ID}!")
    if STRING1 != "None":
        try:
            await ASS_CLI_1.send_message(
                LOG_GROUP_ID,
                "<b>تم حفظ الحساب المساعد الاول!</b>",
            )
        except Exception as e:
            print(
                "\nحدث خطأ تأكد من رفعك للبوت المساعد ادمن بقناه الدخول!"
            )
            console.print(f"\n[red]تم ايقاف البوت")
            return
        try:
            await ASS_CLI_1.join_chat("ZeiNaaMuSic")
            await ASS_CLI_1.join_chat("ZeiNaMu")
        except:
            pass
        console.print(f"├[red] بدأالحساب المساعد الاول {ASSNAME1}!")
        console.print(f"├[green] ايدي :- {ASSID1}!")
    if STRING2 != "None":
        try:
            await ASS_CLI_2.send_message(
                LOG_GROUP_ID,
                "<b>تم حفظ الحساب المساعد الثاني!</b>",
            )
        except Exception as e:
            print(
                "\nحدث خطأ تأكد من رفعك للبوت المساعد ادمن بقناه الدخول!"
            )
            console.print(f"\n[red]تم ايقاف البوت")
            return
        try:
            await ASS_CLI_2.join_chat("ZeiNaaMuSic")
            await ASS_CLI_2.join_chat("ZeiNaMu")
        except:
            pass
        console.print(f"├[red] تم بدء الحساب المساعد الثاني {ASSNAME2}!")
        console.print(f"├[green] الايدي :- {ASSID2}!")
    if STRING3 != "None":
        try:
            await ASS_CLI_3.send_message(
                LOG_GROUP_ID,
                "<b>تم حفظ الحساب المساعد الثالث!</b>",
            )
        except Exception as e:
            print(
                "\nحدث خطأ تأكد من رفعك للبوت المساعد ادمن بقناه الدخول!"
            )
            console.print(f"\n[red]تم ايقاف البوت")
            return
        try:
            await ASS_CLI_3.join_chat("ZeiNaaMuSic")
            await ASS_CLI_3.join_chat("ZeiNaMu")
        except:
            pass
        console.print(f"├[red] تم بدأالحساب المساعد {ASSNAME3}!")
        console.print(f"├[green] الايدي :- {ASSID3}!")
    if STRING4 != "None":
        try:
            await ASS_CLI_4.send_message(
                LOG_GROUP_ID,
                "<b>تم بدء الحساب المساعد الرابع بنجاح!</b>",
            )
        except Exception as e:
            print(
                "\nحدث خطأ تأكد من رفعك للبوت المساعد ادمن بقناه الدخول "
            )
            console.print(f"\n[red]تم ايقاف البوت")
            return
        try:
            await ASS_CLI_4.join_chat("ZeiNaaMuSic")
            await ASS_CLI_4.join_chat("ZeiNaMu")
        except:
            pass
        console.print(f"├[red] تم بدء الحساب المساعد {ASSNAME4}!")
        console.print(f"├[green] الايدي :- {ASSID4}!")
    if STRING5 != "None":
        try:
            await ASS_CLI_5.send_message(
                LOG_GROUP_ID,
                "<b>تم بدء الحساب المساعد الخامس !</b>",
            )
        except Exception as e:
            print(
                "\nحدث خطأ تأكد من رفعك للبوت المساعد ادمن بقناه الدخول"
            )
            console.print(f"\n[red]تم ايقاف البوت")
            return
        try:
            await ASS_CLI_5.join_chat("ZeiNaaMuSic")
            await ASS_CLI_5.join_chat("ZeiNaMu")
        except:
            pass
        console.print(f"├[red] تم بدء الحساب لمساعد {ASSNAME5}!")
        console.print(f"├[green] الايدي :- {ASSID5}!")
    if LOG_SESSION != "None":
        try:
            await LOG_CLIENT.send_message(
                LOG_GROUP_ID,
                "<b>Congrats!! Logger Client has started successfully!</b>",
            )
        except Exception as e:
            print(
                "\nفشل Logger Client في الوصول إلى قناة السجل. تأكد من أنك قد أضفت حساب المسجل الخاص بك إلى قناة السجل الخاصة بك وقمت بالترقية كمسؤول!"
            )
            console.print(f"\n[red]تم ايقاف البوت")
            return
        try:
            await LOG_CLIENT.join_chat("ZeiNaaMuSic")
            await LOG_CLIENT.join_chat("ZeiNaMu")
        except:
            pass
    console.print(f"└[red] تم تنصيب بوت الاغاني بنجاح.")
    if STRING1 != "None":
        await pytgcalls1.start()
    if STRING2 != "None":
        await pytgcalls2.start()
    if STRING3 != "None":
        await pytgcalls3.start()
    if STRING4 != "None":
        await pytgcalls4.start()
    if STRING5 != "None":
        await pytgcalls5.start()
    await idle()
    console.print(f"\n[red]يتم ايقاف البوت")


home_text_pm = f"""مرحبا ,
اسمي  {BOT_NAME}.
انا بوت يقوم بتشغيل الاغاني / الفيديو في المحادثة الصوتيه بمجموعتك.

جميع الاوامر تبدء ب : / """


@app.on_message(filters.command("help") & filters.private)
async def help_command(_, message):
    text, keyboard = await help_parser(message.from_user.mention)
    await app.send_message(message.chat.id, text, reply_markup=keyboard)


@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name[0] == "s":
            sudoers = await get_sudoers()
            text = "⚡️︙<u> **المالكين:**</u>\n"
            sex = 0
            for x in OWNER_ID:
                try:
                    user = await app.get_users(x)
                    user = (
                        user.first_name if not user.mention else user.mention
                    )
                    sex += 1
                except Exception:
                    continue
                text += f"{sex}➤ {user}\n"
            smex = 0
            for count, user_id in enumerate(sudoers, 1):
                if user_id not in OWNER_ID:
                    try:
                        user = await app.get_users(user_id)
                        user = (
                            user.first_name
                            if not user.mention
                            else user.mention
                        )
                        if smex == 0:
                            smex += 1
                            text += "\n⚡️︙<u> **للمطورين**</u>\n"
                        sex += 1
                        text += f"{sex}➤ {user}\n"
                    except Exception:
                        continue
            if not text:
                await message.reply_text("⚡️︙ لا يوجد مطورين")
            else:
                await message.reply_text(text)
            if await is_on_off(5):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                umention = f"[{sender_name}](tg://user?id={int(sender_id)})"
                return await LOG_CLIENT.send_message(
                    LOG_GROUP_ID,
                    f"{message.from_user.mention} بدء البوت في فحص <code>SUDOLIST</code>\n\n**ايدي العضو:** {sender_id}\n**معرف العضو:** {sender_name}",
                )
        if name == "help":
            text, keyboard = await help_parser(message.from_user.mention)
            await message.delete()
            return await app.send_text(
                message.chat.id,
                text,
                reply_markup=keyboard,
            )
        if name[0] == "i":
            m = await message.reply_text("🍒︙ يتم إحضار المعلومات برجاء الانتظار")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
⚡️ **تم تحميل الفيديو بنجاح**

⚡️ **العنوان:** {title}

⚡️ **المده :** {duration} Mins
⚡️ **المشاهدات:** `{views}`
⚡️ **وقت النشر:** {published}
⚡️ **اسم القناة:** {channel}
⚡️ **رابط القناة:** [link]({channellink})
⚡️ **رابط الفيديو :** [Link]({link})

⚡️ تم التحميل بواسطة  {BOT_NAME}"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 شاهد الفيديو علي اليوتيوب", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="✗ اغلاق", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
            if await is_on_off(5):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                umention = f"[{sender_name}](tg://user?id={int(sender_id)})"
                return await LOG_CLIENT.send_message(
                    LOG_GROUP_ID,
                    f"{message.from_user.mention} يقوم البوت بفحص <code>VIDEO INFORMATION</code>\n\n**الايدي:** {sender_id}\n**المعرف:** {sender_name}",
                )
            return
    out = private_panel()
    await message.reply_text(
        home_text_pm,
        reply_markup=InlineKeyboardMarkup(out[1]),
    )
    if await is_on_off(5):
        sender_id = message.from_user.id
        sender_name = message.from_user.first_name
        umention = f"[{sender_name}](tg://user?id={int(sender_id)})"
        return await LOG_CLIENT.send_message(
            LOG_GROUP_ID,
            f"{message.from_user.mention} قام ب بدء البوت.\n\n**الايدي :** {sender_id}\n**المعرف :** {sender_name}",
        )
    return


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """مرحبا {first_name},

اضغط علي الازرار للمزيد من المعلومات.

كل الاوامر تبدء ب: /
""".format(
            first_name=name
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("shikhar"))
async def shikhar(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""مرحبا {query.from_user.first_name},

اضغط علي الازرار للمزيد من الاوامر.

جميع الاوامر تبدء ب : /
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "ها هي المساعدة ل ", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ رجوع", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="✗ اغلاق", callback_data="close"
                    ),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )
    elif home_match:
        out = private_panel()
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out[1]),
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
