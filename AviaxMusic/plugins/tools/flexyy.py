import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode

from AviaxMusic import app
from config import SUPPORT_GROUP


# 🔘 Support Button
BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url=SUPPORT_GROUP)]]
)


# 🎞 Media
MEDIA = {
    "cutie": "https://graph.org/file/24375c6e54609c0e4621c.mp4",
    "horny": "https://graph.org/file/eaa834a1cbfad29bd1fe4.mp4",
    "hot": "https://graph.org/file/745ba3ff07c1270958588.mp4",
    "sexy": "https://graph.org/file/58da22eb737af2f8963e6.mp4",
    "gay": "https://graph.org/file/850290f1f974c5421ce54.mp4",
    "lesbian": "https://graph.org/file/ff258085cf31f5385db8a.mp4",
    "boob": "https://i.gifer.com/8ZUg.gif",
    "cock": "https://telegra.ph/file/423414459345bf18310f5.gif",
}


# ✨ Cool SANS Templates
TEMPLATES = {
    "cutie": "🍑 <b>𝖢𝗎𝗍𝗂𝖾 𝖬𝖾𝗍𝖾𝗋</b>\n{mention} 𝗂𝗌 <b>{percent}%</b> 𝖼𝗎𝗍𝖾 🥀",
    "horny": "🔥 <b>𝖧𝗈𝗋𝗇𝗒 𝖬𝖾𝗍𝖾𝗋</b>\n{mention} 𝗂𝗌 <b>{percent}%</b> 𝗁𝗈𝗋𝗇𝗒 😏",
    "hot": "🔥 <b>𝖧𝗈𝗍 𝖬𝖾𝗍𝖾𝗋</b>\n{mention} 𝗂𝗌 <b>{percent}%</b> 𝗁𝗈𝗍 🥵",
    "sexy": "💋 <b>𝖲𝖾𝗑𝗒 𝖬𝖾𝗍𝖾𝗋</b>\n{mention} 𝗂𝗌 <b>{percent}%</b> 𝗌𝖾𝗑𝗒 💞",
    "gay": "🍷 <b>𝖦𝖺𝗒 𝖬𝖾𝗍𝖾𝗋</b>\n{mention} 𝗂𝗌 <b>{percent}%</b> 𝗀𝖺𝗒 🌈",
    "lesbian": "💜 <b>𝖫𝖾𝗌𝖻𝗂𝖺𝗇 𝖬𝖾𝗍𝖾𝗋</b>\n{mention} 𝗂𝗌 <b>{percent}%</b> 𝗅𝖾𝗌𝖻𝗂𝖺𝗇 ✨",
    "boob": "🍒 <b>𝖡𝗈𝗈𝖻 𝖲𝗂𝗓𝖾</b>\n{mention} → <b>{percent}%</b> 😳",
    "cock": "🍆 <b>𝖢𝗈𝖼𝗄 𝖲𝗂𝗓𝖾</b>\n{mention} → <b>{percent} 𝖼𝗆</b> 😈",
}


# 👤 Safe Mention (HTML)
def user_mention(user) -> str:
    name = user.first_name or "User"
    return f'<a href="tg://user?id={user.id}">{name}</a>'


# 🎯 Main Handler
async def rate_user(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply_text(
            "❌ <b>𝖪𝗂𝗌𝗂 𝗎𝗌𝖾𝗋 𝗄𝗈 𝗋𝖾𝗉𝗅𝗒 𝗄𝖺𝗋𝗄𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗎𝗌𝖾 𝗄𝖺𝗋𝗈!</b>",
            parse_mode=ParseMode.HTML,
            quote=True,
        )

    command = message.command[0].lower()
    if command not in MEDIA:
        return

    target = message.reply_to_message.from_user
    mention = user_mention(target)
    percent = random.randint(1, 100)

    caption = TEMPLATES[command].format(
        mention=mention,
        percent=percent,
    )

    media = MEDIA[command]

    if media.endswith(".gif"):
        await message.reply_animation(
            animation=media,
            caption=caption,
            reply_markup=BUTTON,
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply_video(
            video=media,
            caption=caption,
            reply_markup=BUTTON,
            parse_mode=ParseMode.HTML,
        )


# 🔗 Register Commands
for cmd in MEDIA.keys():
    app.on_message(filters.command(cmd))(rate_user)
