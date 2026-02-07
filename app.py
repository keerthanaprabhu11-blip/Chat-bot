from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Load intents
intents = {
    "greet": ["hi", "hello", "hey"],
    "bye": ["bye", "goodbye"],
    "sad": ["sad", "depressed", "unhappy"],
    "thanks": ["thanks", "thank you"],
    "faq": ["what", "how", "when", "where"]
}

responses = {
    "greet": "Hello! 😊 How can I help you?",
    "bye": "Goodbye! 👋 Have a great day!",
    "sad": "I’m really sorry you feel this way. You’re not alone 💙",
    "thanks": "You’re welcome! 😄",
    "faq": "That’s a good question. Let me think… 🤔",
    "unknown": "I’m not sure about that. Can you rephrase?"
}

def get_intent(msg):
    msg = msg.lower()
    for intent, words in intents.items():
        for w in words:
            if w in msg:
                return intent
    return "unknown"

def log_chat(user, bot):
    with open("chat_log.txt", "a") as f:
        f.write(f"{datetime.now()} | User: {user} | Bot: {bot}\n")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    intent = get_intent(user_msg)

    reply = responses.get(intent, responses["unknown"])

    log_chat(user_msg, reply)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
