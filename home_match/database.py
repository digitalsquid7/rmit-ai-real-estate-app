import json

import chromadb


def query_collection(collection, query):
    """Perform a vector search on the given ChromaDB collection."""
    results = collection.query(query_texts=[query], n_results=3)
    return results


def setup_collection(config):
    """Create a ChromaDB collection using real estate listing from the local JSON file."""

    client = chromadb.Client(chromadb.Settings(anonymized_telemetry=False))
    collection = client.create_collection("real_estate_listings")
    documents = generate_documents(config)
    ids = [str(i) for i in range(1, len(documents) + 1)]
    collection.add(documents=documents, ids=ids)

    return collection


def generate_documents(config):
    """Create documents for ChromaDB from the real estate listings JSON file.
    Vector searches work best on strings, so this function converts the JSON listing objects to strings."""
    documents = []

    with open(config.real_estate_listings_path, 'r') as file:
        data = json.load(file)

    for listing in data['listings']:
        documents.append(
            f"""\
Property: {listing['property_type']} in {listing['neighborhood']}
Price: {listing['price']}
Bedrooms: {listing['bedrooms']}
Bathrooms: {listing['bathrooms']}
Area: {listing['area_sqft']} square feet
Description: {listing['description']}"""
        )

    return documents
