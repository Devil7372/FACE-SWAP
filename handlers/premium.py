from telegram.ext import CommandHandler

PREMIUM_PRICE = "$2/month"

async def premium(update, context):
    await update.callback_query.edit_message_text(
        f"🔓 <b>Premium:</b>\nUnlimited swaps for {PREMIUM_PRICE}\nContact admin to purchase.",
        parse_mode='HTML'
    )

premium_handlers = [
    CommandHandler("premium", premium)
]
