# (c) adarsh-goel
from YasirRoBot.bot import StreamBot
from YasirRoBot.vars import Var
import logging

logger = logging.getLogger(__name__)
from YasirRoBot.bot.plugins.stream import MY_PASS
from YasirRoBot.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.name)
from pyrogram.types import ReplyKeyboardMarkup

if MY_PASS:
    buttonz = ReplyKeyboardMarkup([["start⚡️", "help📚", "login🔑", "DC", "Donate"], ["follow❤️", "ping📡", "status📊", "maintainers😎"]], resize_keyboard=True)
else:
    buttonz = ReplyKeyboardMarkup([["start⚡️", "help📚", "DC", "Donate"], ["follow❤️", "ping📡", "status📊", "maintainers😎"]], resize_keyboard=True)


@StreamBot.on_message((filters.command("start") | filters.regex("start⚡️")) & filters.private)
async def start(b, m):
    if await db.is_banned(int(m.from_user.id)):
        return await m.reply("🚫 Maaf, kamu dibanned dari bot ini oleh owner saya karena kamu melanggar aturan penggunaan bot. Terimakasih..\n\n🚫 Sorry, you have been banned from this bot because you have violated the user rules. Thank you..")
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(Var.BIN_CHANNEL, f"**New User Joined:** \n\n[{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Started Your Bot !!__")
    if Var.UPDATES_CHANNEL:
        try:
            user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await b.send_message(chat_id=m.chat.id, text="__Sorry, You're banned for using Me. Contact the bot owner__\n\n  **Maybe he will help you..**", disable_web_page_preview=True)
                return
        except UserNotParticipant:
            await StreamBot.send_photo(
                chat_id=m.chat.id,
                photo="https://telegra.ph/file/9d94fc0af81234943e1a9.jpg",
                caption="<i>Please Join Channel To Use Me, Because To Many User Flood Bot 🔐</i>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]),
            )
            return
        except Exception:
            await b.send_message(chat_id=m.chat.id, text="<i>Something When Wrong</i> <b> <a href='https://github.com/adarsh-goel'>CLICK HERE FOR SUPPORT </a></b>", disable_web_page_preview=True)
            return
    await StreamBot.send_photo(
        chat_id=m.chat.id,
        photo="https://telegra.ph/file/ca10e459bc6f48a4ad0f7.jpg",
        caption=f'Hi {m.from_user.mention(style="md")}!,\nI am Telegram File to Link Generator Bot with Channel support.\nSend me any file and get a direct download link and streamable link.!',
        reply_markup=buttonz,
    )


@StreamBot.on_message((filters.command("help") | filters.regex("help📚")) & filters.private)
async def help_handler(bot, message):
    if await db.is_banned(int(message.from_user.id)):
        return await message.reply("🚫 Maaf, kamu dibanned dari bot ini oleh owner saya karena kamu melanggar aturan penggunaan bot. Terimakasih..\n\n🚫 Sorry, you have been banned from this bot because you have violated the user rules. Thank you..")
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(Var.BIN_CHANNEL, f"**New User Joined **\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Started Your Bot !!__")
    if Var.UPDATES_CHANNEL:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(chat_id=message.chat.id, text="<i>Sorry, You're banned from using me. Contact Bot Owner.</i>", disable_web_page_preview=True)
                return
        except UserNotParticipant:
            await StreamBot.send_photo(
                chat_id=message.chat.id,
                photo="https://telegra.ph/file/ca10e459bc6f48a4ad0f7.jpg",
                Caption="**Join channel to use this bot!**\n\n__Due to many user flood, only channel subscriber can use bot!__",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🤖 Join Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]),
            )
            return
        except Exception:
            await bot.send_message(chat_id=message.chat.id, text="__Something went wrong. Contact Me__ [Yasir Aris](https://t.me/YasirArisM).", disable_web_page_preview=True)
            return
    await message.reply_text(
        text=f"{message.from_user.mention} kirimkan aku sebuah file dan aku akan mengubah nya menjadi direct link dan stream link!\nJika kamu suka dengan bot ini, kamu bisa donasi ke owner melalui:\n~ <b>QRIS</b>: https://telegra.ph/file/b6c3b568c3e7cf4d7534a.png\n~ <b>Bank Jago</b>: 109641845083\n~ <b>Dana</b>: https://link.dana.id/qr/3kqod34",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💁‍♂️ Owner", url="https://github.com/yasirarism")], [InlineKeyboardButton("💥 Source Code", url="https://github.com/yasirarism/YasirRoBot")]]),
    )
