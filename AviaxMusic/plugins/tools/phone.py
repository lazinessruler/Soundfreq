import aiohttp
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from AviaxMusic import app

API_KEY = "f66950368a61ebad3cba9b5924b4532d"
API_URL = "http://apilayer.net/api/validate"


@app.on_message(filters.command("phone"))
async def check_phone(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "📱 <b>𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝗉𝗁𝗈𝗇𝖾 𝗇𝗎𝗆𝖻𝖾𝗋.</b>\n\n"
            "<b>𝖴𝗌𝖺𝗀𝖾:</b> <code>/phone &lt;number&gt;</code>",
            parse_mode=ParseMode.HTML
        )

    number = message.command[1]

    params = {
        "access_key": API_KEY,
        "number": number,
        "country_code": "",
        "format": 1
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params=params) as response:
                if response.status != 200:
                    return await message.reply_text(
                        "❌ <b>𝖭𝖾𝗍𝗐𝗈𝗋𝗄 𝖾𝗋𝗋𝗈𝗋.</b>\n"
                        "<i>𝖠𝖯𝖨 𝗇𝗈𝗍 𝗋𝖾𝖺𝖼𝗁𝖺𝖻𝗅𝖾.</i>",
                        parse_mode=ParseMode.HTML
                    )

                data = await response.json()

                if not data.get("valid"):
                    return await message.reply_text(
                        "❌ <b>𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗉𝗁𝗈𝗇𝖾 𝗇𝗎𝗆𝖻𝖾𝗋.</b>",
                        parse_mode=ParseMode.HTML
                    )

                result = (
                    "📞 <b>𝖵𝖺𝗅𝗂𝖽 𝖯𝗁𝗈𝗇𝖾 𝖣𝖾𝗍𝖺𝗂𝗅𝗌</b>\n\n"
                    f"➤ <b>𝖭𝗎𝗆𝖻𝖾𝗋:</b> <code>{number}</code>\n"
                    f"➤ <b>𝖢𝗈𝗎𝗇𝗍𝗋𝗒:</b> <code>{data.get('country_name', 'N/A')} "
                    f"({data.get('country_code', 'N/A')})</code>\n"
                    f"➤ <b>𝖫𝗈𝖼𝖺𝗍𝗂𝗈𝗇:</b> <code>{data.get('location', 'N/A')}</code>\n"
                    f"➤ <b>𝖢𝖺𝗋𝗋𝗂𝖾𝗋:</b> <code>{data.get('carrier', 'N/A')}</code>\n"
                    f"➤ <b>𝖣𝖾𝗏𝗂𝖼𝖾 𝖳𝗒𝗉𝖾:</b> <code>{data.get('line_type', 'N/A')}</code>"
                )

                return await message.reply_text(
                    result,
                    parse_mode=ParseMode.HTML
                )

    except aiohttp.ClientError as e:
        return await message.reply_text(
            f"⚠️ <b>𝖭𝖾𝗍𝗐𝗈𝗋𝗄 𝖤𝗋𝗋𝗈𝗋:</b>\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        return await message.reply_text(
            f"⚠️ <b>𝖴𝗇𝗄𝗇𝗈𝗐𝗇 𝖤𝗋𝗋𝗈𝗋:</b>\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )
