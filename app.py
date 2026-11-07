import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

GRAPH_API_VERSION = "v27.0"


@app.route("/", methods=["GET"])
def home():
    return "Horizon WhatsApp Webhook is running", 200
@app.route("/connect", methods=["GET"])
def connect_whatsapp():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Horizon WhatsApp Connection</title>
    </head>
    <body>
        <h1>Horizon WhatsApp</h1>
        <p>صفحة ربط رقم واتساب الفندق بمنصة Meta.</p>
        <p>Embedded Signup configuration is ready.</p>
    </body>
    </html>
    """, 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully", flush=True)
        return challenge, 200

    return "Verification failed", 403


def send_whatsapp_message(to_number, message_text):
    url = (
        f"https://graph.facebook.com/"
        f"{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message_text,
        },
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=15,
    )

    print(
        "WhatsApp send response:",
        response.status_code,
        response.text,
        flush=True,
    )

    return response


@app.route("/webhook", methods=["POST"])
def receive_webhook():
    data = request.get_json(silent=True)

    print("WhatsApp event received:", flush=True)
    print(data, flush=True)

    if not data:
        return jsonify({"status": "invalid json"}), 400

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})

                for message in value.get("messages", []):
                    sender = message.get("from")
                    message_type = message.get("type")

                    if message_type != "text":
                        continue

                    incoming_text = (
                        message.get("text", {}).get("body", "")
                    )

                    print(
                        f"Message from {sender}: {incoming_text}",
                        flush=True,
                    )

                    reply_text = (
                        "مرحباً بكم في فندق هورايزون عدن السياحي 🌷\n\n"
                        "تم استلام رسالتكم بنجاح.\n"
                        "كيف يمكننا مساعدتكم؟\n\n"
                        "1️⃣ الحجز والأسعار\n"
                        "2️⃣ الغرف المتاحة\n"
                        "3️⃣ موقع الفندق\n"
                        "4️⃣ خدمات الفندق\n"
                        "5️⃣ التحدث مع موظف"
                    )

                    if sender:
                        send_whatsapp_message(
                            sender,
                            reply_text,
                        )

    except Exception as error:
        print(
            "Webhook processing error:",
            str(error),
            flush=True,
        )

    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
