from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os

# === TOKEN BOT TELEGRAM ===
TOKEN = os.getenv("TELEGRAM_TOKEN", "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ")

# === START / MENU UTAMA ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Golden Line Pro", callback_data="goldenline_menu"),
         InlineKeyboardButton("🧠 Mapping Pro", callback_data="mapping_pro")],
        [InlineKeyboardButton("📘 Education", callback_data="education"),
         InlineKeyboardButton("💼 Subscription", callback_data="subscription")],
        [InlineKeyboardButton("🎥 Tutorial", callback_data="tutorial"),
         InlineKeyboardButton("🌐 Language", callback_data="language")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "✨ *Welcome to Golden Line AI Pro* ✨\n\n"
        "Sistem analisis pintar direka khas untuk trader profesional.\n"
        "Gunakan menu di bawah untuk akses signal, mapping dan tutorial penuh.\n\n"
        "📊 Real-Time Signal Detection\n"
        "🧠 Smart Market Mapping\n"
        "📘 Education & Learning Hub\n"
        "💼 Subscription Center\n\n"
        "_Pilih menu di bawah untuk bermula._ 🔽"
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# === FUNGSI MAPPING PRO ===
def get_mapping_analysis(pair, timeframe):
    image_url = "https://i.imgur.com/0l3vKcl.png"  # Placeholder image sementara

    if pair == "XAU/USD":
        if timeframe == "M15":
            analysis = (
                "📈 Trend menaik di atas MA10 High & Low.\n"
                "Support aktif sekitar 2340.00 – 2345.00.\n"
                "Resistance utama 2358.50.\n"
                "Fokus: BUY on dip mengikut SOP Golden Line Setup."
            )
        elif timeframe == "H1":
            analysis = (
                "📊 Struktur H1 masih bullish dengan momentum kukuh.\n"
                "Potensi retracement ringan sebelum sambung kenaikan."
            )
        else:
            analysis = "⚖️ Struktur neutral – tunggu breakout seterusnya."
    else:
        analysis = (
            "🛢️ WTI dalam range 80.20 – 81.40.\n"
            "Pantau breakout zone untuk peluang seterusnya."
        )

    copyright_text = (
        "© 2025 Golden Line AI Pro Team\n"
        "📊 Smart Mapping Analysis Powered by Golden Line System"
    )

    return image_url, analysis, copyright_text

# === CALLBACK HANDLER ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "goldenline_menu":
        submenu = [
            [InlineKeyboardButton("🪙 XAU/USD", callback_data="xauusd")],
            [InlineKeyboardButton("🛢️ WTI", callback_data="wti")],
            [InlineKeyboardButton("🏠 Back", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text="📊 *Golden Line Pro*\n\n"
                 "Pilih pasangan (pair) untuk analisis signal real-time 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(submenu)
        )

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

    elif data == "stop_signal":
        await query.edit_message_text(
            text="🛑 *Signal Mode Deactivated*\n\n"
                 "Anda telah hentikan signal real-time dari Golden Line AI Pro.",
            parse_mode="Markdown"
        )

    elif data == "mapping_pro":
        submenu = [
            [InlineKeyboardButton("🪙 XAU/USD", callback_data="map_xauusd"),
             InlineKeyboardButton("🛢️ WTI", callback_data="map_wti")],
            [InlineKeyboardButton("🏠 Back", callback_data="back_main")]
        ]
        await query.edit_message_text(
            text="🧠 *Mapping Pro – Real-Time Market Mapping*\n\n"
                 "Pilih pair untuk dapatkan analisis real-time beserta peta trend.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(submenu)
        )

    elif data in ["map_xauusd", "map_wti"]:
        pair = "XAU/USD" if "xauusd" in data else "WTI"
        timeframe = "M15"
        image_url, analysis, copyright_text = get_mapping_analysis(pair, timeframe)

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image_url,
            caption=f"🧠 *{pair} Mapping ({timeframe})*\n\n{analysis}\n\n{copyright_text}",
            parse_mode="Markdown"
        )

    elif data == "education":
        await query.edit_message_text(
            text="📘 *Education*\n\nAkses modul pembelajaran Golden Line AI Pro 📗",
            parse_mode="Markdown"
        )

    elif data == "subscription":
        await query.edit_message_text(
            text="💼 *Subscription*\n\nMaklumat pelan langganan & sokongan pelanggan akan dikemaskini.",
            parse_mode="Markdown"
        )

    elif data == "tutorial":
        await query.edit_message_text(
            text="🎥 *Tutorial*\n\nPanduan video dan langkah penggunaan sistem Golden Line AI Pro.",
            parse_mode="Markdown"
        )

    elif data == "language":
        await query.edit_message_text(
            text="🌐 *Language*\n\nBahasa tambahan akan disokong dalam versi akan datang 🌏",
            parse_mode="Markdown"
        )

    elif data == "back_main":
        await start(update, context)

# === RUN APP ===
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))
app.run_polling()
