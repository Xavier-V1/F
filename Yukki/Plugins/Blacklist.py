from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import SUDOERS, app
from Yukki.Database import blacklist_chat, blacklisted_chats, whitelist_chat

__MODULE__ = "القائمه السوداء"
__HELP__ = """


🥥︙ /blacklistedchat 
- تحقق من الدردشات المدرجة في القائمة السوداء للبوت.


**ملحوظة:**
للمطورين فقط


🥥︙ /blacklistchat [ايدي الدردشه] 
- ضع أي دردشة في القائمة السوداء بواسطه البوت


🥥︙ /whitelistchat [ايدي الدردشه] 
- ضع اي دردشه في القائمه البيضاء باستخدام البوت

"""


@app.on_message(filters.command("blacklistchat") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**🥥︙الاستخدام:**\n🥥︙ /blacklistchat [ايدي الدردشه]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("🥥︙ الدردشة مدرجة بالفعل في القائمة السوداء.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "🥥︙ تم وضع الدردشة في القائمة السوداء بنجاح"
        )
    await message.reply_text("🥥︙ حدث خطأ ما ، تحقق من السجلات.")


@app.on_message(filters.command("whitelistchat") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**🥥︙ Usage:**\n🥥︙ /whitelistchat [ايدي الدردشه]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("🥥︙ الدردشة مدرجة بالفعل في القائمة البيضاء.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "🥥︙ تمت إضافة الدردشة إلى القائمة البيضاء بنجاح"
        )
    await message.reply_text("🥥︙ حدث خطأ ما ، تحقق من السجلات.")


@app.on_message(filters.command("blacklistedchat"))
async def blacklisted_chats_func(_, message: Message):
    text = "**🥥︙ الدردشات في القائمة السوداء:**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("🥥︙ لا توجد محادثات في القائمة السوداء")
    else:
        await message.reply_text(text)
