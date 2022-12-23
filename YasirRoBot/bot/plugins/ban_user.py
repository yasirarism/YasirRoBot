from YasirRoBot.bot import StreamBot
from YasirRoBot.vars import Var
from pyrogram import filters
from YasirRoBot.utils.database import Database

db = Database(Var.DATABASE_URL, Var.name)


@StreamBot.on_message(filters.command("ban") & filters.private & filters.user(list(Var.OWNER_ID)))
async def ban_handler(bot, m):
    if len(m.command) == 1:
        await m.reply_text(text="🚫 Gunakan: /ban [id user] untuk membanned pengguna.")
        return
    user = m.command[1]
    if not await db.is_banned(user):
        await db.add_ban_user(user)
        await m.reply(f"🚫 User {user} succesfully banned from this bot.")
    else:
        await m.reply(f"🚫 User {user} has banned forever before.")


@StreamBot.on_message(filters.command("unban") & filters.private & filters.user(list(Var.OWNER_ID)))
async def rm_ban_handler(bot, m):
    if len(m.command) == 1:
        await m.reply_text(text="🚫 Gunakan: /unban [id user] untuk unban pengguna.")
        return
    user = m.command[1]
    if not await db.is_banned(user):
        await m.reply(f"🚫 User {user} is not added banned list before.")
    else:
        await db.remove_ban(user)
        await m.reply(f"🚫 User {user} has been banned from this bot.")
