# Local RAG Agent
The purpose of this repo is to demonstrate how to build a basic local RAG agent. This could e.g. be used for making internal company documents "chattable".

The full demo can be seen [here](https://crs17.github.io/local_rag_demo/).

## Brief tech stack overview
- The [Ollama](https://ollama.com) official docker image is used managing and running the language models.
- We deploy Meta's [Llama3.2](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/) large language model and Nomic's [nomic-embed-text](https://www.nomic.ai/news/nomic-embed-text-v1) embedding model.
- [Weaviate](https://weaviate.io) is used as vector store.
- [LangChain](https://www.langchain.com) is used for orchestration of the RAG agent.
- The agent is deployed locally with the [LangGraph](https://www.langchain.com/langgraph) server.
- Finally, the [Agent Chat UI](https://docs.langchain.com/oss/python/langchain/ui) app is chosen as web UI.