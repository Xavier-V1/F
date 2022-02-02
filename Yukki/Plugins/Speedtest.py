import os

import speedtest
import wget
from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import BOT_ID, SUDOERS, app
from Yukki.Utilities.formatters import bytes

__MODULE__ = "اختبار السرعه"
__HELP__ = """

🥥︙ /speedtest 
- ليتم اختبار سرعه البوت

"""


@app.on_message(filters.command("speedtest") & ~filters.edited)
async def statsguwid(_, message):
    m = await message.reply_text("🥥︙يتم اختبار السرعه")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("🥥︙يتم اختبار سرعه التحميل")
        test.download()
        m = await m.edit("🥥︙يتم اختبار سرعه الرفع")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        return await m.edit(e)
    m = await m.edit("🥥︙مشاركه النتائج ")
    path = wget.download(result["share"])

    output = f"""**🥥︙نتيجه اختبار السرعه**
    
<u>**🥥︙الخادم**</u>
**__🥥︙الايبي__** {result['client']['isp']}
**__🥥︙الدوله__** {result['client']['country']}
  
<u>**🥥︙السيرفر**</u>
**__🥥︙الاسم__** {result['server']['name']}
**__🥥︙الدوله__** {result['server']['country']}, {result['server']['cc']}
**__🥥︙السرعه__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
