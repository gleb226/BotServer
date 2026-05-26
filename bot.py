import asyncio
import os
import sys
import threading
import customtkinter as ctk
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.databases.user_database import user_database
from app.databases.categories_database import categories_database
from app.handlers.user_handlers import user_router

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.realpath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))
TOKEN = os.getenv("BOT_TOKEN")

class BotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BotServer Controller")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.label = ctk.CTkLabel(self, text="BotServer is starting...", font=("Helvetica", 18))
        self.label.pack(pady=40)

        self.status_label = ctk.CTkLabel(self, text="Status: Starting", text_color="yellow")
        self.status_label.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Bot", command=self.stop_bot, fg_color="red", hover_color="darkred")
        self.stop_button.pack(pady=20)

        self.loop = None
        self.bot_thread = threading.Thread(target=self.run_bot_async, daemon=True)
        self.bot_thread.start()

    def run_bot_async(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.start_bot())
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}", text_color="red"))

    async def start_bot(self):
        if not TOKEN:
            self.after(0, lambda: self.status_label.configure(text="Error: BOT_TOKEN missing!", text_color="red"))
            return

        bot = Bot(token=TOKEN)
        dp = Dispatcher()
        user_database()
        categories_database()
        dp.include_router(user_router)

        self.after(0, lambda: self.status_label.configure(text="Status: Running", text_color="green"))
        self.after(0, lambda: self.label.configure(text="BotServer is Active"))

        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()

    def stop_bot(self):
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    if not TOKEN and not getattr(sys, 'frozen', False):
        print("BOT_TOKEN not found!")
    
    app = BotApp()
    app.mainloop()
