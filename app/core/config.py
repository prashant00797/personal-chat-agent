from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY:str
    PINECONE_INDEX_NAME:str
    PINECONE_API_KEY:str
    PINECONE_HOST:str
    SUPABASE_URL:str
    SUPABASE_KEY:str

    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings() # type: ignore