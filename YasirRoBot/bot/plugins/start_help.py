# (c) adarsh-goel
from YasirRoBot.bot import StreamBot
from YasirRoBot.vars import Var
import logging
from YasirRoBot.bot.plugins.stream import MY_PASS
from YasirRoBot.utils.database import Database
from YasirRoBot.utils.human_readable import humanbytes
from pyrogram import filters
from urllib.parse import quote_plus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ReplyKeyboardMarkup
from YasirRoBot.utils.file_properties import get_name, get_hash, get_media_file_size

db = Database(Var.DATABASE_URL, Var.name)
logger = logging.getLogger(__name__)

if MY_PASS:
    buttonz = ReplyKeyboardMarkup([["start⚡️", "help📚", "login🔑", "DC", "Donate"], ["follow❤️", "ping📡", "status📊", "maintainers😎"]], resize_keyboard=True)
else:
    buttonz = ReplyKeyboardMarkup([["start⚡️", "help📚", "DC", "Donate"], ["follow❤️", "ping📡", "status📊", "maintainers😎"]], resize_keyboard=True)


@StreamBot.on_message((filters.command("start") | filters.regex("^start⚡️") | filters.regex("^Donate")) & filters.private)
async def start(b, m):
    if await db.is_banned(int(m.from_user.id)):
        return await m.reply("🚫 Maaf, kamu dibanned dari bot ini oleh owner saya karena kamu melanggar aturan penggunaan bot. Terimakasih..\n\n🚫 Sorry, you have been banned from this bot because you have violated the user rules. Thank you..")
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(Var.BIN_CHANNEL, f"**New User Joined:** \n\n[{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Started Your Bot !!__")
    if Var.UPDATES_CHANNEL:
        try:
            user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status.value == "kicked":
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
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start" or usr_cmd == "start⚡️":
        await m.reply_sticker("CAACAgUAAxkBAAI7LmGrSXRRncbHQiifxd0f6gbqO0iSAAL5AAM0dhBWbFxFr9ji9CoeBA", reply_markup=buttonz)
        await m.reply_text(
            text=f"""
👋 Hai {m.from_user.mention}, aku adalah <b>YasirRoBot</b>. Bot yang bisa mengubah file Telegram menjadi direct link dan link streaming tanpa nunggu lama.\n
Kirimkan aku sebuah file atau video dan lihat keajaiban yang terjadi!
Klik /help untuk melihat info lengkapnya.\n
<b>🍃 Bot dibuat oleh :</b>@YasirArisM
<b><u>PERINGATAN 🚸</u></b>
<b>Jangan Spam bot!!!.</b>""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Owner", url=f"https://t.me/{Var.OWNER_USERNAME}"), InlineKeyboardButton("YasirPediaChannel", url="https://t.me/YasirPediaChannel")]]),
        )
    elif m.text == "/start donasi" or m.text == "Donate":
        await m.reply_photo("https://telegra.ph/file/b6c3b568c3e7cf4d7534a.png", caption="🌟 Jika kamu merasa bot ini sangat bermanfaat, kamu bisa donasi dengan scan kode QRIS yang ada di gambar in. Berapapun nilainya saya sangat berterimakasih..")
    else:
        log_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))
        file_hash = get_hash(log_msg, Var.HASH_LENGTH)
        try:
            filename = quote_plus(get_name(log_msg))
        except:
            filename = ""
        stream_link = f"{Var.URL}tonton/{log_msg.id}/{filename}?hash={file_hash}"
        online_link = f"{Var.URL}{log_msg.id}/{filename}?hash={file_hash}"

        msg_text = """
<u>Hai {}, Link kamu berhasil di generate! 🤓</u>
<b>📂 Nama File :</b> <code>{}</code>
<b>📦 Ukuran File :</b> <code>{}</code>
<b>📥 Download Video :</b> <code>{}</code>
<b>🖥 Tonton Video nya  :</b> <code>{}</code>

<b>🚸 Catatan :</b> Dilarang Menggunakan Bot ini Untuk Download Porn, jika ketahuan saya akan menghentikan layanan bot ini.</b>
<i>© @YasirRoBot </i>"""

        await m.reply_sticker("CAACAgUAAxkBAAI7NGGrULQlM1jMxCIHijO2SIVGuNpqAAKaBgACbkBiKqFY2OIlX8c-HgQ")
        await m.reply_text(
            text=msg_text.format(m.from_user.mention, get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🖥 Stream Link", url=stream_link), InlineKeyboardButton("📥 Download Link", url=online_link)],  # Stream Link  # Download Link
                    [InlineKeyboardButton("💰 Donasi ke Owner", url=f"https://t.me/{(await b.get_me()).username}?start=donasi")],
                ]
            ),
        )
        logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")


@StreamBot.on_message((filters.command("help") | filters.regex("^help📚")) & filters.private)
async def help_handler(bot, message):
    if await db.is_banned(int(message.from_user.id)):
        return await message.reply("🚫 Maaf, kamu dibanned dari bot ini oleh owner saya karena kamu melanggar aturan penggunaan bot. Terimakasih..\n\n🚫 Sorry, you have been banned from this bot because you have violated the user rules. Thank you..")
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(Var.BIN_CHANNEL, f"**New User Joined **\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Started Your Bot !!__")
    if Var.UPDATES_CHANNEL:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status.value == "kicked":
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
