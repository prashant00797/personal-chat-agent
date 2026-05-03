import os
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from app.core.config import get_settings
from app.services.pinecone_service import pc_index

# Initialization
config = get_settings()
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
emedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

@tool
def retrieve_relevant_chunks(query:str):
    """
        Search Prashant's personal knowledge base to answer questions about him.
        Use this for questions about his background, experience, skills, tech stack,
        education, availability, location, job preferences,
        salary expectations, contact information or personal interests.
        When in doubt about anything related to Prashant — use this tool first.
        Input: a natural language question string.
    """ 
    try: 
     query_embeddings = emedding_model.embed_query(query)
     relevant_chunks = pc_index.query(
     vector=query_embeddings,
     top_k=5, 
     include_metadata=True,
     include_values=False)
    
     return [
        {
            "text":chunks.metadata["text"],
            "source":chunks.metadata["source"]
        }

        for chunks in relevant_chunks["matches"] # type: ignore
      ]
    except Exception:
       return "Knowledge base temporarily unavailable."
