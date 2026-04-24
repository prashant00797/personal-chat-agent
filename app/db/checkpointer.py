from langgraph.checkpoint.postgres import PostgresSaver

from app.core.config import get_settings

config = get_settings()

def getcheckpointer():
    return PostgresSaver.from_conn_string(config.SUPABASE_DB_SESSION_POOLER)


# run once to create the table - uv run app.db.checkpointer
if __name__ == "__main__":
    with getcheckpointer() as cp:
        cp.setup()
        print("✅ Tables created")