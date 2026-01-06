# Authored By Certified Coders © 2025
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, ChannelInvalid, ChannelPrivate
from pyrogram.enums import ParseMode

from AviaxMusic import app
from AviaxMusic.misc import SUDOERS


# 🔗 Give Invite Link (Current Chat)
@app.on_message(filters.command("givelink"))
async def give_link_command(client: Client, message: Message):
    try:
        link = await app.export_chat_invite_link(message.chat.id)
        await message.reply_text(
            f"🔗 <b>𝖨𝗇𝗏𝗂𝗍𝖾 𝖫𝗂𝗇𝗄 𝖿𝗈𝗋</b> <i>{message.chat.title}</i>\n\n"
            f"{link}",
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        await message.reply_text(
            f"❌ <b>𝖤𝗋𝗋𝗈𝗋 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝗂𝗇𝗀 𝗅𝗂𝗇𝗄</b>\n"
            f"<code>{e}</code>",
            parse_mode=ParseMode.HTML,
        )


# 🔗 Fetch Invite Link by Group ID
@app.on_message(
    filters.command(["link", "invitelink"], prefixes=["/", "!", ".", "#", "?"])
    & SUDOERS
)
async def link_command_handler(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "⚠️ <b>𝖴𝗌𝖺𝗀𝖾:</b> <code>/link &lt;group_id&gt;</code>",
            parse_mode=ParseMode.HTML,
        )

    group_id = message.command[1]
    file_name = f"group_info_{group_id}.txt"

    try:
        chat = await client.get_chat(int(group_id))
        if not chat:
            return await message.reply_text(
                "⚠️ <b>𝖢𝗈𝗎𝗅𝖽 𝗇𝗈𝗍 𝖿𝖾𝗍𝖼𝗁 𝗀𝗋𝗈𝗎𝗉 𝗂𝗇𝖿𝗈.</b>",
                parse_mode=ParseMode.HTML,
            )

        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except (ChannelInvalid, ChannelPrivate):
            return await message.reply_text(
                "🚫 <b>𝖨 𝖽𝗈𝗇’𝗍 𝗁𝖺𝗏𝖾 𝖺𝖼𝖼𝖾𝗌𝗌 𝗍𝗈 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉 / 𝖼𝗁𝖺𝗇𝗇𝖾𝗅.</b>",
                parse_mode=ParseMode.HTML,
            )
        except FloodWait as e:
            return await message.reply_text(
                f"⏳ <b>𝖱𝖺𝗍𝖾 𝖫𝗂𝗆𝗂𝗍</b>\n"
                f"𝖶𝖺𝗂𝗍 <code>{e.value}</code> 𝗌𝖾𝖼𝗈𝗇𝖽𝗌.",
                parse_mode=ParseMode.HTML,
            )

        group_data = {
            "id": chat.id,
            "type": str(chat.type),
            "title": chat.title,
            "members_count": chat.members_count,
            "description": chat.description,
            "invite_link": invite_link,
            "is_verified": chat.is_verified,
            "is_restricted": chat.is_restricted,
            "is_creator": chat.is_creator,
            "is_scam": chat.is_scam,
            "is_fake": chat.is_fake,
            "dc_id": chat.dc_id,
            "has_protected_content": chat.has_protected_content,
        }

        with open(file_name, "w", encoding="utf-8") as file:
            for key, value in group_data.items():
                file.write(f"{key}: {value}\n")

        await client.send_document(
            chat_id=message.chat.id,
            document=file_name,
            caption=(
                f"📂 <b>𝖦𝗋𝗈𝗎𝗉 𝖨𝗇𝖿𝗈</b>\n"
                f"<i>{chat.title}</i>\n\n"
                f"📌 <b>𝖲𝖼𝗋𝖺𝗉𝖾𝖽 𝖻𝗒:</b> @{app.username}"
            ),
            parse_mode=ParseMode.HTML,
        )

    except ValueError:
        await message.reply_text(
            "❌ <b>𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖦𝗋𝗈𝗎𝗉 𝖨𝖣.</b>\n"
            "𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝗏𝖺𝗅𝗂𝖽 𝗀𝗋𝗈𝗎𝗉 𝗂𝖽.",
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        await message.reply_text(
            f"❌ <b>𝖤𝗋𝗋𝗈𝗋</b>\n<code>{e}</code>",
            parse_mode=ParseMode.HTML,
        )
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
