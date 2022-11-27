# (c) Adarsh-Goel
import os
import asyncio
import logging
from asyncio import TimeoutError
from YasirRoBot.bot import StreamBot
from YasirRoBot.utils.database import Database
from YasirRoBot.utils.human_readable import humanbytes
from YasirRoBot.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from YasirRoBot.utils.file_properties import get_name, get_hash, get_media_file_size

db = Database(Var.DATABASE_URL, Var.name)
logger = logging.getLogger(__name__)

MY_PASS = os.environ.get("MY_PASS", None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


@StreamBot.on_message((filters.regex("login🔑") | filters.command("login")), group=4)
async def login_handler(c: Client, m: Message):
    try:
        try:
            ag = await m.reply_text("Now send me password.\n\n If You don't know check the MY_PASS Variable in heroku \n\n(You can use /cancel command to cancel the process)")
            _text = await c.listen(m.chat.id, filters=filters.text, timeout=90)
            if _text.text:
                textp = _text.text
                if textp == "/cancel":
                    await ag.edit("Process Cancelled Successfully")
                    return
            else:
                return
        except TimeoutError:
            await ag.edit("I can't wait more for password, try again")
            return
        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            ag_text = "yeah! you entered the password correctly"
        else:
            ag_text = "Wrong password, try again"
        await ag.edit(ag_text)
    except Exception as e:
        print(e)


@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo), group=4)
async def private_receive_handler(c: Client, m: Message):
    if await db.is_banned(int(m.from_user.id)):
        return await m.reply("🚫 Maaf, kamu dibanned dari bot ini oleh owner saya karena kamu melanggar aturan penggunaan bot. Terimakasih..\n\n🚫 Sorry, you have been banned from this bot because you have violated the user rules. Thank you..")
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(m.chat.id)
        if check_pass == None:
            await m.reply_text("Login first using /login cmd \n don't know the pass? request it from the Developer")
            return
        if check_pass != MY_PASS:
            await pass_db.delete_user(m.chat.id)
            return
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(Var.BIN_CHANNEL, f"New User Joined! : \n\n Name : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started Your Bot!!")
    if Var.UPDATES_CHANNEL:
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status.value == "kicked":
                await c.send_message(chat_id=m.chat.id, text="You are banned!\n\n  **Contact Owner [Yasir Aris](https://t.me/yasirarism) maybe he will help you**", disable_web_page_preview=True)
                return
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>Join Updates Channel To Use Me 🔐</i>""",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")]]),
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(chat_id=m.chat.id, text="**Something Went Wrong. Contact My Owner** [Yasir Aris M](https://github.com/yasirarism)", disable_web_page_preview=True)
            return
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        file_hash = get_hash(log_msg, Var.HASH_LENGTH)
        logger.info(get_name(log_msg))
        stream_link = f"{Var.URL}tonton/{log_msg.id}/{quote_plus(get_name(log_msg))}?hash={file_hash}"
        online_link = f"{Var.URL}unduh/{log_msg.id}/{quote_plus(get_name(log_msg))}?hash={file_hash}"

        msg_text = """
<i><u>Hai {}, Link mu sudah digenerate! 🤓</u></i>
<b>📂 Nama File :</b> <code>{}</code>
<b>📦 Ukuran File :</b> <code>{}</code>
<b>📥 Download Video :</b> <code>{}</code>
<b>🖥 Tonton Video nya  :</b> <code>{}</code>

<b>🚸CATATAN : Dilarang menggunakan bot ini untuk download Po*n, Link tidak akan expired kecuali ada yang menyalahgunakan bot ini.</b>
© @YasirRoBot"""

        await log_msg.reply_text(text=f"**Requested By :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**User ID :** `{m.from_user.id}`\n**Stream Link :** {stream_link}", disable_web_page_preview=True, quote=True)
        await m.reply_sticker("CAACAgUAAxkBAAI7NGGrULQlM1jMxCIHijO2SIVGuNpqAAKaBgACbkBiKqFY2OIlX8c-HgQ")
        await m.reply_text(
            text=msg_text.format(m.from_user.mention, get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🖥 Streaming Link", url=stream_link), InlineKeyboardButton("📥 Download Link", url=online_link)],  # Stream Link  # Download Link
                    [InlineKeyboardButton("💰 Donasi", url=f"https://t.me/{(await c.get_me()).username}?start=donasi")],
                ]
            ),
        )
        logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
    except FloodWait as e:
        print(f"Sleeping for {str(e.value)}s")
        await asyncio.sleep(e.value)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Got floodwait of {str(e.value)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**User ID :** `{str(m.from_user.id)}`", disable_web_page_preview=True)


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo) & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(broadcast.chat.id)
        if check_pass == None:
            await broadcast.reply_text("Login first using /login cmd \n don't know the pass? request it from developer!")
            return
        if check_pass != MY_PASS:
            await broadcast.reply_text("Wrong password, login again")
            await pass_db.delete_user(broadcast.chat.id)

            return
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        try:
            log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        except Exception:
            log_msg = await broadcast.copy(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}tonton/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}unduh/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

        ubotname = (await bot.get_me()).username
        button = []
        if broadcast.chat.id == -1001686184174:
            button.append([InlineKeyboardButton("📥 Stream & Download Link", url=f"https://t.me/{ubotname}?start=YasirBot_{str(log_msg.id)}")])
            button.append([InlineKeyboardButton("💰 Donasi", url=f"https://t.me/{ubotname}?start=donasi")])
        else:
            button.append([InlineKeyboardButton("📥 Stream & Download Link", url=f"https://t.me/{ubotname}?start=YasirBot_{str(log_msg.id)}")])
        await log_msg.reply_text(text=f"**Channel Name:** `{broadcast.chat.title}`\n**CHANNEL ID:** `{broadcast.chat.id}`\n**REQUEST URL:** {stream_link}", quote=True)
        await bot.edit_message_reply_markup(chat_id=broadcast.chat.id, message_id=broadcast.id, reply_markup=InlineKeyboardMarkup(button))
    except FloodWait as w:
        print(f"Sleeping for {str(w.value)}s")
        await asyncio.sleep(w.value)
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"Got Floodwait of {str(w.value)}s from {broadcast.chat.title}\n\n**CHANNEL ID:** `{str(broadcast.chat.id)}`", disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ERROR_TRACEBACK:** `{e}`", disable_web_page_preview=True)
        print(f"Can't Edit Broadcast Message!\nERROR:  **Give me edit permission in updates and bin channels!{e}**")
