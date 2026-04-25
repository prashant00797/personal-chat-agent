import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.core.config import get_settings

config = get_settings()

def getcheckpointer():
    return AsyncPostgresSaver.from_conn_string(config.SUPABASE_DB_SESSION_POOLER)


# run once to create the table - uv run app.db.checkpointer
if __name__ == "__main__":
    import asyncio
    async def setup():
        async with getcheckpointer() as cp:
            await cp.setup()
            print("Tables created")
    asyncio.run(setup())
