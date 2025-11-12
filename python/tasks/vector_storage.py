import os
from pymongo import MongoClient
from dotenv import load_dotenv
from python.tasks.chunks_generator import chunks

from langchain_voyageai import VoyageAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch

load_dotenv()

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
MONGODB_ATLAS_CLUSTER_URI = os.getenv("MONGODB_ATLAS_CLUSTER_URI")

client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
DB_NAME = "Database_resume"
COLLECTION_NAME = "resume"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-index-vectorstores"

embedding_function = VoyageAIEmbeddings(
    voyage_api_key=VOYAGE_API_KEY,
    model="voyage-3.5-lite"
)

vector_store = MongoDBAtlasVectorSearch.from_documents(
    documents = chunks,
    embedding = embedding_function,
    collection = MONGODB_COLLECTION,
    index_name = ATLAS_VECTOR_SEARCH_INDEX_NAME
)

print(f"Successfully added {len(chunks)} chunks to MongoDB Atlas Vector Search collection '{COLLECTION_NAME}' in database '{DB_NAME}'.")

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 1, "score_threshold": 0.75},
)

