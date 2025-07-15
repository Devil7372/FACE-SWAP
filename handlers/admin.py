import os
from telegram.ext import CommandHandler

from utils.user_db import user_stats, db_size

OWNER_ID = int(os.getenv('OWNER_ID'))
OWNER_USERNAME = os.getenv('OWNER_USERNAME')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')

async def about(update, context):
    total = user_stats()
    size_kb = db_size()
    text = (
        f"<b>🤖 About</b>\n"
        f"Owner: @{OWNER_USERNAME} ({OWNER_ID})\n"
        f"Users: <code>{total}</code>\n"
        f"DB: <code>{size_kb} KB</code>\n"
        f"Logs: {LOG_CHANNEL}"
    )
    await update.callback_query.edit_message_text(text, parse_mode='HTML')

async def help_cmd(update, context):
    msg = (
        "<b>Help:</b>\n"
        "Send 2 photos and get started!\n"
        "You have 3 free swaps per day."
    )
    if update.callback_query:
        await update.callback_query.edit_message_text(msg, parse_mode='HTML')
    else:
        await update.message.reply_text(msg, parse_mode='HTML')

async def stats(update, context):
    await update.message.reply_text(f"Total users: {user_stats()}. DB size: {db_size()} KB.")

async def broadcast(update, context):
    if update.effective_user.id != OWNER_ID:
        return
    txt = update.message.text.split(maxsplit=1)
    if len(txt) < 2:
        await update.message.reply_text("Usage: /broadcast <msg>")
        return
    msg = txt[1]
    from utils.user_db import broadcast_all
    sent = broadcast_all(context, msg)
    await update.message.reply_text(f"Broadcast sent to {sent} users.")

admin_handlers = [
    CommandHandler("about", about),
    CommandHandler("help", help_cmd),
    CommandHandler("stats", stats),
    CommandHandler("broadcast", broadcast),
]
