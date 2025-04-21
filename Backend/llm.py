from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from typing import List
from fastapi.responses import JSONResponse
import os


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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

@app.get("/keepalive")
async def keep_alive():
    print("👋 Ping received — staying awake!")
    return JSONResponse({"message": "Still awake 🔥"})

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