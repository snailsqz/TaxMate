from ingest import qdrant, COLLECTION_NAME, embed_text

collections = qdrant.get_collections()
print(collections)

results = qdrant.scroll(collection_name=COLLECTION_NAME, limit=5)
for point in results.points:
    print(f"ID: {point.id}, Content: {point.payload['content']}")

query_vector = embed_text("ภาษีเงินได้บุคคลธรรมดา")
search_result = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_vector,
    limit=3
)
for hit in search_result:
    print(f"[Search Result] ID: {hit.id}, Content: {hit.payload['content']}")
