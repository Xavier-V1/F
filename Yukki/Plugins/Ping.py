import os
import time
from datetime import datetime

import psutil
from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import BOT_USERNAME, MUSIC_BOT_NAME, app, boottime
from Yukki.Utilities.ping import get_readable_time

__MODULE__ = "البينج"
__HELP__ = """

🥥︙ /ping - معرفه ائا كان البوت يعمل او لا.
"""


async def bot_sys_stats():
    bot_uptime = int(time.time() - boottime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
🥥︙وقت البدء {get_readable_time((bot_uptime))}
🥥︙المعالج {cpu}%
🥥︙الرام {mem}%
🥥︙التخزين {disk}%"""
    return stats


@app.on_message(filters.command(["ping", f"ping@{BOT_USERNAME}"]))
async def ping(_, message):
    start = datetime.now()
    response = await message.reply_photo(
        photo="Utils/Query.jpg",
        caption=">> بونج",
    )
    uptime = await bot_sys_stats()
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit_text(
        f"**🥥︙بونج**\n`🥥︙{resp} ⚡`\n\n<b><u>🥥︙ بوت{MUSIC_BOT_NAME} حاله نظام</u></b>{uptime}"
    )
