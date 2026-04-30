from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agent.graph import create_agent_graph
from app.api.routes import chat_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    graph = create_agent_graph() # initialize graph once at server startup
    app.state.graph = graph
    yield


app = FastAPI(
    title="Portfolio Assistant API",
    description="Agentic AI backend for portfolio chatbot",
    version="1.0.0",
    lifespan=lifespan,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://prashantnathv2.netlify.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router.router,prefix="/api")


@app.api_route("/health",methods=["GET","HEAD"])
async def health():
    return {"status": "ok"}