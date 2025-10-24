from flask import Flask, jsonify
import os, requests, subprocess
from datetime import datetime

app = Flask(__name__)

# Дані беремо з Environment Variables у Render
TARGET_IP = os.environ.get("TARGET_IP", "195.66.140.148")  # ваш роутер
BOT_TOKEN = os.environ.get("BOT_TOKEN")                   # токен від BotFather
CHAT_ID = os.environ.get("CHAT_ID")                       # ID чату/групи

def ping(host):
    """Пінгуємо IP"""
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", host])
        return True
    except:
        return False

def notify(msg):
    """Надсилаємо повідомлення в Telegram"""
    if BOT_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        except Exception as e:
            print("Telegram error:", e)

@app.route("/")
def index():
    return "✅ Power monitor is running!"

@app.route("/check")
def check():
    status = "UP" if ping(TARGET_IP) else "DOWN"
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{ts} UTC | {TARGET_IP} is {status}"
    notify(message)
    return jsonify({"status": status, "time": ts})
