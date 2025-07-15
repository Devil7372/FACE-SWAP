from telegram.ext import MessageHandler, filters
from utils.api_swap import swap_faces
from utils.user_db import check_limit, record_usage, is_premium

async def image_handler(update, context):
    user_id = update.effective_user.id
    user_data = context.user_data
    photo = update.message.photo[-1].file_id

    if 'first_photo' not in user_data:
        user_data['first_photo'] = photo
        await update.message.reply_text("Image #1 received! Now send the second image.")
        return
    else:
        user_data['second_photo'] = photo

    # Check daily limit or premium
    if not is_premium(user_id) and not check_limit(user_id):
        await update.message.reply_text(
            "❌ Daily free limit reached! Use /premium for unlimited swaps."
        )
        context.user_data.clear()
        return

    # Download images
    file1 = await context.bot.get_file(user_data['first_photo'])
    file2 = await context.bot.get_file(user_data['second_photo'])
    path1, path2 = f'{user_id}_1.jpg', f'{user_id}_2.jpg'
    await file1.download_to_drive(path1)
    await file2.download_to_drive(path2)

    await update.message.reply_text("Swapping faces...")

    swapped_path = swap_faces(path1, path2)  # Returns result path or raises error

    with open(swapped_path, 'rb') as f:
        await update.message.reply_photo(photo=f, caption="Here is your swapped face!")

    record_usage(user_id)
    context.user_data.clear()
    for p in [path1, path2, swapped_path]:
        try: import os; os.remove(p)
        except: pass

face_swap_handler = MessageHandler(filters.PHOTO, image_handler)
