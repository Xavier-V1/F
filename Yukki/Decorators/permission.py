from typing import Dict, List, Union

from Yukki import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        if message.chat.type == "private":
            return await mystic(_, message)
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "🍒︙احتاج الي تلك الصلاحيات حتي استطيع العمل\n"
                + "\n🍒︙اداره المحادثات المرئية للتحكم بالدردشة"
                + "\n🍒︙حذف الرسائل لحذف رسائل البوت من محادثة المجموعة"
                + "\n🍒︙دعوة اعضاء جديدة حتي استطيع دعوة الحساب المساعد للدردشة"
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "🍒︙ليس لدي صلاحية القيام بهذا الامر"
                + "\n🍒︙اعطني صلاحية اداره المحادثات المرئيه"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "🍒︙ليس لدي صلاحية القيام بهذا الامر"
                + "\n🍒︙اعطني صلاحية حذف الرسائل"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "🍒︙ليس لدي صلاحية القيام بهذا الامر"
                + "\n🍒︙اعطني  صلاحية دعوة اعضاء بالرابط"
            )
            return
        return await mystic(_, message)

    return wrapper
