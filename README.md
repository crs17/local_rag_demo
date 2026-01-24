# Basic RAG Setup
Here I go through the steps of building a basic RAG setup. This could e.g. be used for making company-specific documents "chatable".

I will employ Weaviate as the vector DB, Pydantic AI as the RAG engine and FAST API as the web page frontend.

## Vector DB
A local instance of Weaviate is deployed in a Docker container using the official Weaviate image.
To build and run the Weaviate container (and the other containers) run:
```bash
make run
```

## Models
For this demonstration we use local models Ollama models. As embedding model we use `nomic-embed-text` and the choose Meta's `llama3.2` for LLM.

When the Docker containers are running, the models can be fetched with the command:
```bash
make fetch_models
```




- Weaviate DB
- Reading of docs and chunking method selection
- Ingestion of chunks
- LlamaIndex/Pydantic backend
- Webserver frontend
- README.md with discussion and screenshots