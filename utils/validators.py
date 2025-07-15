import os
from functools import wraps

FORCE_SUB_CHANNEL = os.getenv('FORCE_SUB_CHANNEL')

def force_join_required(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        try:
            member = await context.bot.get_chat_member(FORCE_SUB_CHANNEL, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                raise Exception()
        except:
            btn = [[
                {'text': "🔗 Join Channel", 'url': f'https://t.me/{FORCE_SUB_CHANNEL[1:]}'},
                {'text': "✅ I've joined", 'callback_data': 'refresh'}
            ]]
            await update.message.reply_text(
                "Please join the channel to use the bot.",
                reply_markup=btn,
                parse_mode='HTML'
            )
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
