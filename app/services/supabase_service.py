from supabase import Client,create_client
from app.core.config import get_settings

config = get_settings()
sc :Client = create_client(config.SUPABASE_URL,config.SUPABASE_KEY)