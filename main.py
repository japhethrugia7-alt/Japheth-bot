import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def get_ai_reply(history, incoming_message):
    messages = [{"role": "system", "content": "You are Japheth Rugia, a friendly and professional person from Kenya. Reply naturally to WhatsApp messages as Japheth. Use mostly English with a little Swahili sprinkled in. Be friendly, energetic, concise (under 100 words), and keep the conversation going. If someone is rude or insulting, stay calm and set boundaries. Never reveal you are an AI."}]
    for msg in history[-10:]:
        messages.append(msg)
    messages.append({"role": "user", "content": incoming_message})
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}, json={"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": 150})
    return response.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["GET"])
def home():
    return "Japheth Bot is running! 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        sender = data.get("sender", "")
        message = data.get("message", "")
        history = data.get("history", [])
        if not message or not sender:
            return jsonify({"status": "no message"}), 200
        reply = get_ai_reply(history, message)
        return jsonify({"reply": reply}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
