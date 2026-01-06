from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType, ParseMode
from pyrogram.errors import (
    ChatSendPlainForbidden,
    ChatWriteForbidden,
    Forbidden,
    ChannelPrivate,
)

from AviaxMusic import app
from config import OWNER_ID


# Safe Reply (HTML)
async def _safe_reply_text(message: Message, text: str):
    chat = getattr(message, "chat", None)
    if not chat or chat.type == ChatType.CHANNEL:
        return
    try:
        await message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except (ChatSendPlainForbidden, ChatWriteForbidden, Forbidden, ChannelPrivate):
        pass


# 🎙 Voice Chat Started
@app.on_message(filters.video_chat_started & filters.group)
async def on_voice_chat_started(_, message: Message):
    text = (
        "🎙 <b>𝖵𝗈𝗂𝖼𝖾 𝖢𝗁𝖺𝗍 𝖲𝗍𝖺𝗋𝗍𝖾𝖽</b>\n"
        "<i>𝖩𝗈𝗂𝗇 𝖺𝗇𝖽 𝖾𝗇𝗃𝗈𝗒 𝗍𝗁𝖾 𝖼𝗈𝗇𝗏𝖾𝗋𝗌𝖺𝗍𝗂𝗈𝗇 ✨</i>"
    )
    await _safe_reply_text(message, text)


# 🔕 Voice Chat Ended
@app.on_message(filters.video_chat_ended & filters.group)
async def on_voice_chat_ended(_, message: Message):
    text = (
        "🔕 <b>𝖵𝗈𝗂𝖼𝖾 𝖢𝗁𝖺𝗍 𝖤𝗇𝖽𝖾𝖽</b>\n"
        "<i>𝖳𝗁𝖺𝗇𝗄𝗌 𝖿𝗈𝗋 𝗃𝗈𝗂𝗇𝗂𝗇𝗀 💙</i>"
    )
    await _safe_reply_text(message, text)


# 👥 Voice Chat Invite
@app.on_message(filters.video_chat_members_invited & filters.group)
async def on_voice_chat_members_invited(_, message: Message):
    if message.from_user:
        inviter_name = message.from_user.first_name or "User"
        inviter = f"<a href='tg://user?id={message.from_user.id}'>{inviter_name}</a>"
    else:
        inviter = "User"

    invited_users = []
    vcmi = getattr(message, "video_chat_members_invited", None)
    users = getattr(vcmi, "users", []) if vcmi else []

    for user in users:
        name = user.first_name or "User"
        invited_users.append(
            f"<a href='tg://user?id={user.id}'>{name}</a>"
        )

    if invited_users:
        text = (
            "👥 <b>𝖵𝗈𝗂𝖼𝖾 𝖢𝗁𝖺𝗍 𝖨𝗇𝗏𝗂𝗍𝖾</b>\n\n"
            f"• {inviter}\n"
            f"• <b>𝖨𝗇𝗏𝗂𝗍𝖾𝖽:</b> {', '.join(invited_users)}\n\n"
            "<i>𝖳𝖺𝗉 𝗍𝗈 𝗃𝗈𝗂𝗇 𝗍𝗁𝖾 𝗏𝗈𝗂𝖼𝖾 𝖼𝗁𝖺𝗍 🎧</i>"
        )
        await _safe_reply_text(message, text)


# 👋 Leave Group
@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID) & filters.group)
async def leave_group(_, message: Message):
    text = (
        "👋 <b>𝖫𝖾𝖺𝗏𝗂𝗇𝗀 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉</b>\n"
        "<i>𝖦𝗈𝗈𝖽𝖻𝗒𝖾 & 𝗍𝖺𝗄𝖾 𝖼𝖺𝗋𝖾 🌸</i>"
    )
    await _safe_reply_text(message, text)
    try:
        await app.leave_chat(message.chat.id, delete=True)
    except (ChatWriteForbidden, Forbidden, ChannelPrivate):
        pass
