from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import threading
import time

app = Flask(__name__)
API_URL = "http://localhost:8000/chat"
conversation_history = {}
analyzer = SentimentIntensityAnalyzer()

# Mapping logic for emotion detection
def get_emotion(text):
    sentiment = analyzer.polarity_scores(text)
    neg = sentiment['neg']
    neu = sentiment['neu']
    pos = sentiment['pos']
    text_lower = text.lower()

    greetings = {"hi", "hello", "hey", "greetings", "yo", "hola"}

    if text_lower.strip() in greetings:
        return "Greeting"
    if pos > 0.7:
        return "Joy / Excited"
    elif 0.4 < pos <= 0.7:
        return "Content / Grateful"
    elif neu > 0.7:
        return "Confused / Lost"
    elif neu > 0.6:
        return "Neutral / Calm"
    elif neg > 0.6:
        return "Sad / Lonely"
    elif neg > 0.5 and pos < 0.2:
        return "Angry / Frustrated"
    elif neg > 0.4 and neu > 0.4:
        return "Anxious / Worried"
    elif "gross" in text_lower or "nasty" in text_lower or "disgusting" in text_lower:
        return "Disgusted"
    elif any(word in text_lower for word in ["wow", "really?", "no way", "omg"]):
        return "Surprised"
    else:
        return "Neutral / Calm"
    

EMOJI_MAP = {
    "Joy / Excited": "😄",
    "Content / Grateful": "😊",
    "Neutral / Calm": "😌",
    "Sad / Lonely": "😔",
    "Angry / Frustrated": "😠",
    "Anxious / Worried": "😟",
    "Confused / Lost": "😕",
    "Disgusted": "🤢",
    "Surprised": "😲"
}




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')

    # Detect emotion
    emotion_label = get_emotion(user_message)
    emoji = EMOJI_MAP.get(emotion_label, "")
    message_with_emotion = f"Emotion detected: {emotion_label}\n{user_message}"

    # Init conversation history
    if session_id not in conversation_history:
        conversation_history[session_id] = [
            {"role": "system", "content": "You are Moodify, an emotionally intelligent assistant. Keep responses brief (under 60 words), casual, and deeply empathetic based on detected user emotions."}
        ]

    conversation_history[session_id].append({"role": "user", "content": message_with_emotion})

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
        print(emoji)

        return jsonify({"response": assistant_message, "emotion": emotion_label,"emoji": emoji})
        

    except Exception as e:
        print(f"Error calling backend API: {e}")
        return jsonify({"response": "Sorry, there was an error connecting to the AI service."}), 500

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    data = request.json
    session_id = data.get('session_id', 'default')
    conversation_history[session_id] = [
        {"role": "system", "content": "You are Moodify, an emotionally intelligent assistant. Keep your tone warm, concise, and friendly, adapting based on emotions like joy, sadness, confusion, or excitement."}
    ]
    return jsonify({"status": "success"})

def ping_fastapi():
    while True:
        try:
            res = requests.get("http://localhost:8000/keepalive")
            if res.status_code == 200:
                print(f"[{time.strftime('%H:%M:%S')}] ✅ Pinged backend:", res.json()["message"])
            else:
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Ping failed with status {res.status_code}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ Error pinging backend:", e)
        time.sleep(10 * 60)  # ping every 13 minutes

# Start the pinging thread when Flask starts
threading.Thread(target=ping_fastapi, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
