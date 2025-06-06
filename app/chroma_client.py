import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection_name = "property_data"
collection = None  

def init_chroma_collection():
    global collection
    try:
        collection = client.get_collection(name=collection_name)
    except:
        collection = client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    return collection

def get_chroma_collection():
    global collection
    if collection is None:
        collection = init_chroma_collection()
    return collection

