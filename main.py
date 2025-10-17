from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os

# === TOKEN BOT TELEGRAM ===
TOKEN = os.getenv("TELEGRAM_TOKEN", "7935629909:AAGOW4HQ5FoCm_kq1QCVuyk1rDbcEXbtSWd")

# === MENU UTAMA ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Golden Line Pro", callback_data="goldenline_menu"),
         InlineKeyboardButton("🧭 Mapping Pro", callback_data="mapping_pro")],
        [InlineKeyboardButton("🎓 Education", callback_data="education"),
         InlineKeyboardButton("📘 Subscription", callback_data="subscription")],
        [InlineKeyboardButton("📚 Tutorial", callback_data="tutorial"),
         InlineKeyboardButton("🌐 Language", callback_data="language")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "🤖 *Welcome to Golden Line AI Pro*\n\n"
        "Selamat datang ke platform rasmi Golden Line Team.\n\n"
        "📊 Signal Real-Time\n"
        "🧭 Mapping Analisis Harian\n"
        "🎓 Modul Pembelajaran & Tutorial Lengkap\n\n"
        "Sila pilih menu di bawah untuk mula menggunakan sistem ini 🔽"
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# === CALLBACK HANDLER ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # === MENU GOLDEN LINE PRO ===
    if data == "goldenline_menu":
        submenu = [
            [InlineKeyboardButton("🪙 XAU/USD", callback_data="xauusd")],
            [InlineKeyboardButton("🛢️ WTI", callback_data="wti")],
            [InlineKeyboardButton("🏠 Back", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text="📊 *Golden Line Pro*\n\nPilih pasangan (pair) untuk analisis signal real-time di bawah 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(submenu)
        )

    # === SUBMENU XAU/USD ===
    elif data == "xauusd":
        tfmenu = [
            [InlineKeyboardButton("🕒 M15", callback_data="xauusd_m15"),
             InlineKeyboardButton("🕕 M30", callback_data="xauusd_m30"),
             InlineKeyboardButton("🕐 H1", callback_data="xauusd_h1")],
            [InlineKeyboardButton("🏠 Back", callback_data="goldenline_menu")]
        ]
        await query.edit_message_text(
            text="🪙 *Selected Pair:* XAU/USD\n\n"
                 "Sila pilih timeframe untuk analisis signal:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(tfmenu)
        )

    # === SUBMENU WTI ===
    elif data == "wti":
        tfmenu = [
            [InlineKeyboardButton("🕒 M15", callback_data="wti_m15"),
             InlineKeyboardButton("🕕 M30", callback_data="wti_m30"),
             InlineKeyboardButton("🕐 H1", callback_data="wti_h1")],
            [InlineKeyboardButton("🏠 Back", callback_data="goldenline_menu")]
        ]
        await query.edit_message_text(
            text="🛢️ *Selected Pair:* WTI\n\n"
                 "Sila pilih timeframe untuk analisis signal:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(tfmenu)
        )

    # === TIMEFRAME HANDLER ===
    elif data in ["xauusd_m15", "xauusd_m30", "xauusd_h1",
                  "wti_m15", "wti_m30", "wti_h1"]:

        pair = "XAU/USD" if "xauusd" in data else "WTI"
        tf = data.split("_")[1].upper()

        await query.edit_message_text(
            text=f"✅ *Signal Active Mode ON*\n\n"
                 f"📍 Pair: {pair}\n🕒 Timeframe: {tf}\n\n"
                 f"Menunggu signal real-time dari sistem Golden Line AI Pro...\n\n"
                 f"Tekan 'Stop Signal' untuk hentikan notifikasi semasa.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Stop Signal", callback_data="stop_signal")]
            ])
        )

    # === STOP SIGNAL ===
    elif data == "stop_signal":
        await query.edit_message_text(
            text="🛑 *Signal Mode Deactivated*\n\n"
                 "Anda telah hentikan signal real-time dari Golden Line AI Pro.",
            parse_mode="Markdown"
        )

    # === MAPPING PRO ===
    elif data == "mapping_pro":
        await query.edit_message_text(
            text="🧭 *Mapping Pro*\n\nFungsi analisis struktur pasaran akan datang 🔍",
            parse_mode="Markdown"
        )

    # === EDUCATION ===
    elif data == "education":
        await query.edit_message_text(
            text="🎓 *Education*\n\nAkses modul pembelajaran lengkap Golden Line AI Pro 📘",
            parse_mode="Markdown"
        )

    # === SUBSCRIPTION ===
    elif data == "subscription":
        await query.edit_message_text(
            text="📘 *Subscription*\n\nMaklumat tentang pelan langganan & pakej sokongan pelanggan 💎",
            parse_mode="Markdown"
        )

    # === TUTORIAL ===
    elif data == "tutorial":
        await query.edit_message_text(
            text="📚 *Tutorial*\n\nLangkah-langkah & panduan penggunaan sistem Golden Line AI Pro 🧠",
            parse_mode="Markdown"
        )

    # === LANGUAGE ===
    elif data == "language":
        await query.edit_message_text(
            text="🌐 *Language*\n\nPilih bahasa yang anda ingin gunakan untuk sistem ini 🌏",
            parse_mode="Markdown"
        )

    # === BACK KE MENU UTAMA ===
    elif data == "back_main":
        await start(update, context)


# === RUN APP ===
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))
app.run_polling()
