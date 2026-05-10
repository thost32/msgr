import os
import requests
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# --- Config from environment variables ---
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "my_secret_verify_token")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# --- Load your knowledge base once at startup ---
def load_knowledge():
    try:
        with open("knowledge.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            print("✅ Knowledge base loaded successfully.")
            return content
    except FileNotFoundError:
        print("⚠️  knowledge.txt not found. Bot will use general knowledge only.")
        return ""

KNOWLEDGE = load_knowledge()
groq_client = Groq(api_key=GROQ_API_KEY)


# --- Facebook Webhook Verification (GET) ---
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verified by Facebook.")
        return challenge, 200

    print("❌ Webhook verification failed.")
    return "Forbidden", 403


# --- Receive Messages from Facebook (POST) ---
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]

                # Handle text messages only
                if "message" in event:
                    msg = event["message"]
                    # Skip messages sent by the page itself (echoes)
                    if msg.get("is_echo"):
                        continue
                    if "text" in msg:
                        user_text = msg["text"]
                        print(f"📩 Message from {sender_id}: {user_text}")
                        reply = get_groq_reply(user_text)
                        send_facebook_message(sender_id, reply)

    return "OK", 200


# --- Ask Groq for a reply ---
def get_groq_reply(user_message):
    system_prompt = """You are a friendly and helpful assistant for a Facebook page.
Your job is to answer customer questions based on the business information provided below.
Be warm, concise, and helpful. Keep replies short (2-4 sentences max) since this is a chat.
If a question is not covered in the information, politely say:
"I don't have that info right now, but feel free to contact us directly and we'll be happy to help!"

--- BUSINESS INFORMATION ---
{knowledge}
--- END OF BUSINESS INFORMATION ---""".format(knowledge=KNOWLEDGE if KNOWLEDGE else "No specific info provided.")

    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        print(f"🤖 Groq reply: {reply}")
        return reply
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return "Sorry, I'm having a little trouble right now. Please try again in a moment! 😊"


# --- Send reply back to Facebook Messenger ---
def send_facebook_message(recipient_id, text):
    url = "https://graph.facebook.com/v19.0/me/messages"
    headers = {"Content-Type": "application/json"}
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code != 200:
        print(f"❌ Facebook send error: {response.text}")
    else:
        print(f"✅ Reply sent to {recipient_id}")


# --- Health check route ---
@app.route("/", methods=["GET"])
def home():
    return "✅ Facebook Messenger Bot is running!", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
