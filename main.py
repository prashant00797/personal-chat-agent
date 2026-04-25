from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.agent.graph import create_agent_graph
from app.api.routes import chat_router,register_router
from app.db.checkpointer import getcheckpointer


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with getcheckpointer() as cp:
        graph = create_agent_graph(cp)
        app.state.graph = graph
        app.state.checkpointer = cp

        yield


app = FastAPI(
    title="Personal Chat Agent",
    description="Personal ReAct agent for portfolio with RAG & github search",
    version="1.0.0",
    lifespan=lifespan)


app.include_router(register_router.router,prefix="/api")
app.include_router(chat_router.router,prefix="/api")