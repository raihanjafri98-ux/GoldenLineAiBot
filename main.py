from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os

TOKEN = os.getenv("TELEGRAM_TOKEN", "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ")

# === START MENU ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Golden Line Pro", callback_data="goldenline_menu")],
        [InlineKeyboardButton("🗺️ Mapping Pro", callback_data="mapping_pro")],
        [InlineKeyboardButton("🎓 Education", callback_data="education")],
        [InlineKeyboardButton("💼 Subscription", callback_data="subscription")],
        [InlineKeyboardButton("📘 Tutorial", callback_data="tutorial")],
        [InlineKeyboardButton("🌐 Language", callback_data="language")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 *Welcome to ChiefHanOfficial AI Bot*\n\n"
        "Sila pilih menu di bawah untuk mula 🚀",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# === CALLBACK HANDLER ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # === Golden Line Pro ===
    if data == "goldenline_menu":
        submenu = [
            [InlineKeyboardButton("📡 GoldenLine Signal AI Pro", callback_data="signal_pro")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text="📊 *Golden Line Pro*\n\nPilih fungsi di bawah:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(submenu)
        )

    # === Mapping Pro ===
    elif data == "mapping_pro":
        await query.edit_message_text(
            text="🗺️ *Mapping Pro*\n\nFungsi analisa struktur pasaran akan datang 🚧",
            parse_mode="Markdown"
        )

    # === Education ===
    elif data == "education":
        await query.edit_message_text(
            text="🎓 *Education Center*\n\nModul latihan & eBook akan dimuat naik tidak lama lagi 📘",
            parse_mode="Markdown"
        )

    # === Subscription ===
    elif data == "subscription":
        await query.edit_message_text(
            text="💼 *Subscription Status*\n\nAkaun anda: *ACTIVE (Free Beta)* 🚀\n\n"
                 "Hubungi admin untuk naik taraf akaun premium 🔑",
            parse_mode="Markdown"
        )

    # === Tutorial ===
    elif data == "tutorial":
        await query.edit_message_text(
            text="📘 *Tutorial Guide*\n\n1️⃣ Cara guna GoldenLine Pro\n2️⃣ Setup SOP Entry\n3️⃣ Mapping & Market Phase\n\n"
                 "📺 Video guide & modul akan dikemaskini kemudian.",
            parse_mode="Markdown"
        )

    # === Language ===
    elif data == "language":
        lang_menu = [
            [InlineKeyboardButton("🇲🇾 Bahasa Melayu", callback_data="lang_ms")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text="🌐 *Pilih Bahasa / Choose Language:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(lang_menu)
        )

    # === Back to Main Menu ===
    elif data == "back_main":
        await start(update, context)

# === MAIN APP ===
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))

if __name__ == "__main__":
    app.run_polling()
