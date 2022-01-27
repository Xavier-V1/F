from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from config import MUSIC_BOT_NAME, SUPPORT_CHANNEL, SUPPORT_GROUP
from Yukki import BOT_USERNAME


def setting_markup2():
    buttons = [
        [
            InlineKeyboardButton(text="🎸 جودة الصوت", callback_data="AQ"),
            InlineKeyboardButton(text="🎸 حجم الصوت", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="🎸 المستخدمون المعتمدون", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="🎸 لوحه التحكم", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="اغلاق ✗", callback_data="close"),
        ],
    ]
    return f"🎸  **{MUSIC_BOT_NAME} الاعدادات**", buttons


def start_pannel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎸 قائمة اوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎸 الاعدادات", callback_data="settingm"
                )
            ],
        ]
        return f"🎸  **هذا هو {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎸 قائمة اوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎸 الاعدادات", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎸 جروب الدعم", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎸 **هذا هو {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎸 قائمة اوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎸 الاعدادات", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎸 قناة السورس", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
        ]
        return f"🎸 **هذا هو {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎸 قائمة اوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎸 الاعدادات", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎸 قناة السورس", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="🎸 جروب الدعم", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎸 **هذا هو {MUSIC_BOT_NAME}**", buttons


def private_panel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎸 قائمة اوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ اضفني الي مجموعتك",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
        ]
        return f"🎸 **هذا هو {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎸 قائمة اوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ اضفني الي مجموعتك",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎸 جروب الدعم", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎸 **هذا هو {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎸 قائمة اوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ اضفني الي مجموعتك",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎸 قناة السورس", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
        ]
        return f"🎸  **هذا هو {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🎸 قائمة اوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ اضفني الي مجموعتك",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎸 قناة السورس", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="🎸 جروب الدعم", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎸  **هذا هو {MUSIC_BOT_NAME}**", buttons


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="🎸 جودة الصوت", callback_data="AQ"),
            InlineKeyboardButton(text="🎸 حجم الصوت", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="🎸 المستخدمون المعتمدون", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="🎸 لوحه التحكم", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="اغلاق ✗", callback_data="close"),
            InlineKeyboardButton(text="🔙 رجوع", callback_data="okaybhai"),
        ],
    ]
    return f"🎸  **{MUSIC_BOT_NAME} الاعدادات**", buttons


def volmarkup():
    buttons = [
        [
            InlineKeyboardButton(
                text="🎸 اعادة تعيين الصوت ", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🎸 منخفض", callback_data="LV"),
            InlineKeyboardButton(text="🎸 متوسط", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🎸 عالي", callback_data="HV"),
            InlineKeyboardButton(text="🎸 مضخم", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🎸 حجم مخصص ", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 رجوع", callback_data="settingm")],
    ]
    return f"🎸  **{MUSIC_BOT_NAME} الاعدادات**", buttons


def custommarkup():
    buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🎸 صوت مخصص ", callback_data="AV")],
    ]
    return f"🎸  **{MUSIC_BOT_NAME} الاعدادات**", buttons


def usermarkup():
    buttons = [
        [
            InlineKeyboardButton(text="👥 الجميع", callback_data="EVE"),
            InlineKeyboardButton(text="🙍 الادمنية", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="🎸 قائمة الاعضاء المعتمدة", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 رجوع", callback_data="settingm")],
    ]
    return f"🎸  **{MUSIC_BOT_NAME} الاعدادات**", buttons


def dashmarkup():
    buttons = [
        [
            InlineKeyboardButton(text="✔️ مدة التشغيل", callback_data="UPT"),
            InlineKeyboardButton(text="💾 الرام", callback_data="RAT"),
        ],
        [
            InlineKeyboardButton(text="💻 معالج", callback_data="CPT"),
            InlineKeyboardButton(text="💽 ذاكره", callback_data="DIT"),
        ],
        [InlineKeyboardButton(text="🔙 رجوع", callback_data="settingm")],
    ]
    return f"🎸  **{MUSIC_BOT_NAME} الاعدادات**", buttons
