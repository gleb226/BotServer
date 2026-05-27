import asyncio
import os
import sys
import threading
import customtkinter as ctk
from PIL import Image
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

        self.title("BotServer Management Console")
        self.geometry("500x400")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="🚀 BotServer Control", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.pack(pady=(25, 10))

        self.sub_label = ctk.CTkLabel(
            self.main_frame, 
            text="Professional File Management System",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.sub_label.pack(pady=(0, 20))

        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color=("gray90", "gray16"), corner_radius=10)
        self.status_frame.pack(fill="x", padx=40, pady=10)

        self.status_dot = ctk.CTkLabel(self.status_frame, text="●", text_color="yellow", font=("Helvetica", 20))
        self.status_dot.pack(side="left", padx=(15, 5), pady=10)

        self.status_text = ctk.CTkLabel(
            self.status_frame, 
            text="Status: Initializing...", 
            font=ctk.CTkFont(size=15, weight="medium")
        )
        self.status_text.pack(side="left", pady=10)

        self.info_label = ctk.CTkLabel(
            self.main_frame, 
            text="The bot is starting up. Please wait...", 
            font=ctk.CTkFont(size=12),
            text_color="#555555"
        )
        self.info_label.pack(pady=(20, 10))

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=(10, 20))

        self.stop_button = ctk.CTkButton(
            self.button_frame, 
            text="Shutdown Bot", 
            command=self.stop_bot,
            fg_color="#E74C3C", 
            hover_color="#C0392B",
            width=150,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold")
        )
        self.stop_button.pack(side="left", padx=10)

        self.loop = None
        self.bot_thread = threading.Thread(target=self.run_bot_async, daemon=True)
        self.bot_thread.start()

    def update_status(self, text, color, dot_color=None):
        self.status_text.configure(text=f"Status: {text}")
        self.status_text.configure(text_color=color)
        if dot_color:
            self.status_dot.configure(text_color=dot_color)

    def run_bot_async(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.start_bot())
        except Exception as e:
            self.after(0, lambda: self.update_status(f"Error: {str(e)[:20]}...", "red", "red"))
            self.after(0, lambda: self.info_label.configure(text=f"Technical detail: {str(e)}", text_color="#E74C3C"))

    async def start_bot(self):
        if not TOKEN:
            self.after(0, lambda: self.update_status("Token Missing", "red", "red"))
            self.after(0, lambda: self.info_label.configure(text="Please check your .env file for BOT_TOKEN", text_color="#E74C3C"))
            return

        try:
            bot = Bot(token=TOKEN)
            dp = Dispatcher()

            user_database()
            categories_database()

            dp.include_router(user_router)

            self.after(0, lambda: self.update_status("Active", "#2ECC71", "#2ECC71"))
            self.after(0, lambda: self.info_label.configure(text="Bot is running and accepting connections", text_color="#2ECC71"))

            await dp.start_polling(bot)
        except Exception as e:
            self.after(0, lambda: self.update_status("Critical Error", "red", "red"))
            self.after(0, lambda: self.info_label.configure(text=str(e), text_color="#E74C3C"))
        finally:
            await bot.session.close()

    def stop_bot(self):
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = BotApp()
    app.mainloop()