import chromadb
# setup Chroma in-memory, for easy prototyping. Can add persistence easily!
client = chromadb.Client()

# Create collection. get_collection, get_or_create_collection, delete_collection also available!
collection = client.create_collection("language-learning-assitant")
# Add docs to the collection. Can also update and delete. Row-based API coming soon!
# Read documents from local text files
with open ('path/to/doc1.txt', 'r') as f1 , open ('path/to/doc2.txt', 'r') as f2:
    doc1 = f1.read()
    doc2= f2.read()
collection.add(
    documents=["doc1", "doc2"], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
    metadatas=[{"source": "doc1.txt"}, {"source": "doc2.txt"}], # filter on these!
    ids=["doc1", "doc2"], # unique for each doc
)

# Query/search 2 most similar results. You can also .get by id
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)
print(results)