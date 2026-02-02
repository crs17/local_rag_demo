import json
import requests

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_weaviate import WeaviateVectorStore
import weaviate


def query_raw_model(query):
    r = requests.post(
        'http://localhost:11434/api/chat',
        data=json.dumps({
            'model': 'llama3.2',
            "messages": [{
                "role": "user",
                "content": query,
            }],
            "stream": False
        })
    )
    r.raise_for_status()

    return r.json()['message']['content']


class LocalRAGAgent:
    prompt = (
        "You have access to a tool that retrieves context about the Napoleonic wars. "
        "Use the tool to help answer user queries."
    )

    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
        )
        self.weaviate_client = weaviate.connect_to_local()
        self.vector_store = WeaviateVectorStore(
            client=self.weaviate_client,
            index_name="napoleonic_wars",
            text_key="text",
            embedding=self.embeddings,
        )
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0.0,
        )

        @tool(response_format="content_and_artifact")
        def retrieve_context(query: str):
            """Retrieve information to help answer a query."""
            retrieved_docs = self.vector_store.similarity_search(query, k=2)
            serialized = "\n\n".join(
                (f"Source: {doc.metadata}\nContent: {doc.page_content}")
                for doc in retrieved_docs
            )
            return serialized, retrieved_docs

        tools = [retrieve_context]
        self.agent = create_agent(
            self.llm, tools, system_prompt=self.prompt
        )


    def stream(self, query):
        messages = {"messages": [{"role": "user", "content": query}]}
        for event in self.agent.stream(messages, stream_mode="values"):
            yield event

    def __del__(self):
        self.weaviate_client.close()

