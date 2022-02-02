import os
import re

import lyricsgenius
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import VideosSearch

from Yukki import MUSIC_BOT_NAME, app

__MODULE__ = "كلمات"
__HELP__ = """

🥥︙ /Lyrics [اسم الاغنيه]
- لجلب كلمات الاغنيه.

**ملحوظه**:
🥥︙يحتوي الزر المضمن في الأغاني على بعض الأخطاء. يبحث فقط عن 50٪ من النتائج. يمكنك استخدام الأمر بدلاً من ذلك إذا كنت تريد كلمات لأي موسيقى يتم تشغيلها.

"""


@app.on_callback_query(filters.regex(pattern=r"lyrics"))
async def lyricssex(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    try:
        id, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"🥥︙حدث خطأ\n🥥︙**يمكن أن يكون السبب المحتمل**:{e}"
        )
    url = f"https://www.youtube.com/watch?v={id}"
    print(url)
    try:
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = result["title"]
    except Exception as e:
        return await CallbackQuery.answer(
            "🥥︙الصوت غير موجود. مشاكل يوتيوب.", show_alert=True
        )
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    t = re.sub(r"[^\w]", " ", title)
    y.verbose = False
    S = y.search_song(t, get_full_info=False)
    if S is None:
        return await CallbackQuery.answer(
            "Lyrics not found :p", show_alert=True
        )
    await CallbackQuery.message.delete()
    userid = CallbackQuery.from_user.id
    usr = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    xxx = f"""
**🥥︙كلمات البحث مدعوم من {MUSIC_BOT_NAME}**

**🥥︙بحثت بواسطة: -** {usr}
**🥥︙الأغنية التي تم البحث عنها: -** __{title}__

**🥥︙كلمات وجدت ل: -** __{S.title}__
**🥥︙الفنان:-** {S.artist}

**__🥥︙الكلمات__**

{S.lyrics}"""
    if len(xxx) > 4096:
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await CallbackQuery.message.reply_document(
            document=filename,
            caption=f"**🥥︙انتاج:**\n\n🥥︙`كلمات`",
            quote=False,
        )
        os.remove(filename)
    else:
        await CallbackQuery.message.reply_text(xxx)


@app.on_message(filters.command("lyrics"))
async def lrsearch(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**🥥︙الاستخدام**\n\n/lyrics [ اسم الاغنيه]")
    m = await message.reply_text("Searching Lyrics")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("🥥︙لم اجد كلمات الاغنيه :p")
    xxx = f"""
**🥥︙تم البحث عن طريث {MUSIC_BOT_NAME}**

**🥥︙الباحث :-** __{query}__
**🥥︙وجدت ل:-** __{S.title}__
**🥥︙الفنان:-** {S.artist}

**__🥥︙الكلمات:__**

{S.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**🥥︙انتاج:**\n\n🥥︙`كلمات`",
            quote=False,
        )
        os.remove(filename)
    else:
        await m.edit(xxx)
