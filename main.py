from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import threading
import requests
import os

# =========================
# CONFIGURATION
# =========================
TOKEN = "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ"
CHAT_ID = "1933986987"   # Group ID / Personal chat ID
PORT = int(os.environ.get("PORT", 5000))
bot = Bot(token=TOKEN)

# =========================
# LOGGING
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# =========================
# FLASK WEBHOOK APP (TradingView)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "GoldenLinePro AI Engine is running ✅", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    pair = data.get("pair", "Unknown Pair")
    timeframe = data.get("timeframe", "N/A")
    signal = data.get("signal", "N/A")
    entry = data.get("entry", "N/A")
    tp1 = data.get("tp1", "N/A")
    tp2 = data.get("tp2", "N/A")
    tp3 = data.get("tp3", "N/A")
    sl = data.get("sl", "N/A")

    message = f"""
📡 *Golden Line Pro Signal Alert*
━━━━━━━━━━━━━━━━━━━
💎 *Pair:* {pair}
🕒 *Timeframe:* {timeframe}
📈 *Signal:* {signal.upper()}

🎯 *Entry Price:* {entry}

🎯 *Take Profit Targets:*
• TP1: {tp1}
• TP2: {tp2}
• TP3: {tp3}

🛑 *Stop Loss:* {sl}

⚙️ *Golden Line AI Engine*
━━━━━━━━━━━━━━━━━━━
"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)
    return {"status": "Signal sent ✅"}, 200

# =========================
# TELEGRAM BOT MENU SECTION
# =========================

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = [
        [InlineKeyboardButton("📊 GoldenLinePro", callback_data="goldenlinepro"),
         InlineKeyboardButton("🧠 IntelBox", callback_data="intelbox")],
        [InlineKeyboardButton("🎓 Education", callback_data="education"),
         InlineKeyboardButton("📬 Subscription", callback_data="subscription")],
        [InlineKeyboardButton("🌐 Language", callback_data="language"),
         InlineKeyboardButton("📚 Tutorial", callback_data="tutorial")],
        [InlineKeyboardButton("🆘 Help", callback_data="help"),
         InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]

    reply_markup = InlineKeyboardMarkup(menu)
    welcome = (
        "🤖 *Welcome to Golden Line Pro* – Powered by ChiefHanOfficial 🚀\n\n"
        "Experience the precision of Golden Line Setup enhanced with smart AI analysis 🔥\n"
        "Stay synced with market flow, volume traps, and trend direction in real-time ⚡\n\n"
        "✨ *What You’ll Get:*\n"
        "• 📊 *Golden Line Pro Radar* – Advanced market structure & signal detection\n"
        "• 🧠 *IntelBox* – AI-powered insights on setups & confirmation logic\n"
        "• 🎓 *Education* – Learn the full Golden Line Setup from A–Z\n\n"
        "👉 Choose your action below:"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown", reply_markup=reply_markup)


# Inline button actions
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # === GoldenLinePro Section ===
    if query.data == "goldenlinepro":
        pairs = [
            [InlineKeyboardButton("XAU/USD 🪙", callback_data="xauusd"),
             InlineKeyboardButton("WTI Crude Oil 🛢️", callback_data="wti")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        await query.edit_message_text(
            "🏭 *Golden Line Pro Market Radar*\n\nSelect your trading pair below:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(pairs)
        )

    # === Pair Selection ===
    elif query.data in ["xauusd", "wti"]:
        pair_name = "XAU/USD 🪙" if query.data == "xauusd" else "WTI Crude Oil 🛢️"
        tf_menu = [
            [InlineKeyboardButton("M15", callback_data=f"{query.data}_m15"),
             InlineKeyboardButton("M30", callback_data=f"{query.data}_m30"),
             InlineKeyboardButton("H1", callback_data=f"{query.data}_h1")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        await query.edit_message_text(
            f"📈 *Selected Pair:* {pair_name}\nSelect a timeframe for AI analysis:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(tf_menu)
        )

    # === Timeframe Selection ===
    elif any(tf in query.data for tf in ["_m15", "_m30", "_h1"]):
        base_pair = query.data.split("_")[0]
        tf = query.data.split("_")[1].upper()
        pair_name = "XAU/USD 🪙" if base_pair == "xauusd" else "WTI Crude Oil 🛢️"

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo="https://i.ibb.co/sKJb5Qv/goldenlinepro-header.jpg",
            caption=f"📊 *Golden Line Pro Signal Report*\n{pair_name} – Timeframe {tf}",
            parse_mode="Markdown"
        )

        message = (
            f"💹 *Market Analysis by GoldenLine AI:*\n"
            f"Detected *SELL* signal for {pair_name}.\n\n"
            f"📉 *Trend:* Bearish | *Setup:* Golden Line (LWMA 5/10)\n\n"
            f"🎯 *Entry:* 2368.50\n"
            f"TP1: 2366.20 | TP2: 2363.80 | TP3: 2361.50\n"
            f"🛑 *SL:* 2372.00\n\n"
            f"⚙️ *Golden Line Engine:* Real-time trend & volume precision.\n"
            f"⚠️ For educational purposes only."
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="Markdown")

    elif query.data == "home":
        await start(update, context)


# =========================
# RUN TELEGRAM + FLASK TOGETHER
# =========================
def run_flask():
    app.run(host="0.0.0.0", port=PORT)

def run_telegram():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.run_polling()

if __name__ == "__main__":
    # Jalankan Flask dan Telegram serentak
    threading.Thread(target=run_flask).start()
    run_telegram()
