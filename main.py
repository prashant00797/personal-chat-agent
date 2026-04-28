from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat_router

app = FastAPI(
    title="Personal Chat Agent",
    description="Personal ReAct agent for portfolio with RAG & github search",
    version="1.0.0",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


app.include_router(chat_router.router)