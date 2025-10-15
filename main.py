from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# === BOT TOKEN ===
TOKEN = "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ"

# === Logging setup (optional) ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# === /start command ===
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

# === Callback button logic ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # === GoldenLinePro main menu ===
    if query.data == "goldenlinepro":
        commodities_menu = [
            [InlineKeyboardButton("XAU/USD 🪙", callback_data="xauusd"),
             InlineKeyboardButton("WTI Crude Oil 🛢️", callback_data="wti")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        await query.edit_message_text(
            "🏭 *Golden Line Pro Market Radar*\n\nSelect your trading pair below:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(commodities_menu)
        )

    # === Pair selection ===
    elif query.data in ["xauusd", "wti"]:
        pair_name = "XAU/USD 🪙" if query.data == "xauusd" else "WTI Crude Oil 🛢️"
        tf_menu = [
            [InlineKeyboardButton("M15", callback_data=f"{query.data}_m15"),
             InlineKeyboardButton("M30", callback_data=f"{query.data}_m30"),
             InlineKeyboardButton("H1", callback_data=f"{query.data}_h1")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        await query.edit_message_text(
            f"📈 *Selected Pair:* {pair_name}\nSelect a timeframe for signal analysis:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(tf_menu)
        )

    # === Timeframe selection ===
    elif any(tf in query.data for tf in ["_m15", "_m30", "_h1"]):
        base_pair = query.data.split("_")[0]
        tf = query.data.split("_")[1].upper()

        pair_name = "XAU/USD 🪙" if base_pair == "xauusd" else "WTI Crude Oil 🛢️"

        # === Header Image (optional banner) ===
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo="https://i.ibb.co/sKJb5Qv/goldenlinepro-header.jpg",  # tukar ke banner rasmi ChiefHanOfficial
            caption=f"📊 *Golden Line Pro Signal Report*\n{pair_name} – Timeframe {tf}",
            parse_mode="Markdown"
        )

        # === Example signal report ===
        signal_report = (
            f"💹 *Market Analysis by GoldenLine AI:*\n"
            f"GoldenLine AI detects a *SELL* signal for {pair_name}.\n\n"
            f"📉 *Trend:* Bearish | *Method:* Golden Line Setup (LWMA 5/10)\n\n"
            f"📍 *Support Levels:*\nS1: 2367.20\nS2: 2364.50\n\n"
            f"📈 *Resistance Levels:*\nR1: 2371.80\nR2: 2374.10\n\n"
            f"🎯 *Target Points:*\nTP1: 2365.50\nTP2: 2363.40\nTP3: 2361.80\n\n"
            f"💡 *Entry Tips:*\nEnter near 2368.50 and exit TP1–TP3 using BE strategy.\n"
            f"Set SL below Golden Line structure confirmation.\n\n"
            f"⚙️ *Golden Line Engine:* Real-time trend & volume precision.\n\n"
            f"⚠️ *Disclaimer:* This analysis is for educational purposes only.\n"
            f"Trade responsibly using SOP Golden Line Setup."
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=signal_report, parse_mode="Markdown")

    # === Other buttons ===
    elif query.data == "intelbox":
        await query.edit_message_text("🧠 Opening IntelBox... analyzing setup confirmation logic 🔍")

    elif query.data == "education":
        await query.edit_message_text("🎓 Accessing Golden Line Setup learning module 💡")

    elif query.data == "subscription":
        await query.edit_message_text("💼 Subscription Status: *Active (Free Beta)* 🚀", parse_mode="Markdown")

    elif query.data == "language":
        await query.edit_message_text("🌐 Language selection: English / Bahasa Melayu 🇲🇾")

    elif query.data == "tutorial":
        await query.edit_message_text("📚 Tutorial: Use /start anytime to restart the main menu 📖")

    elif query.data == "help":
        await query.edit_message_text("🆘 Need assistance? Contact @ChiefHanOfficialSupport")

    elif query.data == "settings":
        await query.edit_message_text("⚙️ Settings will be available soon. Stay tuned 🔧")

    elif query.data == "home":
        await start(update, context)

# === Run the bot ===
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))
app.run_polling()
