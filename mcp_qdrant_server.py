#!/usr/bin/env python3
"""
Qdrant MCP Server - Provides vector search capabilities using OpenAI embeddings
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Environment variables must be set manually.")

import openai
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from mcp.server.fastmcp import FastMCP, Context


# Initialize Qdrant client
def get_qdrant_client() -> QdrantClient:
    """Get Qdrant client from environment variables or defaults"""
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY", None)

    if url.startswith("http"):
        return QdrantClient(url=url, api_key=api_key)
    else:
        # For local file-based storage
        return QdrantClient(path=url)


# Function to create embeddings
def get_embedding(text: str) -> List[float]:
    """Get embeddings from OpenAI API"""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
    response = client.embeddings.create(model=model, input=text)

    return response.data[0].embedding


# Create MCP Server
mcp = FastMCP("Qdrant-OpenAI")


@dataclass
class QdrantContext:
    client: QdrantClient


@mcp.tool()
def query_collection(query_text: str) -> str:
    """
    Search a Qdrant collection using semantic search with OpenAI embeddings.

    Args:
        collection_name: Name of the Qdrant collection to search
        query_text: The search query in natural language
        limit: Maximum number of results to return (default: 5)
        model: OpenAI embedding model to use (default: text-embedding-3-large)

    Returns:
        JSON string containing search results
    """
    # Get Qdrant client from context
    client = get_qdrant_client()

    # Generate embedding for query
    model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "default")
    query_vector = get_embedding(query_text)

    # Search Qdrant
    try:
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=50,
            score_threshold=0.5,
        )

        # Format results
        results = []
        for scored_point in search_result:
            result = {
                "id": scored_point.id,
                "score": scored_point.score,
                "payload": scored_point.payload,
            }
            results.append(result)

        return json.dumps({"results": results}, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


# @mcp.tool()
# async def list_collections() -> str:
#     """
#     List all available collections in the Qdrant database.

#     Returns:
#         JSON string containing the list of collections
#     """
#     client = get_qdrant_client()

#     try:
#         collections = client.get_collections()
#         return json.dumps({"collections": [c.name for c in collections.collections]}, indent=2)
#     except Exception as e:
#         return json.dumps({"error": str(e)})


@mcp.tool()
def collection_info() -> str:
    """
    Get information about a specific collection.

    Args:
        collection_name: Name of the collection

    Returns:
        JSON string containing collection information
    """
    client = get_qdrant_client()

    try:
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "default")
        collection_info = client.get_collection(collection_name)
        return json.dumps(
            {
                "vectors_count": collection_info.vectors_count,
                "points_count": collection_info.points_count,
                "dimension": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    # Run the server
    mcp.run(transport="stdio")
