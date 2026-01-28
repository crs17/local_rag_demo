import itertools

from langchain_text_splitters import RecursiveCharacterTextSplitter
import weaviate
from weaviate.classes.config import Configure
import wikipediaapi


def run():
    # Read the wiki page on the Napoleonic Wars
    wiki = wikipediaapi.Wikipedia(user_agent='Basic RAG Setup', language='en')
    wiki_page = wiki.page('Napoleonic_Wars')

    # Instantiate the text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    # Split each section of the wiki page into chunks
    documents = list(
        itertools.chain.from_iterable(    
            [
                [
                    {
                        'title': section.title,
                        'text': chunk,
                    }
                    for chunk in text_splitter.split_text(section.text)
                ]
                for section in wiki_page.sections
            ]
        )
    )

    # Vectorize and uplaod the chunk to the Weaviate DB
    with weaviate.connect_to_local() as client:

        if client.collections.exists('napoleonic_wars'):
            client.collections.delete('napoleonic_wars')

        napoleonic_wars = client.collections.create(
            name='napoleonic_wars',
            vector_config=Configure.Vectors.text2vec_ollama(  # Configure the Ollama embedding integration
                api_endpoint='http://host.docker.internal:11434',
                model='nomic-embed-text'
            )
        )

        with napoleonic_wars.batch.fixed_size(batch_size=100) as batch:
            for chunk in documents:
                batch.add_object(properties=chunk)

        print(f'Imported {len(documents)} chunks into the Napoleonic Wars collection')


if __name__ == "__main__":
    run()