[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/amansingh0311-mcp-qdrant-openai-badge.png)](https://mseep.ai/app/amansingh0311-mcp-qdrant-openai)

# MCP Qdrant Server with OpenAI Embeddings

[![smithery badge](https://smithery.ai/badge/@amansingh0311/mcp-qdrant-openai)](https://smithery.ai/server/@amansingh0311/mcp-qdrant-openai)

This MCP server provides vector search capabilities using Qdrant vector database and OpenAI embeddings.

## Features

- Semantic search in Qdrant collections using OpenAI embeddings
- List available collections
- View collection information

## Prerequisites

- Python 3.10+ installed
- Qdrant instance (local or remote)
- OpenAI API key

## Installation

### Installing via Smithery

To install Qdrant Vector Search Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@amansingh0311/mcp-qdrant-openai):

```bash
npx -y @smithery/cli install @amansingh0311/mcp-qdrant-openai --client claude
```

### Manual Installation
1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/mcp-qdrant-openai.git
   cd mcp-qdrant-openai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL to your Qdrant instance (default: "http://localhost:6333")
- `QDRANT_API_KEY`: Your Qdrant API key (if applicable)

## Usage

### Run the server directly

```bash
python mcp_qdrant_server.py
```

### Run with MCP CLI

```bash
mcp dev mcp_qdrant_server.py
```

### Installing in Claude Desktop

```bash
mcp install mcp_qdrant_server.py --name "Qdrant-OpenAI"
```

## Available Tools

### query_collection

Search a Qdrant collection using semantic search with OpenAI embeddings.

- `collection_name`: Name of the Qdrant collection to search
- `query_text`: The search query in natural language
- `limit`: Maximum number of results to return (default: 5)
- `model`: OpenAI embedding model to use (default: text-embedding-3-small)

### list_collections

List all available collections in the Qdrant database.

### collection_info

Get information about a specific collection.

- `collection_name`: Name of the collection to get information about

## Example Usage in Claude Desktop

Once installed in Claude Desktop, you can use the tools like this:

```
What collections are available in my Qdrant database?

Search for documents about climate change in my "documents" collection.

Show me information about the "articles" collection.
```
