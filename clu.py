# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llama-index",
#     "llama-index-embeddings-huggingface",
#     "llama-index-llms-ollama",
# ]
# ///
import os
import sys

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama


def build_index():
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)

    store_path = "store"

    # Try to load the vector store from cache

    index = None
    if os.path.exists("store"):
        storage_context = StorageContext.from_defaults(persist_dir=store_path)
        index = load_index_from_storage(storage_context=storage_context)

    if index is None:
        documents = SimpleDirectoryReader(
            input_dir="./notes/",
            required_exts=[".md"],
            recursive=True,
        ).load_data()
        print(f"Loaded {len(documents)} documents")

        # If cache does not exist, create the vector store
        index = VectorStoreIndex.from_documents(documents)

        # Save the vector store to cache
        index.storage_context.persist(persist_dir=store_path)
    return index


def main():
    if len(sys.argv) < 2:
        print("Usage: python clu.py <query_string>")
        sys.exit(1)

    whoami = os.getlogin()

    index = build_index()
    if len(sys.argv) == 1 or sys.argv[1] == "--chat":
        chat_engine = index.as_chat_engine()
        # in a continuous loop, gather a prompt and generate a response
        while True:
            if len(sys.argv) > 2:
                prompt = " ".join(sys.argv[2:])
                sys.argv = sys.argv[:1]
                print(f"{whoami}: {prompt}")
            else:
                prompt = input(f"{whoami}: ")
            if prompt == "exit":
                break
            streaming_response = chat_engine.stream_chat(prompt)
            print("clu: ", end="")
            for token in streaming_response.response_gen:
                print(token, end="")
            print()
    else:
        query_engine = index.as_query_engine()
        query_string = " ".join(sys.argv[1:])
        print(f"Query: {query_string}")
        response = query_engine.query(query_string)
        print(response)

if __name__ == '__main__':
    main()