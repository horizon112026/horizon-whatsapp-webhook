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
    @app.route("/privacy", methods=["GET"])
def privacy_policy():
    return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سياسة الخصوصية - Horizon Aden Hotel</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 850px; margin: 40px auto; padding: 25px; line-height: 1.9;">

    <h1>سياسة الخصوصية</h1>
    <h2>Horizon Aden Hotel</h2>

    <p>
        نحترم خصوصية مستخدمي خدمات Horizon Aden Hotel،
        وتوضح هذه السياسة كيفية معالجة المعلومات عند التواصل معنا
        عبر WhatsApp والخدمات الرقمية المرتبطة به.
    </p>

    <h3>المعلومات التي تتم معالجتها</h3>
    <p>
        قد تتم معالجة رقم هاتف WhatsApp، ومحتوى الرسائل التي يرسلها
        المستخدم، وبيانات الرسائل اللازمة لتقديم خدمة العملاء
        والرد على الاستفسارات.
    </p>

    <h3>كيفية استخدام المعلومات</h3>
    <p>
        تستخدم المعلومات للرد على العملاء، وتقديم معلومات الفندق،
        والمساعدة في الاستفسارات والحجوزات والخدمات المتعلقة
        بتجربة العميل.
    </p>

    <h3>WhatsApp Business Platform</h3>
    <p>
        قد تتم معالجة الرسائل من خلال WhatsApp Business Platform
        والأدوات التقنية التي يستخدمها Horizon Aden Hotel
        لتقديم خدمة العملاء.
    </p>

    <h3>مشاركة المعلومات</h3>
    <p>
        لا نبيع المعلومات الشخصية للمستخدمين. وقد تتم معالجة
        البيانات بواسطة مزودي الخدمات التقنية بالقدر اللازم
        لتشغيل خدمة المراسلة وتقديم الخدمة المطلوبة.
    </p>

    <h3>الاحتفاظ بالبيانات</h3>
    <p>
        نحتفظ بالمعلومات للمدة اللازمة لتقديم الخدمة والوفاء
        بالمتطلبات التشغيلية أو القانونية المطبقة، ثم يتم حذفها
        أو التعامل معها وفق الإجراءات المناسبة.
    </p>

    <h3>طلبات الخصوصية والحذف</h3>
    <p>
        يمكن للمستخدم التواصل مع Horizon Aden Hotel لطلب معلومات
        بشأن بياناته أو طلب حذفها، مع مراعاة المتطلبات القانونية
        والتشغيلية السارية.
    </p>

    <h3>تحديث السياسة</h3>
    <p>
        قد يتم تحديث سياسة الخصوصية عند تغيير الخدمات أو المتطلبات
        التقنية والتنظيمية.
    </p>

    <p>
        آخر تحديث: نوفمبر 2026
    </p>

</body>
</html>
    """, 200
@app.route("/connect", methods=["GET"])
def connect_whatsapp():
    return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Horizon WhatsApp Connection</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 60px auto;
            padding: 30px;
            text-align: center;
        }

        button {
            background-color: #25D366;
            color: white;
            border: none;
            padding: 15px 25px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
        }

        button:hover {
            background-color: #1ebe5d;
        }

        #status {
            margin-top: 25px;
            white-space: pre-wrap;
        }
    </style>
</head>

<body>

    <h1>Horizon WhatsApp</h1>

    <p>
        ربط رقم واتساب الفندق مع Horizon Cloud API
        مع الاحتفاظ بـ WhatsApp Business على الجوال.
    </p>

    <button onclick="launchWhatsAppSignup()">
        ربط رقم WhatsApp Business
    </button>

    <div id="status"></div>

    <script>
        window.fbAsyncInit = function() {
            FB.init({
                appId: '1892603858377343',
                autoLogAppEvents: true,
                xfbml: true,
                version: 'v27.0'
            });
        };
    </script>

    <script async defer crossorigin="anonymous"
        src="https://connect.facebook.net/en_US/sdk.js">
    </script>

    <script>
        function fbLoginCallback(response) {
            if (response.authResponse) {
                const code = response.authResponse.code;

                document.getElementById("status").innerText =
                    "تم إكمال خطوة التسجيل في Meta بنجاح.\\n" +
                    "تم استلام رمز التفويض.";
            } else {
                document.getElementById("status").innerText =
                    "لم تكتمل عملية الربط.";
            }
        }

        function launchWhatsAppSignup() {
            document.getElementById("status").innerText =
                "جاري فتح WhatsApp Embedded Signup...";

            FB.login(
                fbLoginCallback,
                {
                    config_id: '1133590566040031',
                    response_type: 'code',
                    override_default_response_type: true,
                    extras: {
                        setup: {},
                    
    featureType: 'whatsapp_business_app_onboarding'
                    }
                }
            );
        }

        window.addEventListener(
            'message',
            function(event) {
                if (
                    event.origin !== 'https://www.facebook.com' &&
                    event.origin !== 'https://web.facebook.com'
                ) {
                    return;
                }

                try {
                    const data =
                        typeof event.data === 'string'
                            ? JSON.parse(event.data)
                            : event.data;

                    if (data && data.type === 'WA_EMBEDDED_SIGNUP') {
                        console.log(
                            'WhatsApp Embedded Signup event:',
                            data
                        );

                        document.getElementById("status").innerText =
                            "تم استقبال بيانات WhatsApp من Meta.";
                    }
                } catch (error) {
                    console.log(
                        'Embedded Signup event:',
                        event.data
                    );
                }
            }
        );
    </script>

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
