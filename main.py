import telebot
from telebot import types

TOKEN = 7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📊 MSE Radar")
    btn2 = types.KeyboardButton("🧠 IntelBox")
    btn3 = types.KeyboardButton("🎓 Education")
    btn4 = types.KeyboardButton("⚙️ Help / Tutorial")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     "🤖 Welcome to *Golden Line AI Bot* 🚀\nChoose your action below:",
                     parse_mode='Markdown',
                     reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "📊 MSE Radar":
        bot.send_message(message.chat.id, "🔍 Radar aktif... Menganalisa pasaran sekarang 📈")
    elif message.text == "🧠 IntelBox":
        bot.send_message(message.chat.id, "📦 Membuka Golden Line IntelBox...")
    elif message.text == "🎓 Education":
        bot.send_message(message.chat.id, "🎯 Akses modul pembelajaran Golden Line Setup 🎓")
    elif message.text == "⚙️ Help / Tutorial":
        bot.send_message(message.chat.id, "📘 Arahan: Tekan /start semula untuk reset menu.")
    else:
        bot.send_message(message.chat.id, "❌ Arahan tidak dikenali. Tekan /start semula.")

bot.polling(non_stop=True)
