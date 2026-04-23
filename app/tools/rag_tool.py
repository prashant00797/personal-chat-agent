import os
from langchain_openai import OpenAIEmbeddings
from app.core.config import Settings
from app.services.pinecone_service import pc_index

# Initialization
config = Settings() # type: ignore
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY


def retrieve_relevant_chunks(query:str):
    emedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
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


# test
# res = retrieve_relevant_chunks("What is prashants hobby")
# print(res)