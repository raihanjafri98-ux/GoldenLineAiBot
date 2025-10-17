from flask import Flask, request
import requests, json, os

TOKEN = os.getenv("TELEGRAM_TOKEN", "7935629099:AAGOW4HQ5FoCm_kQl0CYuyk1rDbcEXbtSWQ")
DATA_FILE = "active_users.json"

app = Flask(__name__)

def load_active_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    symbol = data.get("symbol")
    tf = data.get("tf")
    signal = data.get("signal")
    price = data.get("price")

    users = load_active_users()
    for chat_id, user in users.items():
        if user["active"] and user["pair"] == symbol and user["tf"] == tf:
            message = f"""
📈 *Golden Line Signal Detected*
Pair: {symbol}
Timeframe: {tf}
Signal: *{signal}*
Price: `{price}`

🎯 TP1: +35 Pips  
🎯 TP2: +70 Pips  
🏁 TP3: Hold & BE
"""
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
