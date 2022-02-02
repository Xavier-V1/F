import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import LOG_SESSION, OWNER_ID
from Yukki import BOT_ID, BOT_USERNAME, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Yukki.Database import (add_gban_user, add_off, add_on, add_sudo,
                            get_active_chats, get_served_chats, get_sudoers,
                            is_gbanned_user, remove_active_chat,
                            remove_gban_user, remove_served_chat, remove_sudo,
                            set_video_limit)

__MODULE__ = "المطورين"
__HELP__ = """


🥥︙ /sudolist 
- لعرض قائمة مطورين البوت 


**ملحوظه :**
🥥︙تلك الاوامر للمطورين فقط


🥥︙ /addsudo [بالمعرف او بالرد]
-  لرفع مطور

🥥︙ /delsudo [بالمعرف او بالرد]
- لتنزيل مطور

🥥︙ /maintenance [enable / disable]
- تفعيل وتعطيل الصيانه في البوت!

🥥︙ /logger [enable / disable]
- عند التمكين ، يقوم البوت بتسجيل الاستعلامات التي تم البحث عنها في مجموعة المسجل.

🥥︙ /clean
- تنظيف الملفات والسجلات المؤقتة.
"""
# Add Sudo Users!


@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "🥥︙ الرد على رسالة المستخدم أو إعطاء اسم المستخدم / معرف المستخدم."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                f"🥥︙ {user.mention} مطور بالفعل."
            )
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"🥥︙ تم اضافه **{user.mention}** لقائمة المطورين."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        else:
            await message.reply_text("🥥︙ فشل")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            f"🥥︙ {message.reply_to_message.from_user.mention} بالفعل مطور."
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        await message.reply_text(
            f"🥥︙ تم ؤفع **{message.reply_to_message.from_user.mention}** لقائمة المطورين"
        )
        os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    else:
        await message.reply_text("🥥︙ خطأ")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER_ID))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "🥥︙الرد على رسالة المستخدم أو إعطاء اسم المستخدم / معرف المستخدم."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id not in SUDOERS:
            return await message.reply_text(f"🥥︙ليس مطور.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(
                f"🥥︙ تم المسح **{user.mention}** من {MUSIC_BOT_NAME}'s المطورين."
            )
            return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        await message.reply_text(f"🥥︙ حدث خطأ ما")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in SUDOERS:
        return await message.reply_text(
            f"🥥︙العضو ليس مطور في {MUSIC_BOT_NAME}"
        )
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(
            f"🥥︙ تم المسح **{mention}** من {MUSIC_BOT_NAME}'s مطور."
        )
        return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    await message.reply_text(f"🥥︙حدث خطأ")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "🥥<u> **المالكين**</u>\n"
    sex = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            sex += 1
        except Exception:
            continue
        text += f"{sex}➤ {user}\n"
    smex = 0
    for count, user_id in enumerate(sudoers, 1):
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n🥥<u> **المطورين**</u>\n"
                sex += 1
                text += f"{sex}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("🥥︙ لا يوجد مالكين")
    else:
        await message.reply_text(text)


### Video Limit


@app.on_message(
    filters.command(["set_video_limit", f"set_video_limit@{BOT_USERNAME}"])
    & filters.user(SUDOERS)
)
async def set_video_limit_kid(_, message: Message):
    if len(message.command) != 2:
        usage = "**🥥︙الاستخدام**\n/set_video_limit [عدد من المحادثات المسموح به]"
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    try:
        limit = int(state)
    except:
        return await message.reply_text(
            "🥥︙يرجى استخدام الأرقام الرقمية لتحديد الحد"
        )
    await set_video_limit(141414, limit)
    await message.reply_text(
        f"🥥︙تم تحديد الحد الأقصى لمكالمات الفيديو لـ {limit} دردشه."
    )


## Maintenance Yukki


@app.on_message(filters.command("maintenance") & filters.user(SUDOERS))
async def maintenance(_, message):
    usage = "**🥥︙الاستخدام**\n/maintenance [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("🥥︙ Enabled لتفعيل الصيانه")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("🥥︙ Disabled لتعطيل الصيانه")
    else:
        await message.reply_text(usage)


## Logger


@app.on_message(filters.command("logger") & filters.user(SUDOERS))
async def logger(_, message):
    if LOG_SESSION == "None":
        return await message.reply_text(
            "🥥︙لم اجد دخول.\n\nمن فضلك <code>LOG_SESSION</code> فار وجرب مره اخري."
        )
    usage = "**🥥︙الاستخدام**\n/logger [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 5
        await add_on(user_id)
        await message.reply_text("🥥︙Enabled الدخول")
    elif state == "disable":
        user_id = 5
        await add_off(user_id)
        await message.reply_text("🥥︙ Disabled الدخول")
    else:
        await message.reply_text(usage)


## Gban Module


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**🥥︙الاستخدام**\n/gban [معرف او ايدي الشخص]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "🥥︙هتحظر نفسك يعبيط"
            )
        elif user.id == BOT_ID:
            await message.reply_text("🥥︙ هو انا عبيط هحظر نفسي")
        elif user.id in SUDOERS:
            await message.reply_text("🥥︙ عايز تحظر مطور ؟")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**🥥︙بدء الحظر العام على {user.mention}**\n\n🥥︙الوقت المتوقع {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**🥥︙حظر عام جديد في بوت {MUSIC_BOT_NAME}**__

**🥥︙الاصل** {message.chat.title} [`{message.chat.id}`]
**🥥︙المطور** {from_user.mention}
**🥥︙المحظور** {user.mention}
**🥥︙ايدي المحظور** `{user.id}`
**🥥︙عدد المجموعات** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("🥥︙عايز تحظر نفسك يا عبيط")
    elif user_id == BOT_ID:
        await message.reply_text("🥥︙عايزني ابلك نفسي يعبيط؟")
    elif user_id in sudoers:
        await message.reply_text("🥥︙دا مطور يا غبي ازاي هحظره")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("🥥︙محظور بالفعل")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**🥥︙يتم تنفيذ الحظر العام علي {mention}**\n\n🥥︙الوقت المتوقع {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**🥥︙عضو محظور جديد {MUSIC_BOT_NAME}**__

**🥥︙الاصل** {message.chat.title} [`{message.chat.id}`]
**🥥︙معرف المطور** {from_user_mention}
**🥥︙العضو المحظور** {mention}
**🥥︙ايدي العضو** `{user_id}`
**🥥︙ الدردشات** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**🥥︙الاستخدام**\n🥥︙ /ungban [معرف | ايدي]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("🥥︙عايز تلغي حظر نفسك يا غبي")
        elif user.id == BOT_ID:
            await message.reply_text("🥥︙ هو انا هلغي حظر نفسي ؟")
        elif user.id in sudoers:
            await message.reply_text("🥥︙لا يتم حظر او الغاء حظر المطورين")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("🥥︙تم الغاء الحظر العام بالفعل")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"🥥︙تم الغاء حظر العضو بنجاح")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("🥥︙عايز تلغي حظر نفسك يا غبي")
    elif user_id == BOT_ID:
        await message.reply_text(
            "🥥︙ هو انا هلغي حظر نفسي ؟"
        )
    elif user_id in sudoers:
        await message.reply_text("🥥︙لا يتم حظر او الغاء حظر المطورين")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("🥥︙تم الغاء الحظر العام بالفعل")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"🥥︙تم الغاء حظر العضو بنجاح")


# Broadcast Message


@app.on_message(filters.command("broadcast_pin") & filters.user(SUDOERS))
async def broadcast_message_pin_silent(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**🥥︙تم اذاعة الرسالة في {sent}  مجموعه {pin} وتثبيتها.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**🥥︙الاستخدام**\n🥥︙ /broadcast بالرد علي الرساله"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**🥥︙تم اذاعة الرسالة في {sent}  مجموعه {pin} وتثبيتها.**"
    )


@app.on_message(filters.command("broadcast_pin_loud") & filters.user(SUDOERS))
async def broadcast_message_pin_loud(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**🥥︙تم اذاعة الرسالة في {sent}  مجموعه {pin} وتثبيتها.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**🥥︙الاستخدام**\n🥥︙ /broadcast ثم الرساله او بالرد علي الرساله"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**🥥︙تم اذاعة الرسالة في {sent}  مجموعه {pin} وتثبيتها.**"
    )


@app.on_message(filters.command("broadcast") & filters.user(SUDOERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"**🥥︙تم الاذاعه ل {sent} مجموعه.**")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**🥥︙الاستخدام**\n🥥︙ /broadcast ثم الرساله او بالرد علي الرساله"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"**🥥︙تمت الاذاعة ل  {sent} مجموعه.**")


# Clean


@app.on_message(filters.command("clean") & filters.user(SUDOERS))
async def clean(_, message):
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await message.reply_text("🥥︙تم تنظيف جميع الملفات يا صديقي ")
