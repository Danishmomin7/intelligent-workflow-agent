from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.agent import AgentController
import os

app = FastAPI(title="Intelligent Workflow Agent - MVP")

# Allow frontend at localhost:3000 for development
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = AgentController()

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_id = body.get("user_id", "demo-user")
    text = body.get("text", "")
    result = await agent.handle_text(user_id=user_id, text=text)
    return JSONResponse(content=result)

@app.post("/api/schedule")
async def schedule(request: Request):
    body = await request.json()
    resp = await agent.schedule_meeting(body)
    return JSONResponse(content=resp)

@app.post("/api/summarize")
async def summarize(request: Request):
    body = await request.json()
    file_id = body.get("drive_file_id")
    text = body.get("text")  # optional direct text
    resp = await agent.summarize_document(file_id=file_id, text=text)
    return JSONResponse(content=resp)
