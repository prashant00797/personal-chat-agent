import os
import traceback
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import get_settings

config = get_settings()
os.environ["PINECONE_API_KEY"] = config.PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

# initializing imports for indexing
document_path = "./knowledge_base/Prashant_kb.pdf"
loader = PyPDFLoader(document_path)
splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)


# pincone client intialization
pc = Pinecone(pinecone_api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)
index.delete(delete_all=True) # clear existing vectors before re-indexing

try:

   if(os.path.exists(document_path)):
      docs = loader.load()
      chunks = splitter.split_documents(docs)
      embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
      vector_store = PineconeVectorStore.from_documents(
       documents=chunks,
       embedding=embeddings,
       index_name=config.PINECONE_INDEX_NAME
      )
      print("Indexing Successful",len(chunks));
except Exception as e:
   traceback.print_exc()
   raise e