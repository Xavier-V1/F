import asyncio
import math
import os
import dotenv
import random
import shutil
from datetime import datetime
from time import strftime, time

import heroku3
import requests
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import Client, filters
from pyrogram.types import Message

from config import (HEROKU_API_KEY, HEROKU_APP_NAME, UPSTREAM_BRANCH,
                    UPSTREAM_REPO)
from Yukki import LOG_GROUP_ID, MUSIC_BOT_NAME, SUDOERS, app
from Yukki.Database import get_active_chats, remove_active_chat, remove_active_video_chat
from Yukki.Utilities.heroku import is_heroku, user_input
from Yukki.Utilities.paste import isPreviewUp, paste_queue

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__MODULE__ = "السيرفر"
__HELP__ = f"""

**ملحوظه**
**للمطورين فقط**

🥥︙ /get_log
- احصل على سجل لآخر 100 سطر من هيروكا.

🥥︙ /get_var
- احصل على فار من هيروكا

🥥︙ /del_var
- حذف فار من هيروكا

🥥︙ /set_var [اسم الفار] [القيمه]
- قم بتعيين فار أو تحديث فار على هيروكا . منفصلة فار وقيمتها بمسافة.

🥥︙ /usage
- لمعرفه سعه استخدامك

🥥︙ /update
- لتحديث بوتك

🥥︙ /restart 
- لتحديث البوت
"""


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


@app.on_message(filters.command("get_log") & filters.user(SUDOERS))
async def log_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "🥥︙<b>تم اكتشاف تطبيق HEROKU!</b>\n\n🥥︙لتحديث تطبيقك ، تحتاج إلى إعداد ملف `HEROKU_API_KEY` و `HEROKU_APP_NAME` الفارات بالتوالي!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "🥥︙<b>تم اكتشاف تطبيق HEROKU!</b>\n\n🥥︙<b>تأكد من وضعك</b> `HEROKU_API_KEY` **و** `HEROKU_APP_NAME` <b>الفار بشكل صحيح حتى تتمكن من التحديث عن بُعد!</b>"
            )
    else:
        return await message.reply_text("🥥︙فقط من أجل تطبيقات Heroku")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            "🥥︙ يرجى التأكد من أن مفتاح Heroku API الخاص بك ، واسم التطبيق الخاص بك مهيأ بشكل صحيح في heroku"
        )
    data = happ.get_log()
    if len(data) > 1024:
        link = await paste_queue(data)
        url = link + "/index.txt"
        return await message.reply_text(
            f"🥥︙هنا هو سجل التطبيق الخاص بك[{HEROKU_APP_NAME}]\n\n[انقر هنا للتحقق من السجلات]({url})"
        )
    else:
        return await message.reply_text(data)


@app.on_message(filters.command("get_var") & filters.user(SUDOERS))
async def varget_(client, message):
    usage = "**🥥︙الاستخدام**\n/get_var [اسم الفار]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n🥥︙لتحديث تطبيقك ، تحتاج إلى إعداد ملف `HEROKU_API_KEY` و `HEROKU_APP_NAME` الفارات بالتوالي!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n<b>تأكد من وضعك</b> `HEROKU_API_KEY` **و** `HEROKU_APP_NAME` <b>الفار بشكل صحيح حتى تتمكن من التحديث عن بُعد!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                "🥥︙يرجى التأكد من أن مفتاح Heroku API الخاص بك ، واسم التطبيق الخاص بك مهيأ بشكل صحيح في heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            return await message.reply_text(
                f"**🥥︙كونفينج هيروكا**\n\n**{check_var}:** `{heroku_config[check_var]}`"
            )
        else:
            return await message.reply_text("🥥︙ لا يوجد فار")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text("🥥︙ .env لم يتم ايجاده.")
        output = dotenv.get_key(path, check_var)
        if not output:
            return await message.reply_text("🥥︙ لا يوجد فار")
        else:
            return await message.reply_text(f".env:\n\n**{check_var}:** `{str(output)}`")


@app.on_message(filters.command("del_var") & filters.user(SUDOERS))
async def vardel_(client, message):
    usage = "**🥥︙الاستخدام**\n/del_var [اسم الفار]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n🥥︙لتحديث تطبيقك ، تحتاج إلى إعداد ملف `HEROKU_API_KEY` و `HEROKU_APP_NAME` الفارات بالتوالي"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n<b>تأكد من وضعك</b> `HEROKU_API_KEY` **و** `HEROKU_APP_NAME` <b>الفار بشكل صحيح حتى تتمكن من التحديث عن بُعد!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                "🥥︙يرجى التأكد من أن مفتاح Heroku API الخاص بك ، واسم التطبيق الخاص بك مهيأ بشكل صحيح في heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            await message.reply_text(
                f"**🥥︙فار هيروكا**\n\n🥥︙ اسم الفار `{check_var}` تم مسحه بنجاح"
            )
            del heroku_config[check_var]
        else:
            return await message.reply_text(f"🥥︙ لا يوجد فار")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text("🥥︙ .env لم يتم ايجاده..")
        output = dotenv.unset_key(path, check_var)
        if not output[0]:
            return await message.reply_text("🥥︙ لا يوجد فار")
        else:
            return await message.reply_text(f"🥥︙.env حذف المتغيرات\n\n`{check_var}`تم حذفه بنجاح. لإعادة تشغيل الروبوت اضغط /restart .")


@app.on_message(filters.command("set_var") & filters.user(SUDOERS))
async def set_var(client, message):
    usage = "**🥥︙الاستخدام**\n/set_var [اسم الفار] [قيمه الفار]"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n🥥︙لتحديث تطبيقك ، تحتاج إلى إعداد ملف `HEROKU_API_KEY` و `HEROKU_APP_NAME` الفارات بالتوالي"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n<b>تأكد من وضعك</b> `HEROKU_API_KEY` **و** `HEROKU_APP_NAME` <b>الفار بشكل صحيح حتى تتمكن من التحديث عن بُعد!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                "🥥︙يرجى التأكد من أن مفتاح Heroku API الخاص بك ، واسم التطبيق الخاص بك مهيأ بشكل صحيح في heroku"
            )
        heroku_config = happ.config()
        if to_set in heroku_config:
            await message.reply_text(
                f"**🥥︙فار هيروكا**\n\n`{to_set}` تم تحديثها بنجاح برجاء التحديث /restart."
            )
        else:
            await message.reply_text(
                f"🥥︙تمت إضافة فار جديد بالاسم `{to_set}`. سيعاد تشغيل البوت الآن."
            )
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text("🥥︙ .env لم يتم ايجاده..")
        output = dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            return await message.reply_text(f"**🥥︙ .env تحديث الفار:**\n\n`{to_set}` تم تحديثها بنجاح برجاء التحديث /restart.")
        else:
            return await message.reply_text(f"**🥥︙ .env إضافة المتغيرات**\n\n`{to_set}` تم تحديثها بنجاح برجاء التحديث /restart.")


@app.on_message(filters.command("usage") & filters.user(SUDOERS))
async def usage_dynos(client, message):
    ### Credits CatUserbot
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n🥥︙لتحديث تطبيقك ، تحتاج إلى إعداد ملف `HEROKU_API_KEY` و `HEROKU_APP_NAME` الفارات بالتوالي"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n<b>تأكد من وضعك</b> `HEROKU_API_KEY` **و** `HEROKU_APP_NAME` <b>الفار بشكل صحيح حتى تتمكن من التحديث عن بُعد!</b>"
            )
    else:
        return await message.reply_text("🥥︙فقط للتطبيثات هيروكا")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            "🥥︙يرجى التأكد من أن مفتاح Heroku API الخاص بك ، واسم التطبيق الخاص بك مهيأ بشكل صحيح في heroku"
        )
    dyno = await message.reply_text("🥥︙التحقق من استخدام Heroku. ارجوك انتظر")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
**استخدام DYNO**

<u>🥥︙الاستخدام</u>
🥥︙مجموع المستخدمة `{AppHours}`**h**  `{AppMinutes}`**m**  [`{AppPercentage}`**%**]

🥥︙مجموع المتبقي `{hours}`**h**  `{minutes}`**m**  [`{percentage}`**%**]"""
    return await dyno.edit(text)


@app.on_message(filters.command("update") & filters.user(SUDOERS))
async def update_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n🥥︙لتحديث تطبيقك ، تحتاج إلى إعداد ملف `HEROKU_API_KEY` و `HEROKU_APP_NAME` الفارات بالتوالي"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n<b>تأكد من وضعك</b> `HEROKU_API_KEY` **و** `HEROKU_APP_NAME` <b>الفار بشكل صحيح حتى تتمكن من التحديث عن بُعد!</b>"
            )
    response = await message.reply_text("🥥︙التحقق من وجود تحديثات متوفرة ...")
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit("🥥︙خطأ أمر Git")
    except InvalidGitRepositoryError:
        return await response.edit("🥥︙ملف Git Repsitory غير صالح")
    to_exc = f"🥥︙git fetch origin {UPSTREAM_BRANCH} &> /dev/null"
    os.system(to_exc)
    await asyncio.sleep(7)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]  # main git repository
    for checks in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        verification = str(checks.count())
    if verification == "":
        return await response.edit("🥥︙البوت محدث!")
    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[
            (format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4
        ],
    )
    for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        updates += f"<b>➣ #{info.count()}: [{info.summary}]({REPO_}/commit/{info}) by -> {info.author}</b>\n\t\t\t\t<b>➥ Commited on:</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    _update_response_ = "<b>🥥︙يتوفر تحديث جديد للبوت!</b>\n\n🥥︙ رفع التحديثات الآن</code>\n\n**<u>🥥︙ التحديثات</u>**\n\n"
    _final_updates_ = _update_response_ + updates
    if len(_final_updates_) > 4096:
        link = await paste_queue(updates)
        url = link + "/index.txt"
        nrs = await response.edit(
            f"<b>🥥︙يتوفر تحديث جديد للبوت!</b>\n\n🥥︙ رفع التحديثات الآن</code>\n\n**<u>🥥︙ التحديثات</u>**\n\n[اضغط هنا لمعرفه التحديثات]({url})"
        )
    else:
        nrs = await response.edit(
            _final_updates_, disable_web_page_preview=True
        )
    os.system("git stash &> /dev/null && git pull")
    if await is_heroku():
        try:
            await response.edit(
                f"{nrs.text}\n\n🥥︙تم تحديث البوت بنجاح على Heroku! الآن ، انتظر لمدة 2-3 دقائق حتى يتم إعادة تشغيل البوت!"
            )
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await response.edit(
                f"{nrs.text}\n\n🥥︙حدث خطأ ما أثناء بدء إعادة التشغيل! يرجى المحاولة مرة أخرى في وقت لاحق أو التحقق من السجلات لمزيد من المعلومات."
            )
            return await app.send_message(
                LOG_GROUP_ID,
                f"🥥︙حدث خطأ في التحديث #UPDATER بسبب : <code>{err}</code>",
            )
    else:
        await response.edit(
            f"{nrs.text}\n\n🥥︙تم تحديث البوت بنجاح على Heroku! الآن ، انتظر لمدة 2-3 دقائق حتى يتم إعادة تشغيل البوت!"
        )
        os.system("pip3 install -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && bash start")
        exit()
    return


@app.on_message(filters.command("restart") & filters.user(SUDOERS))
async def restart_(_, message):
    response = await message.reply_text("🥥︙يتم التحديث....")
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n🥥︙لتحديث تطبيقك ، تحتاج إلى إعداد ملف `HEROKU_API_KEY` و `HEROKU_APP_NAME` الفارات بالتوالي"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
              "<b>🥥︙تم اكتشاف تطبيق هيروكو!</b>\n\n<b>تأكد من وضعك</b> `HEROKU_API_KEY` **و** `HEROKU_APP_NAME` <b>الفار بشكل صحيح حتى تتمكن من التحديث عن بُعد!</b>"
            )
        try:
            served_chats = []
            try:
                chats = await get_active_chats()
                for chat in chats:
                    served_chats.append(int(chat["chat_id"]))
            except Exception as e:
                pass
            for x in served_chats:
                try:
                    await app.send_message(
                        x,
                        f"🥥︙بوت {MUSIC_BOT_NAME} قام بتحديث نفسه. نأسف للأعطال.\n\n🥥︙قم بالتشغيل بعد 10-15 مجددا.",
                    )
                    await remove_active_chat(x)
                    await remove_active_video_chat(x)
                except Exception:
                    pass
            heroku3.from_key(HEROKU_API_KEY).apps()[HEROKU_APP_NAME].restart()
            await response.edit(
                "**🥥︙تحديث هيروكا**\n\n🥥︙تم بدء إعادة التشغيل بنجاح! انتظر لمدة 1-2 دقيقة حتى يتم إعادة تشغيل البوت."
            )
            return
        except Exception as err:
            await response.edit(
                "🥥︙حدث خطأ ما أثناء بدء إعادة التشغيل! يرجى المحاولة مرة أخرى في وقت لاحق أو التحقق من السجلات لمزيد من المعلومات."
            )
            return
    else:
        served_chats = []
        try:
            chats = await get_active_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
        except Exception as e:
            pass
        for x in served_chats:
            try:
                await app.send_message(
                    x,
                          f"🥥︙بوت {MUSIC_BOT_NAME} قام بتحديث نفسه. نأسف للأعطال.\n\n🥥︙قم بالتشغيل بعد 10-15 مجددا.",
                )
                await remove_active_chat(x)
                await remove_active_video_chat(x)
            except Exception:
                pass
        A = "downloads"
        B = "raw_files"
        C = "cache"
        D = "search"
        try:
            shutil.rmtree(A)
            shutil.rmtree(B)
            shutil.rmtree(C)
            shutil.rmtree(D)
        except:
            pass
        await asyncio.sleep(2)
        try:
            os.mkdir(A)
        except:
            pass
        try:
            os.mkdir(B)
        except:
            pass
        try:
            os.mkdir(C)
        except:
            pass
        try:
            os.mkdir(D)
        except:
            pass
        await response.edit(
            "🥥︙ تم بدء إعادة التشغيل بنجاح! انتظر لمدة 1-2 دقيقة حتى يتم إعادة تشغيل الروبوت."
        )
        os.system(f"kill -9 {os.getpid()} && bash start")
