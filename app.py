from flask import Flask, request
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mydocbot123")

@app.route("/")
def home():
    return "Bot is running", 200

def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text}
            }
    requests.post(url, headers=headers, json=data)

# Track which service each user selected
user_state = {}

def handle_message(phone, text):
    text = text.strip().upper()
    if text == "HI":
        send_message(phone, "Welcome to MyDocBot!\nReply with:\n1. GST\n2. ITR\n3. TDS")
    elif text == "GST":
        send_message(phone, "Enter financial year (e.g. 2023-24)")
    elif text == "ITR":
        send_message(phone, "Enter financial year (e.g. 2023-24)")
    elif text == "TDS":
        send_message(phone, "Enter financial year (e.g. 2023-24)")
    else:
        send_message(phone, "Please type HI to start")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Invalid token", 403

    data = request.json
    print("Incoming payload:", data)
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        phone = msg["from"]
        text = msg["text"]["body"]
        print(f"Message from {phone}: {text}") 
        handle_message(phone, text)
    except Exception as e:
        print("Error:", e)
    return "OK"

if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000)
