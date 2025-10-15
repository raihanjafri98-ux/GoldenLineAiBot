from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# === BOT TOKEN ===
TOKEN = "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ"

# === Logging (optional) ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# === /start Command ===
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

    welcome_message = (
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
    await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=reply_markup)

# === Callback Handler (semua button action) ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # === GoldenLinePro Section ===
    if query.data == "goldenlinepro":
        commodities_menu = [
            [InlineKeyboardButton("XAU/USD", callback_data="xauusd"),
             InlineKeyboardButton("XAG/USD", callback_data="xagusd")],
            [InlineKeyboardButton("WTI Crude Oil", callback_data="wti"),
             InlineKeyboardButton("Brent Crude Oil", callback_data="brent")],
            [InlineKeyboardButton("Natural Gas (NG)", callback_data="ng"),
             InlineKeyboardButton("FCPO", callback_data="fcpo")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        await query.edit_message_text("🏭 *Commodities Market*\nSelect a pair (Page 1 of 1):",
                                      parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(commodities_menu))

    elif query.data in ["xauusd", "xagusd", "wti", "brent", "ng", "fcpo"]:
        pair_name = {
            "xauusd": "XAU/USD",
            "xagusd": "XAG/USD",
            "wti": "WTI Crude Oil",
            "brent": "Brent Crude Oil",
            "ng": "Natural Gas (NG)",
            "fcpo": "FCPO"
        }[query.data]

        tf_menu = [
            [InlineKeyboardButton("M15", callback_data=f"{query.data}_m15"),
             InlineKeyboardButton("H1", callback_data=f"{query.data}_h1")],
            [InlineKeyboardButton("H4", callback_data=f"{query.data}_h4"),
             InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        await query.edit_message_text(f"📈 *Selected Pair:* {pair_name}\nSelect a timeframe:",
                                      parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(tf_menu))

    elif any(tf in query.data for tf in ["_m15", "_h1", "_h4"]):
        base_pair = query.data.split("_")[0]
        tf = query.data.split("_")[1].upper()

        pair_name = {
            "xauusd": "XAU/USD",
            "xagusd": "XAG/USD",
            "wti": "WTI Crude Oil",
            "brent": "Brent Crude Oil",
            "ng": "Natural Gas (NG)",
            "fcpo": "FCPO"
        }[base_pair]

        # === Banner Image (optional) ===
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo="https://i.ibb.co/sKJb5Qv/goldenlinepro-header.jpg",
            caption=f"📊 *Golden Line Pro Signal Report*\n{pair_name} – Timeframe {tf}",
            parse_mode="Markdown"
        )

        # === Signal Report ===
        report = (
            f"💹 *Market Analysis by GoldenLine AI:*\n"
            f"GoldenLine AI detects a *SELL* signal for {pair_name}.\n\n"
            f"📉 *Trend:* Bearish | *Method:* Golden Line Setup (LWMA 5/10)\n\n"
            f"📍 *Support Levels:*\nS1: 2367.20\nS2: 2364.50\n\n"
            f"📈 *Resistance Levels:*\nR1: 2371.80\nR2: 2374.10\n\n"
            f"🎯 *Target Points:*\nTP1: 2365.50\nTP2: 2363.40\nTP3: 2361.80\n\n"
            f"💡 *Entry Tips:*\nEnter near 2368.50 and exit TP1–TP3 using BE strategy.\n"
            f"Set SL below Golden Line structure confirmation.\n\n"
            f"⚠️ *Disclaimer:* For educational purposes only.\n"
            f"Trade responsibly using SOP Golden Line Setup."
        )

        await context.bot.send_message(chat_id=update.effective_chat.id, text=report, parse_mode="Markdown")

    elif query.data == "home":
        await start(update, context)

# === Main Run ===
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))
app.run_polling()
