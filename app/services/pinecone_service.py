from pinecone import Pinecone
from app.core.config import get_settings

config = get_settings()
pc = Pinecone(api_key=config.PINECONE_API_KEY)
pc_index = pc.Index(config.PINECONE_INDEX_NAME)
   