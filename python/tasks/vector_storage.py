import os
from pymongo import MongoClient
from dotenv import load_dotenv
from tasks.chunks_generator import chunks
from langchain_voyageai import VoyageAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch

load_dotenv()

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
MONGODB_ATLAS_CLUSTER_URI = os.getenv("MONGODB_ATLAS_CLUSTER_URI")

client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
DB_NAME = "Database_resume"
COLLECTION_NAME = "resume"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"

embedding_function = VoyageAIEmbeddings(
    voyage_api_key=VOYAGE_API_KEY,
    model="voyage-3.5-lite"
)

# Check if we need to add documents
current_count = MONGODB_COLLECTION.count_documents({})
if current_count == 0:
    vector_store = MongoDBAtlasVectorSearch.from_documents(
        documents=chunks,
        embedding=embedding_function,
        collection=MONGODB_COLLECTION,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME
    )
    print(f"Successfully added {len(chunks)} chunks to MongoDB.")
else:
    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=embedding_function,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME
    )

# Create retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
