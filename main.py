import os
from dotenv import load_dotenv

from telegram.ext import Application

from handlers.start_handler import start_handler, button_handler
from handlers.face_swap import face_swap_handler, image_handler
from handlers.admin import admin_handlers
from handlers.premium import premium_handlers
from handlers.limits import limits_handlers

def main():
    load_dotenv()
    app = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    # User Handlers
    app.add_handler(start_handler)
    app.add_handler(image_handler)
    app.add_handler(button_handler)

    # Feature Handlers
    app.add_handler(face_swap_handler)
    app.add_handlers(admin_handlers)
    app.add_handlers(premium_handlers)
    app.add_handlers(limits_handlers)

    app.run_polling()

if __name__ == "__main__":
    main()
