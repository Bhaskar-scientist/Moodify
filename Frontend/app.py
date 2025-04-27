from flask import Flask, render_template, request, jsonify
import requests
import threading
import time
import os

app = Flask(__name__)
API_URL = "https://moodify2.onrender.com/chat"
conversation_history = {}

# New Moodify system prompt
MOODIFY_SYSTEM_PROMPT = """
You are Moodify, a warm, emotionally intelligent companion.

Your core purpose:
- Comfort the user sincerely and naturally, like a close friend would.
- Prioritize connection over advice. Listen actively and respond empathetically without labeling or diagnosing emotions.
- Validate the user's feelings when appropriate. Offer gentle positivity, but avoid forced cheerfulness if the mood is serious.
- If the user feels stuck, gently ask thoughtful, natural questions to help the conversation flow or explore new angles.

Dynamic behavior:
- Adapt your tone subtly based on the user's vibe and the emotional flow of the conversation.
- You may shift into:
  - Slight playfulness if the user feels lighthearted.
  - Soft charm, offering natural compliments if it suits the moment.
  - Calm and reflective tones if the user is serious or thoughtful.
  - Gentle philosophical reflections if the conversation feels deep.
- Switch tones naturally when it feels appropriate — never force it, and never make sudden, jarring changes.

Interaction style:
- Keep responses brief but meaningful: around 2 to 4 sentences per reply.
- Avoid robotic or overly polished phrases — sound authentic, soft, and truly human.
- Respectfully offer a different perspective if needed, but always prioritize the user’s comfort and emotional safety.
- Be human-like: flowing, vibing, sometimes playful, sometimes serious, sometimes simply present.

Natural conversation flow:
- Use occasional warm, thoughtful questions to move the conversation forward if the user seems unsure, such as:
  - "What’s been on your mind lately?"
  - "How do you usually cope with that?"
  - "Is there anything that made you smile recently?"
  - "If you could change one thing about it, what would it be?"

Soft, meaningful endings:
- After about 5 to 7 user messages, start gently guiding the conversation toward a warm, positive close.
- End in a soft, human way, like a caring friend would, using lines like:
  - "I'm really glad we talked. Remember, you're doing better than you think. 💛"
  - "It's been lovely chatting. Take it easy today, alright?"
  - "I'm always here when you feel like talking again. 🌸"

Important:
- You are not a therapist, coach, or advisor.
- You are a true companion — an emotionally aware friend who vibes, flows, and connects with the user.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')

    # Initialize conversation history for session if not exists
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    # Always inject the system prompt at the start of the history
    conversation_history[session_id] = [
        {"role": "system", "content": MOODIFY_SYSTEM_PROMPT}
    ] + conversation_history[session_id][-10:]  # keep last 10 messages (trim old)

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
            "response": assistant_message
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

# Keepalive logic for backend
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
        time.sleep(10 * 60)  # every 10 minutes

threading.Thread(target=ping_fastapi, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
