# 🚀 BotServer Configuration Guide

This guide explains how to get the necessary tokens for your bot.

## 1. Telegram Bot Token
To use this bot, you need a token from Telegram's official bot manager.

1.  Open Telegram and search for **[@BotFather](https://t.me/botfather)**.
2.  Send the command `/newbot`.
3.  Follow the instructions to name your bot.
4.  Copy the **API Token** provided (it looks like `123456:ABC-DEF...`).
5.  Paste this token when the `install.bat` asks for it.

---

## 2. Payment Token (Commercial Version Only)
If you want to accept payments for extra storage, you need a provider token.

1.  Go back to **[@BotFather](https://t.me/botfather)**.
2.  Send `/mybots` and select your bot.
3.  Go to **Bot Settings** -> **Payments**.
4.  Choose a provider (e.g., **LiqPay** for Ukraine).
5.  Follow the provider's link to connect your account.
6.  BotFather will give you a **Provider Token** (starts with `PAYMENT_` or `sandbox_`).
7.  Add this token to your `.env` file as `PAYMENT_TOKEN=your_token_here`.

---

## 3. Database Management
- **SQLite (Default):** No setup required. Everything is stored in `bot.db`.
- **MongoDB (Scalable):** If you are a developer, install MongoDB locally or use a cloud service (MongoDB Atlas). Update `.env` with `DATABASE_TYPE=mongodb` and `MONGO_URL=your_connection_string`.

---

## 🛠️ Need Help?
- **GitHub:** [@gleb226](https://github.com/gleb226)
- **Commands:** Use `/start` to begin and `/language` to change settings.
