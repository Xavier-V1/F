import asyncio
import random
import time
from sys import version as pyver
from typing import Dict, List, Union

import psutil
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from Yukki import ASSIDS, BOT_ID, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Yukki import boottime as bot_start_time
from Yukki import db, random_assistant
from Yukki.Core.PyTgCalls import Yukki
from Yukki.Database import (add_nonadmin_chat, add_served_chat,
                            blacklisted_chats, get_assistant, get_authuser,
                            get_authuser_names, get_start, is_nonadmin_chat,
                            is_served_chat, remove_active_chat,
                            remove_nonadmin_chat, save_assistant, save_start)
from Yukki.Decorators.admins import ActualAdminCB
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (custommarkup, dashmarkup, setting_markup,
                          setting_markup2, start_pannel, usermarkup, volmarkup)
from Yukki.Utilities.assistant import get_assistant_details
from Yukki.Utilities.ping import get_readable_time

welcome_group = 2

__MODULE__ = "الاساسي"
__HELP__ = """


🥥︙ /start 
- لبدء البوت


🥥︙ /help 
- لجلب قائمه الاوامر


/settings 
- 🥥︙لجلب قائمه الاعدادات
"""


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id == BOT_ID:
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        f"🥥︙هشششششششششش رومك[{message.chat.title}] اتحظرت\n\n🥥︙شوف اي مطور يفك حظرها"
                    )
                    return await app.leave_chat(chat_id)
                _assistant = await get_assistant(message.chat.id, "assistant")
                if not _assistant:
                    ran_ass = random.choice(random_assistant)
                    assis = {
                        "saveassistant": ran_ass,
                    }
                    await save_assistant(message.chat.id, "assistant", assis)
                else:
                    ran_ass = _assistant["saveassistant"]
                (
                    ASS_ID,
                    ASS_NAME,
                    ASS_USERNAME,
                    ASS_ACC,
                ) = await get_assistant_details(ran_ass)
                out = start_pannel()
                await message.reply_text(
                    f"🥥︙مرحبا بك في {MUSIC_BOT_NAME}\n\n🥥︙قم برفعي ادمن في مجموعتك\n\n🥥︙ معرف الحساب المساعد:- @{ASS_USERNAME}\n🥥︙ايدي الحساب المساعد:- {ASS_ID}",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                )
            if member.id in ASSIDS:
                return await remove_active_chat(chat_id)
            if member.id in OWNER_ID:
                return await message.reply_text(
                    f"🥥︙ انضم مالك البوت{MUSIC_BOT_NAME} لمحادثتك [{member.mention}] "
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"🥥︙انضم مطور {MUSIC_BOT_NAME} لمحاثتك [{member.mention}] "
                )
            return
        except:
            return


@app.on_message(filters.command(["help", "start"]) & filters.group)
@PermissionCheck
async def useradd(_, message: Message):
    out = start_pannel()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"🥥︙شكرا لاضافتي بمجموعتك {message.chat.title}.\n🥥︙البوت {MUSIC_BOT_NAME} في حاله الاتصال\n\n🥥︙ستجد البوتات المساعده, وحل اي مشكله تواجهك في قناه السورس",
            reply_markup=InlineKeyboardMarkup(out[1]),
        ),
    )


@app.on_message(filters.command("settings") & filters.group)
@PermissionCheck
async def settings(_, message: Message):
    c_id = message.chat.id
    _check = await get_start(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_start(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    text, buttons = setting_markup2()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"{text}\n\n**🥥︙اسم المجموعه** {message.chat.title}\n**🥥︙ايدي المجموعه** {message.chat.id}\n**🥥︙مستوي الصوت** {volume}%",
            reply_markup=InlineKeyboardMarkup(buttons),
        ),
    )


@app.on_callback_query(filters.regex("okaybhai"))
async def okaybhai(_, CallbackQuery):
    await CallbackQuery.answer("🥥︙يتم الرجوع")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"🥥︙شكرا لاضافتي بمجموعتك {message.chat.title}.\n🥥︙ {MUSIC_BOT_NAME} في حاله الاتصال\n\n🥥︙ستجد البوتات المساعده, وحل اي مشكله تواجهك في قناه السورس",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("🥥︙اعدادات البوت")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_start(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_start(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**مستوي الصوت** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("EVE"))
@ActualAdminCB
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("Changes Saved")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n🥥︙اوامر المجموعه تغيرت \n\ يمكن لاي شخص في المجموعه توقيف او تخطي او استكمال الموسيقي\n\n🥥︙تم التحديث بواسطه @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "🥥︙بالتاكيد الاوامر لجميع الاعضاء", show_alert=True
        )


@app.on_callback_query(filters.regex("AMS"))
@ActualAdminCB
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "🥥︙بالتأكيد الاوامر للادمنيه فقط", show_alert=True
        )
    else:
        await CallbackQuery.answer("Changes Saved")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n🥥︙اوامر المجموعه تغيرت \n\n🥥︙لا يمكن لاي شخص سوي الادميه في المجموعه توقيف او تخطي او استكمال الموسيقي\n\n🥥︙تم التحديث بواسطه @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("🥥︙بالتأكيد قي اعلي جوده", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("🥥︙اعدادات البوت")
        text, buttons = volmarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("🥥︙اعدادات البوت")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "Admins Only"
        else:
            current = "Everyone"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n\n🥥︙من يمكنه استخدام البوت {MUSIC_BOT_NAME}:- **{current}**\n\n**🥥︙ما هذا?**\n\n🥥︙ الجميع- يمكن الجميع استخدام البوت{MUSIC_BOT_NAME}الاوامر(skip, pause, resume)",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("🥥︙انتظر")
        text, buttons = dashmarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n\n🥥︙فحص {MUSIC_BOT_NAME} يتم تحديث البوت دائما افحص قناه السورس",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("🥥︙اعدادات البوت")
        text, buttons = custommarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت .")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("🥥︙يتم تغيير اعدادات الصوت ")
        except:
            return await CallbackQuery.answer("🥥︙لا يوجد محادثه صوتيه")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**🥥︙المجموعه** {c_title}\n**🥥︙ايدي المجموعه** {c_id}\n**🥥︙مستوي الصوت** {volume}%\n🥥︙جوده الصوت الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("Auth Users!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\n🥥︙ لم يتم العثور على مستخدمين معتمدين\n\n🥥︙ يمكنك السماح لأي شخص غير مسؤول باستخدام أوامر المسؤول الخاصة بي عن طريق /auth وحذف باستخدام /unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "🥥︙ إحضار المستخدمين المصرح لهم ... الرجاء الانتظار"
            )
            msg = f"**🥥︙قائمة المستخدمين المعتمدين**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
                user_id = _note["auth_user_id"]
                user_name = _note["auth_name"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    🥥︙اضيف بواسطه- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"🥥︙وقت بدء البوت {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"🥥︙مساحه استخدام المعالج {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"🥥︙الذاكره المستخدمه {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"🥥︙المساحه المستخدمه {diske}%", show_alert=True
        )
