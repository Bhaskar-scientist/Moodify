from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from typing import List, Optional # Added Optional
from fastapi.responses import JSONResponse
import os


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://moodify-s79y.onrender.com"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DeepInfra API configuration
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# New model for the /start_chat request
class StartChatRequest(BaseModel):
    start: Optional[bool] = None # Optional, as the frontend sends { start: true }

@app.get("/keepalive")
async def keep_alive():
    print("👋 Ping received — staying awake!")
    return JSONResponse({"message": "Still awake 🔥"})

# New endpoint for /start_chat
@app.post("/start_chat")
async def start_chat_session(request: StartChatRequest):
    # The request body will be something like {"start": true}
    # For now, we'll just log that the chat session is starting
    # and return a success message.
    # You can add more complex logic here if needed in the future,
    # e.g., initializing session-specific data.
    if request.start:
        print("🚀 Chat session initiated by frontend.")
        return JSONResponse({"status": "success", "message": "Chat session started."})
    else:
        # Handle cases where 'start' might not be true or is missing, though frontend sends it as true
        print("⚠️ Received /start_chat request without 'start: true'.")
        return JSONResponse({"status": "noop", "message": "Start signal not explicitly true."}, status_code=200)


@app.post("/chat")
async def chat_completion(request: ChatRequest):
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            
            payload = {
                "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
                "messages": [msg.model_dump() for msg in request.messages],
                "max_tokens": 150,
                "temperature": 0.6,
                "top_p": 0.8
            }
            
            response = await client.post(
                API_URL,
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
            return response.json()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
