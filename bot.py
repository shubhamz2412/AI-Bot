from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 1. Yahan apni Keys dalo
GEMINI_API_KEY = "" #add your google api key
TELEGRAM_BOT_TOKEN = "" #past your telegram bot token

# 2. Gemini Client & Chat Setup
client = genai.Client(api_key=GEMINI_API_KEY)
chat = client.chats.create(model="gemini-3.6-flash")

def get_reply(user_input):
    user_lower = user_input.strip().lower()
    words = user_lower.split()

    # Exact word match for greetings
    if any(w in ["hi", "hello", "hey"] for w in words):
        return "hey man"

    elif user_lower in ["kese ho", "kaise ho"]:
        return "me thik hu ap bato"

    elif user_lower in ["me bhi ek kam tha tumse", "ek kam tha"]:
        return "me apke liye hi hu bataoo"

    elif user_lower in ["what is your name", "tumhara name kya hai"]:
        return "ap jo rakh do mere malik"


    elif any(keyword in user_lower for keyword in
             ["kisne banaya", "who made", "creator", "banane wale", "who built"]):
        return f"Shubham Sir ne😁"


    elif any(keyword in user_lower for keyword in
             ["shubham", "builder", "creator", "who built", "who made", "banaya", "banane wale"]):
        return f"Arre! 😎 Shubham nahi, Shubham Sir boliye! 😂 Ye wahi legendary insaan hain jinhone mujhe design kiya hai, isi wajah se aaj aap mujhse baat kar paa rahe ho. 🤖❤️ Simple words mein: Main unki creation hoon, aur woh mere creator hain. 😌🔥"

    elif user_lower == "byy":
        return "byy too, jaldi aana😊"

    else:
        try:
            # Primary model request
            response = chat.send_message(user_input)
            return response.text
        except Exception as e:
            # Agar 503 traffic busy error aaye toh backup try karega
            if "503" in str(e):
                try:
                    fallback_chat = client.chats.create(model="gemini-2.5-flash")
                    return fallback_chat.send_message(user_input).text
                except Exception:
                    return "Google server par abhi traffic jyada hai, 5 second baad dobara type karo."
            return f"Kuch gadbad ho gayi: {e}"

# Telegram Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! Main aapka AI bot hu. Kuch bhi pucho!")

# Telegram Message Handler
async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    bot_reply = get_reply(user_msg)
    await update.message.reply_text(bot_reply)

if __name__ == '__main__':
    # Telegram Bot initialize
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))

    print("Bot live hai! Apne phone me Telegram open karke message bhejo...")
    app.run_polling()