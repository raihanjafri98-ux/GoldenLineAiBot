from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_keyboard = [
        ["📊 GoldenLinePro", "🧠 IntelBox"],
        ["🎓 Education", "💼 Subscription"],
        ["🌐 Language", "📚 Tutorial"],
        ["🆘 Help", "⚙️ Settings"]
    ]
    reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

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

# Response handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "goldenlinepro" in text:
        await update.message.reply_text("📊 Radar aktif... Menganalisa pasaran semasa 📈")
    elif "intelbox" in text:
        await update.message.reply_text("🧠 Membuka Golden Line IntelBox... Menganalisa setup 🔍")
    elif "education" in text:
        await update.message.reply_text("🎓 Akses modul pembelajaran Golden Line Setup 💡")
    elif "subscription" in text:
        await update.message.reply_text("💼 Status akaun: *ACTIVE (Free Beta)* 🚀", parse_mode="Markdown")
    elif "language" in text:
        await update.message.reply_text("🌐 Pilih bahasa: English / Bahasa Melayu")
    elif "tutorial" in text:
        await update.message.reply_text("📚 Tutorial penggunaan: Tekan /help untuk panduan penuh 📖")
    elif "help" in text:
        await update.message.reply_text("🆘 Arahan: Tekan /start semula untuk reset menu atau hubungi @ChiefHanOfficialSupport")
    elif "settings" in text:
        await update.message.reply_text("⚙️ Settings belum aktif dalam versi ini. Stay tuned 🔧")
    else:
        await update.message.reply_text("❌ Arahan tidak dikenali. Tekan /start semula untuk reset menu.")

# Main app
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
