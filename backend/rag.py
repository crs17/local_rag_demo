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




prompt = (
    "You have access to a tool that retrieves context about the Napoleonic wars. "
    "Use the tool to help answer user queries. "
    "Base your answer ONLY on the content returned by the tool. "
    "Do not add any facts, names, or details that are not explicitly stated in the retrieved context—even if you think you know them. "
    "If the retrieved context says only X and Y, then your answer must mention only X and Y. "
    "Do not make up information. If the context does not contain the answer, say so."
)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

weaviate_client = weaviate.connect_to_local()
vector_store = WeaviateVectorStore(
    client=weaviate_client,
    index_name="napoleonic_wars",
    text_key="text",
    embedding=embeddings,
)

llm = ChatOllama(
    model="llama3.2",
    temperature=0.0,
    seed=42,
)

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


agent = create_agent(
    llm,
    tools=[retrieve_context],
    system_prompt=prompt
)
