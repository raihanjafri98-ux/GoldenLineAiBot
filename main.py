from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 GoldenLinePro", callback_data="goldenlinepro"),
         InlineKeyboardButton("🧠 IntelBox", callback_data="intelbox")],
        [InlineKeyboardButton("🎓 Education", callback_data="education"),
         InlineKeyboardButton("📬 Subscription", callback_data="subscription")],
        [InlineKeyboardButton("🌐 Language", callback_data="language"),
         InlineKeyboardButton("📚 Tutorial", callback_data="tutorial")],
        [InlineKeyboardButton("🆘 Help", callback_data="help"),
         InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        "🤖 Welcome to *Golden Line Pro* – Powered by ChiefHanOfficial 🚀\n\n"
        "Experience the precision of Golden Line Setup enhanced with smart AI analysis 🔥\n"
        "Stay synced with market flow, volume traps, and trend direction in real-time ⚡\n\n"
        "✨ *What You’ll Get:*\n"
        "• 📊 *Golden Line Pro Radar* – Advanced market structure & signal detection\n"
        "• 🧠 *IntelBox* – AI-powered insights on setups & confirmation logic\n"
        "• 🎓 *Education* – Learn the full Golden Line Setup from A–Z\n"
        "• 🆘 *Support & Tutorial* – Access help anytime directly from ChiefHanOfficial\n\n"
        "Ready to master the market with confidence?\n👉 Choose your action below:"
    )

    await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=reply_markup)

# Callback button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "goldenlinepro":
        await query.edit_message_text("📊 Radar aktif... Menganalisa pasaran semasa 📈")
    elif data == "intelbox":
        await query.edit_message_text("🧠 Membuka Golden Line IntelBox... Menganalisa setup 🔍")
    elif data == "education":
        await query.edit_message_text("🎓 Akses modul pembelajaran Golden Line Setup 💡")
    elif data == "subscription":
        await query.edit_message_text("💼 Status akaun: *ACTIVE (Free Beta)* 🚀", parse_mode="Markdown")
    elif data == "language":
        await query.edit_message_text("🌐 Pilih bahasa: English / Bahasa Melayu")
    elif data == "tutorial":
        await query.edit_message_text("📚 Tutorial penggunaan: Tekan /help untuk panduan penuh 📖")
    elif data == "help":
        await query.edit_message_text("🆘 Arahan: Tekan /start semula untuk reset menu atau hubungi @ChiefHanOfficialSupport")
    elif data == "settings":
        await query.edit_message_text("⚙️ Settings belum aktif dalam versi ini. Stay tuned 🔧")

# Main app
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
from telegram.ext import CallbackQueryHandler
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
