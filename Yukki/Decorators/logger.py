from config import LOG_GROUP_ID
from Yukki.Core.Clients.cli import LOG_CLIENT
from Yukki.Database import is_on_off


def logging(mystic):
    async def wrapper(_, message):
        if await is_on_off(5):
            if message.chat.username:
                chatusername = f"@{message.chat.username}"
            else:
                chatusername = "Private Group"
            try:
                query = message.text.split(None, 1)[1]
                what = "Query Given"
            except:
                try:
                    if not message.reply_to_message:
                        what = "Command Given Only"
                    else:
                        what = "Replied to any file."
                except:
                    what = "Command"
            logger_text = f"""
__**🥥︙ مجموعة جديدة {what}**__

**🥥︙ الدردشة** {message.chat.title} [`{message.chat.id}`]
**🥥︙ العضو** {message.from_user.mention}
**🥥︙ المعرف** @{message.from_user.username}
**🥥︙ الايدي** `{message.from_user.id}`
**🥥︙اللينك** {chatusername}
**🥥︙ الرقم** {message.text}"""
            if LOG_CLIENT != "None":
                await LOG_CLIENT.send_message(
                    LOG_GROUP_ID,
                    f"{logger_text}",
                    disable_web_page_preview=True,
                )
        return await mystic(_, message)

    return wrapper
