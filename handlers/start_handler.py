import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from utils.user_db import add_or_update_user
from utils.validators import force_join_required

FORCE_SUB_CHANNEL = os.getenv('FORCE_SUB_CHANNEL')
DISCUSSION_GROUP = os.getenv('DISCUSSION_GROUP')

@force_join_required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_or_update_user(user)
    keyboard = [
        [InlineKeyboardButton("💬 Discussion", url=DISCUSSION_GROUP)],
        [InlineKeyboardButton("ℹ️ About", callback_data="about"),
         InlineKeyboardButton("📝 Help", callback_data="help")],
        [InlineKeyboardButton("🚀 Premium", callback_data="premium")]
    ]
    await update.message.reply_text(
        f"👋 Welcome, <b>{user.first_name}</b>!\n"
        "Send two selfies. You get 3 free face swaps daily.\n",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'about':
        from handlers.admin import about
        await about(update, context)
    elif query.data == 'help':
        from handlers.admin import help_cmd
        await help_cmd(update, context)
    elif query.data == 'premium':
        from handlers.premium import premium
        await premium(update, context)
    elif query.data == 'refresh':
        await start(update, context)

start_handler = CommandHandler("start", start)
button_handler = CallbackQueryHandler(button_handler)
