import os
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv 
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/wassup")
async def wassup():
    return {"message": "wrong route dawg"}

@app.post("/chat")
async def handle_chat(request: ChatRequest):
    user_prompt = request.message
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a specialist who carefully verifies information. 
                    You are skeptical and always do additional research.
                    I am not always right, and you are not always right either.
                    But we both strive to achieve the highest possible accuracy."""
                },
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            stream=False,
        )
        answer = response.choices[0].message.content
        return {"response": answer}
    except Exception as e:
        print(f"\nOpenAI API Error: {e}")
        return {"response": "Sorry, something went wrong."}