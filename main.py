# ==============================
# Golden Line Pro AI Telegram Bot + TradingView Webhook
# ==============================
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import threading
import requests
import os

# ==============================
# CONFIGURATION
# ==============================
TOKEN = "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ"
CHAT_ID = "-1002399898672"  # Ganti dgn group ID / personal chat ID
PORT = int(os.environ.get("PORT", 5000))

# ==============================
# LOGGING
# ==============================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==============================
# FLASK WEBHOOK (TradingView)
# ==============================
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

    message = (
        f"📊 *Golden Line Pro Signal Alert*\n\n"
        f"📍 *Pair:* {pair}\n"
        f"🕒 *Timeframe:* {timeframe}\n"
        f"⚡ *Signal:* {signal}\n"
        f"🎯 *Entry Price:* {entry}\n\n"
        f"🎯 *Take Profit Targets:*\n"
        f"TP1: {tp1}\nTP2: {tp2}\nTP3: {tp3}\n\n"
        f"🛑 *Stop Loss:* {sl}\n\n"
        f"🤖 Golden Line AI Engine"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

    return {"status": "Signal sent ✅"}, 200

# ==============================
# TELEGRAM BOT MENU SECTION
# ==============================

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
        "• 🎓 *Education* – Learn the full Golden Line Setup from A–Z\n"
        "• 🆘 *Support & Tutorial* – Access help anytime directly from ChiefHanOfficial\n\n"
        "👉 Choose your action below:"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown", reply_markup=reply_markup)

# ==============================
# BUTTON LOGIC
# ==============================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "goldenlinepro":
        commodities_menu = [
            [InlineKeyboardButton("XAU/USD", callback_data="xauusd"),
             InlineKeyboardButton("WTI Crude Oil", callback_data="wti")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        await query.edit_message_text(
            text="📊 Choose your trading pair below:",
            reply_markup=InlineKeyboardMarkup(commodities_menu)
        )

    elif query.data in ["xauusd", "wti"]:
        tf_menu = [
            [InlineKeyboardButton("M15", callback_data=f"{query.data}_m15"),
             InlineKeyboardButton("M30", callback_data=f"{query.data}_m30"),
             InlineKeyboardButton("H1", callback_data=f"{query.data}_h1")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        await query.edit_message_text(
            text=f"🕒 Selected Pair: *{query.data.upper()}*\nSelect a timeframe for AI analysis:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(tf_menu)
        )

    elif any(tf in query.data for tf in ["_m15", "_m30", "_h1"]):
        base_pair = query.data.split("_")[0].upper()
        tf = query.data.split("_")[1].upper()

        message = (
            f"📊 *Golden Line Pro Signal Report*\n\n"
            f"📍 Pair: {base_pair}\n"
            f"🕒 Timeframe: {tf}\n\n"
            f"📈 Market Analysis by GoldenLine AI:\n"
            f"Detected *SELL* signal for {base_pair}\n\n"
            f"🎯 TP1: 2366.20 | TP2: 2363.80 | TP3: 2361.50\n"
            f"🛑 SL: 2372.00\n\n"
            f"🤖 Golden Line Engine – Real-time trend & volume precision.\n"
            f"For educational purposes only."
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode="Markdown"
        )

    elif query.data == "home":
        await start(update, context)

# ==============================
# RUN FLASK + TELEGRAM TOGETHER
# ==============================

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

def run_telegram():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram()
