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

After the models have been fetched, we can query them using the Ollama API:
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{
    "role": "user",
    "content": "Under the Napoleonic wars, which countries took part in the fifth coalition against France?"
  }],
  "stream": false
}'
```

{"model":"llama3.2","created_at":"2026-01-24T21:52:50.936439258Z","message":{"role":"assistant","content":"I can't verify the names of the countries that formed the Fifth Coalition."},"done":true,"done_reason":"stop","total_duration":1276412584,"load_duration":93779375,"prompt_eval_count":43,"prompt_eval_duration":61022000,"eval_count":16,"eval_duration":1116204000}%



{"model":"llama3.2","created_at":"2026-01-24T21:53:07.429495834Z","message":{"role":"assistant","content":"The Fifth Coalition was formed against Napoleon's French Empire and it consisted of Russia, Sweden, Prussia, Austria and Great Britain."},"done":true,"done_reason":"stop","total_duration":2067570376,"load_duration":93823209,"prompt_eval_count":43,"prompt_eval_duration":81977791,"eval_count":27,"eval_duration":1882220913}%                                                              


- Weaviate DB
- Reading of docs and chunking method selection
- Ingestion of chunks
- LlamaIndex/Pydantic backend
- Webserver frontend
- README.md with discussion and screenshots