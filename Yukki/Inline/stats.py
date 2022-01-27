from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

stats1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🎸 احصائيات النظام", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات المساحة", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات البوت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات مونجو", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🎸 احصائيات عامة", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات المساحة", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات البوت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات مونجو", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats3 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🎸 احصائيات النظام", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات عامة", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات البوت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات مونجو", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats4 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🎸 احصائيات النظام", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات المساحة", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات عامة", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات مونجو", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats5 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🎸 احصائيات النظام", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات المساحة", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات البوت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات عامة", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats6 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🎸 احصائيات النظام", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات المساحة", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات البوت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="🎸 احصائيات مونجو", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎸 احصائيات عامة", callback_data=f"gen_stats"
            )
        ],
    ]
)


stats7 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="يتم جلب احصائيات المساعد....",
                callback_data=f"wait_stats",
            )
        ]
    ]
)
