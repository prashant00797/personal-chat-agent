from supabase import Client,create_client
from app.core.config import Settings

config = Settings() # type: ignore
sc :Client = create_client(config.SUPABASE_URL,config.SUPABASE_KEY)