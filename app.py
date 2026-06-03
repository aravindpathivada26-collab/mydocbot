from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "mydocbot123"
ACCESS_TOKEN = "EAAhxlj8zrn0BRrKu8YQZAuueCyqQ9AD26GZC31cRk7uspRjRRtTkBShFbEE7d5RYiGHou3kjYHR7o6Ujw2x4uZBZA6iJzkLD6FughrTuthEBVkN4CVK3ZAPu7b6RwNvHluR3RIrl5pbv7bsg3QdGQdy4gZCfKQ6VD1toUUgdNWoP4CNLhfpMgpptnXr0ApKsQZAB2p7kOnKzZCeLmLoMnBjZB0AwqJUNGDgdZAUwFRb2ONAqBDpxBOZAC7SmuAMJfQovVw1eSs7PPGH3W3mz7ZBBZAZADxlyfG"
PHONE_NUMBER_ID = "1191571390698057"

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
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        phone = msg["from"]
        text = msg["text"]["body"]
        handle_message(phone, text)
    except:
        pass
    return "OK"

if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000)
