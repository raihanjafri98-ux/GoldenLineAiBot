from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json, os

TOKEN = os.getenv("TELEGRAM_TOKEN", "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ")
DATA_FILE = "active_users.json"

# === Save active users ===
def save_active_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_active_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# === START MENU ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💛 Golden Line Pro", callback_data="goldenline_menu")],
        [InlineKeyboardButton("🧠 Mapping Pro", callback_data="mapping_pro")],
        [InlineKeyboardButton("🎓 Education", callback_data="education")],
        [InlineKeyboardButton("📘 Subscription", callback_data="subscription")],
        [InlineKeyboardButton("📚 Tutorial", callback_data="tutorial")],
        [InlineKeyboardButton("🌐 Language", callback_data="language")]
    ]
    await update.message.reply_text(
        "🤖 *Welcome to ChiefHanOfficial AI Bot*\n\nPilih menu di bawah untuk mula 📊",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === CALLBACK HANDLER ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    users = load_active_users()

    # --- Golden Line Pro Menu ---
    if data == "goldenline_menu":
        submenu = [
            [InlineKeyboardButton("🪙 XAU/USD", callback_data="pair_xauusd")],
            [InlineKeyboardButton("🛢️ WTI/USD", callback_data="pair_wtiusd")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
        ]
        await query.edit_message_text(
            "🟡 *GoldenLine Signal AI Pro*\nPilih pair untuk mula analisis 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(submenu)
        )

    # --- Pair Menu ---
    elif data.startswith("pair_"):
        pair = data.split("_")[1].upper()
        submenu = [
            [InlineKeyboardButton("⏱ M15", callback_data=f"{pair}_M15")],
            [InlineKeyboardButton("⏱ M30", callback_data=f"{pair}_M30")],
            [InlineKeyboardButton("⏱ H1", callback_data=f"{pair}_H1")],
            [InlineKeyboardButton("⬅️ Back", callback_data="goldenline_menu")]
        ]
        await query.edit_message_text(
            f"📊 *Selected Pair:* {pair}\n\nPilih timeframe untuk signal analisis 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(submenu)
        )

    # --- Timeframe selected ---
    elif "_" in data:
        pair, tf = data.split("_")
        chat_id = str(query.message.chat_id)
        users[chat_id] = {"pair": pair, "tf": tf, "active": True}
        save_active_users(users)

        await query.edit_message_text(
            f"✅ *Signal Active Mode ON*\nPair: {pair}\nTimeframe: {tf}\n\nMenunggu signal real-time...",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Stop Signal", callback_data="stop_signal")],
                [InlineKeyboardButton("🏠 Home", callback_data="back_main")]
            ])
        )

    elif data == "stop_signal":
        chat_id = str(query.message.chat_id)
        users.pop(chat_id, None)
        save_active_users(users)
        await query.edit_message_text(
            "🛑 Signal dihentikan.\nKembali ke menu utama untuk sambung semula.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="back_main")]])
        )

    elif data == "back_main":
        await start(update, context)

# === RUN BOT ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.run_polling()
