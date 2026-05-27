import asyncio
import os
import sys
import threading
from datetime import datetime, timedelta
import customtkinter as ctk
from PIL import Image
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.databases.user_database import user_database, db
from app.databases.categories_database import categories_database
from app.handlers.user_handlers import user_router, LiqPayManager
from app.common.config import LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY, STORAGE_PLANS, translations, VERSION
from app.utils.file_utils import clear_user_data

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.realpath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))
TOKEN = os.getenv("BOT_TOKEN")

async def background_scheduler(bot: Bot):
    liqpay = LiqPayManager(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    while True:
        try:
            pending = db.get_pending_payments()
            for item in pending:
                if isinstance(item, tuple): u_id, o_id, p_id = item
                else: u_id, o_id, p_id = item['user_id'], item['pending_order_id'], item['pending_plan_id']
                res = await liqpay.get_status(o_id)
                if res.get("status") in ["success", "wait_accept"]:
                    plan = STORAGE_PLANS.get(p_id)
                    if plan:
                        db.set_storage_limit(u_id, float(plan["size"]))
                        db.clear_pending_payment(u_id)
                        lang = db.get_language(u_id) or "English"
                        try: await bot.send_message(u_id, translations[lang]["payment_success"].format(plan["size"]))
                        except: pass

            users = db.get_all_users_with_subscription()
            for user in users:
                if isinstance(user, tuple): u_id, last_pay, limit, lang = user
                else: u_id, last_pay, limit, lang = user['user_id'], user['last_payment_date'], user['storage_limit_gb'], user['language']
                if last_pay:
                    pay_date = datetime.strptime(last_pay, "%Y-%m-%d")
                    days_passed = (datetime.now() - pay_date).days
                    lang = lang or "English"
                    t = translations[lang]
                    if days_passed >= 30:
                        db.set_storage_limit(u_id, 2.0)
                        clear_user_data(u_id)
                        try: await bot.send_message(u_id, t["subscription_cancelled"])
                        except: pass
                    elif days_passed >= 27:
                        kb = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text=t["renew_button"], callback_data="renew_sub")],
                            [InlineKeyboardButton(text=t["cancel_subscription"], callback_data="cancel_sub_confirm")]
                        ])
                        try: await bot.send_message(u_id, t["subscription_reminder"], reply_markup=kb)
                        except: pass
        except Exception as e: print(f"Scheduler error: {e}")
        await asyncio.sleep(3600)

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
        self.header_label = ctk.CTkLabel(self.main_frame, text="🚀 BotServer Control", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=(25, 10))
        self.sub_label = ctk.CTkLabel(self.main_frame, text="Professional File Management System", font=ctk.CTkFont(size=14), text_color="gray")
        self.sub_label.pack(pady=(0, 20))
        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color=("gray90", "gray16"), corner_radius=10)
        self.status_frame.pack(fill="x", padx=40, pady=10)
        self.status_dot = ctk.CTkLabel(self.status_frame, text="●", text_color="yellow", font=("Helvetica", 20))
        self.status_dot.pack(side="left", padx=(15, 5), pady=10)
        self.status_text = ctk.CTkLabel(self.status_frame, text="Status: Initializing...", font=ctk.CTkFont(size=15, weight="bold"))
        self.status_text.pack(side="left", pady=10)
        self.info_label = ctk.CTkLabel(self.main_frame, text="The bot is starting up. Please wait...", font=ctk.CTkFont(size=12), text_color="#555555")
        self.info_label.pack(pady=(20, 10))
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=(10, 20))
        self.stop_button = ctk.CTkButton(self.button_frame, text="Shutdown Bot", command=self.stop_bot, fg_color="#E74C3C", hover_color="#C0392B", width=150, height=35, corner_radius=8, font=ctk.CTkFont(weight="bold"))
        self.stop_button.pack(side="left", padx=10)
        self.loop = None
        self.bot_thread = threading.Thread(target=self.run_bot_async, daemon=True)
        self.bot_thread.start()

    def update_status(self, text, color, dot_color=None):
        self.status_text.configure(text=f"Status: {text}"); self.status_text.configure(text_color=color)
        if dot_color: self.status_dot.configure(text_color=dot_color)

    def run_bot_async(self):
        self.loop = asyncio.new_event_loop(); asyncio.set_event_loop(self.loop)
        try: self.loop.run_until_complete(self.start_bot())
        except Exception as e: self.after(0, lambda: self.update_status(f"Error: {str(e)[:20]}...", "red", "red"))

    async def start_bot(self):
        if not TOKEN: self.after(0, lambda: self.update_status("Token Missing", "red", "red")); return
        try:
            bot = Bot(token=TOKEN); dp = Dispatcher(); dp.include_router(user_router)
            self.after(0, lambda: self.update_status("Active", "#2ECC71", "#2ECC71"))
            self.after(0, lambda: self.info_label.configure(text="Bot is running and accepting connections", text_color="#2ECC71"))
            asyncio.create_task(background_scheduler(bot))
            await dp.start_polling(bot)
        except Exception as e: self.after(0, lambda: self.update_status("Critical Error", "red", "red"))
        finally: await bot.session.close()

    def stop_bot(self): self.destroy(); sys.exit(0)

if __name__ == "__main__":
    app = BotApp(); app.mainloop()
