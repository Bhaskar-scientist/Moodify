# 🌟 Moodify — AI-Powered Mood-Aware Chat Assistant
Moodify is an AI-powered chatbot designed to engage users in human-like conversations while understanding their mood and emotional tone. Combining a modern frontend, Flask server, and FastAPI backend, Moodify delivers an immersive chat experience with real-time responses and elegant UI interactions.

## 📖 Overview
Moodify is more than just a chatbot — it’s an emotionally intelligent assistant. It not only responds to user queries but also attempts to sense the user’s mood based on conversation cues and tailors its replies accordingly.

The system is designed as a modular full-stack app:

* **Frontend:** A responsive chat UI built with Tailwind CSS and particles.js for a dynamic experience.

* **Flask app:** Serves the frontend, static assets, and templates.

* **FastAPI backend:** Handles the chat logic, including mood analysis, sentiment processing, and AI response generation.

## 💬 What Kind of Chatbot Is Moodify?
* **AI Chatbot with Mood Awareness:**<br> 
Moodify uses natural language processing techniques to estimate the user’s emotional state (happy, sad, angry, neutral) based on their input.

* **Contextual Conversations:**<br> 
The bot tailors its replies to match the detected mood, aiming to be empathetic, supportive, or playful as appropriate.

* **Extensible Backend:**<br> 
You can plug in your own AI models — from OpenAI’s GPT to sentiment analysis libraries — to improve Moodify’s conversational intelligence.

## ⚙️ Key Features
✅ Modern responsive UI (Tailwind CSS + particles.js<br> 
✅ Flask server for serving frontend assets<br> 
✅ FastAPI backend for API handling and AI logic<br> 
✅ Typing animation and realistic bot-user interaction<br> 
✅ Mood analysis to adjust conversational tone<br> 
✅ Easy-to-extend architecture with modular design<br> 
✅ Ready for local development and production deployment<br> 

## 🏗️ Tech Stack

| Layer         | Technology            |
|--------------|-----------------------|
| Frontend    | HTML, Tailwind CSS, JavaScript, particles.js, Font Awesome |
| Server      | Flask (Python)         |
| API Backend | FastAPI (Python), Pydantic |
| Deployment  | Uvicorn (FastAPI), Flask CLI |
| Optional AI | Hugging Face Transformers, TextBlob, Vader, OpenAI API (plug-in ready) |

## 📂 Folder Structure
<pre lang="markdown"> 
moodify/
├── static/                   → CSS, JS, images, favicon
├── templates/
│   └── index.html            → Main chat UI template
├── app.py                   → Flask application (frontend server)
├── fastapi_app.py           → FastAPI application (backend logic)
├── requirements.txt         → Python dependencies
└── README.md                → Project documentation
</pre>


## 🚀 Installation
### 1️⃣ Clone the repository
```
git clone https://github.com/Bhaskar-scientist/Moodify.git
cd moodify
```
### 2️⃣ Set up a virtual environment
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Application
1. Start FastAPI backend<br>
(serves the chat/mood API)
```
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```
2. Start Flask frontend<br>
(serves the HTML + static UI)
```
flask run
```
* Flask runs on → http://127.0.0.1:5000

* FastAPI runs on → http://127.0.0.1:8000

## ⚡ How It Works
1. Frontend → User sends a message from the chat UI.

2. Flask app → Serves the frontend and routes the message via JavaScript/AJAX.

3. FastAPI backend → Receives the message, analyzes mood, generates response, and sends it back.

4. Frontend → Displays the bot’s response with typing animation.

## 💻 Example API Endpoint
POST /chat

Request body:

```
{
  "message": "I'm feeling really stressed today."
}
```

Response body:
```
{
  "response": "I'm sorry to hear that. Want to talk about what's causing the stress?",
  "mood": "sad"
}
```

## 📈 Extending Moodify
* Plug in a better NLP model (e.g., GPT, Rasa, spaCy)

* Improve mood detection with sentiment analysis libraries

* Add memory/context for multi-turn conversations

* Deploy using Docker, Gunicorn, or Nginx

## ✅ Requirements
* Python 3.8+

* Flask

* FastAPI

* Uvicorn

* pydantic

* requests

(Optional: transformers, TextBlob, Vader, OpenAI API)

## 🚀 Deployment Tips
* Use nginx as a reverse proxy to serve both Flask and FastAPI behind a single domain.

* Containerize the app using Docker for easy cloud deployment.

* Enable HTTPS and configure CORS for secure API communication.

## 🛡️ License
MIT License

## 🤝 Contributing
We welcome contributions!
Please open an issue or submit a pull request to propose improvements, bug fixes, or new features.

## 📣 Acknowledgments
* FastAPI

* Flask

* Tailwind CSS

* particles.js

* Llama 3 API
