from pinecone import Pinecone
from app.core.config import Settings

config = Settings() # type: ignore
pc = Pinecone(api_key=config.PINECONE_API_KEY)
pc_index = pc.Index(config.PINECONE_INDEX_NAME)
   