from Yukki import BOT_USERNAME, LOG_GROUP_ID, app
from Yukki.Database import blacklisted_chats, is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "🥥︙ انت ادمن مخفي بالمجموعة\n🥥︙ برجاء اظهار حسابك"
            )
        blacklisted_chats_list = await blacklisted_chats()
        if message.chat.id in blacklisted_chats_list:
            await message.reply_text(
                f"🥥︙**دردشة محظورة**\n\n🥥︙ تم وضع مجموعتك في القائمة السوداء قم بالتحدث للشخص من المطورين\n🥥︙ [تجد جميع المطورين هنا](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
            return await app.leave_chat(message.chat.id)
        if await is_on_off(1):
            if int(message.chat.id) != int(LOG_GROUP_ID):
                return await message.reply_text(
                    f"🥥︙ البوت تحت الصيانة اسف للأعطال"
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"🥥︙**عضو محظور**\n\n🥥︙تم حظرك من استخدام البوت اسال اي من المطورين لفك حظرك \n🥥︙ [تجد جميع المطورين هنا](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
        return await mystic(_, message)

    return wrapper


def checkerCB(mystic):
    async def wrapper(_, CallbackQuery):
        blacklisted_chats_list = await blacklisted_chats()
        if CallbackQuery.message.chat.id in blacklisted_chats_list:
            return await CallbackQuery.answer(
                "🥥︙ قام المطور بحظر المجموعة", show_alert=True
            )
        if await is_on_off(1):
            if int(CallbackQuery.message.chat.id) != int(LOG_GROUP_ID):
                return await CallbackQuery.answer(
                    "🥥︙ البوت تحت الصيانة اسف للأعطال",
                    show_alert=True,
                )
        if await is_gbanned_user(CallbackQuery.from_user.id):
            return await CallbackQuery.answer(
                "🥥︙ انت محظور", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
