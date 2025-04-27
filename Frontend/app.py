from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
import threading
import time
import os

app = Flask(__name__)
API_URL = "https://moodify2.onrender.com/chat"
conversation_history = {}

# Load emotion detection model
tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
EMOTION_LABELS = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion',
                  'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust', 'embarrassment',
                  'excitement', 'fear', 'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism',
                  'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral']

# Emoji mapping (can expand as needed)
EMOJI_MAP = {
    "joy": "😄",
    "gratitude": "😊",
    "sadness": "😔",
    "anger": "😠",
    "fear": "😟",
    "confusion": "😕",
    "disgust": "🤢",
    "surprise": "😲",
    "neutral": "😌"
}

# Detect emotion using HuggingFace transformer
def get_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.nn.functional.softmax(logits, dim=-1)[0]
    top_idx = torch.argmax(probs).item()
    return EMOTION_LABELS[top_idx], probs[top_idx].item()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')

    # Detect emotion
    emotion_label, emotion_confidence = get_emotion(user_message)
    emoji = EMOJI_MAP.get(emotion_label.lower(), "")
    
    # Create a mild influence system prompt (30% emotion bias)
    system_prompt = (
        "You are Moodify, a warm, emotionally aware assistant. "
        "While maintaining your own conversational logic, consider the user's emotional state: "
        f"{emotion_label}. Respond in a brief (max 60 words), empathetic but clear tone."
    )

    # Init or update conversation history
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    
    # Reset system prompt each time for partial emotion influence
    conversation_history[session_id] = [
        {"role": "system", "content": system_prompt}
    ] + conversation_history[session_id][-10:]  # keep last 10 messages

    conversation_history[session_id].append({"role": "user", "content": user_message})

    try:
        response = requests.post(
            API_URL,
            json={"messages": conversation_history[session_id]}
        )

        if response.status_code != 200:
            print(f"Backend error: {response.text}")
            return jsonify({"response": "Sorry, something went wrong."}), 500

        response_data = response.json()
        assistant_message = response_data["choices"][0]["message"]["content"]
        conversation_history[session_id].append({"role": "assistant", "content": assistant_message})

        return jsonify({
            "response": assistant_message,
            "emotion": emotion_label,
            "emoji": emoji,
            "confidence": f"{emotion_confidence:.2f}"
        })

    except Exception as e:
        print(f"Error calling backend API: {e}")
        return jsonify({"response": "Sorry, there was an error connecting to the AI service."}), 500

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    data = request.json
    session_id = data.get('session_id', 'default')
    conversation_history.pop(session_id, None)
    return jsonify({"status": "success"})

# Keepalive logic
def ping_fastapi():
    while True:
        try:
            res = requests.get("https://moodify2.onrender.com/keepalive")
            if res.status_code == 200:
                print(f"[{time.strftime('%H:%M:%S')}] ✅ Pinged backend:", res.json()["message"])
            else:
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Ping failed with status {res.status_code}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ Error pinging backend:", e)
        time.sleep(10 * 60)

threading.Thread(target=ping_fastapi, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
