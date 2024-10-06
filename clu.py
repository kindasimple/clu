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
import uuid
import json
import argparse

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "settings.json")
DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
STORE_PATH = os.path.join(os.path.dirname(__file__), "store")
CHATS_PATH = os.path.join(os.path.dirname(__file__), "chats")
SHARE_PATH = os.path.join(os.path.dirname(__file__), "share")
DEFAULT_MODEL = "llama3"
EX_CMD = ":"
LEADER = "\\"

COMMANDS = "".join({LEADER, EX_CMD})

CHAT_ID = uuid.uuid4().hex
chat_engine = None
chat_context: list[dict[str, str]] = []

CONFIG_DEFAULTS = {
    "model": "llama3",
    "agent_name": "clu",
    "data_path": os.path.join(os.path.dirname(__file__), "data"),
    "store_path": os.path.join(os.path.dirname(__file__), "store"),
    "chats_path": os.path.join(os.path.dirname(__file__), "chats"),
    "share_path": os.path.join(os.path.dirname(__file__), "share"),
}

# Load configuration from file
if not os.path.exists("config.json"):
    with open(CONFIG_PATH, "w", encoding="utf8") as f:
        json.dump(CONFIG_DEFAULTS, f)

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)


def build_index(model: str = None):
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = Ollama(model=model, request_timeout=360.0)

    # Try to load the vector store from cache
    index = None
    if os.path.exists("store"):
        storage_context = StorageContext.from_defaults(persist_dir=STORE_PATH)
        index = load_index_from_storage(storage_context=storage_context)

    if index is None:
        documents = SimpleDirectoryReader(
            input_dir=DATA_PATH,
            required_exts=[".md", ".txt"],
            recursive=True,
        ).load_data()
        print(f"Loaded {len(documents)} documents")

        # If cache does not exist, create the vector store
        index = VectorStoreIndex.from_documents(documents)

        # Save the vector store to cache
        index.storage_context.persist(persist_dir=STORE_PATH)
    return index


def parse_command(prompt) -> tuple[str, str, list[str]]:
    """
    Check if the prompt is a command
    """
    if prompt[0] in COMMANDS:
        args = prompt.lstrip(COMMANDS).split(" ")
        return prompt[0], args[0], args[1:]
    return None, None, None


def bindings(key, cmd, args):
    """
    Handle commands
    """
    global chat_context
    global chat_engine
    if key == EX_CMD:
        match cmd:
            case "help":
                print(
                    f"""Commands:
                {LEADER}save [path] - Save the chat to a file
                {LEADER}quit - Exit the chat
                {LEADER}share - Share the chat to a file
                """
                )
            case "save":
                os.makedirs(CHATS_PATH, exist_ok=True)
                path = os.path.join(CHATS_PATH, f"{CHAT_ID}.json")
                if args:
                    path = args[0]
                print("Saving to: ", path)
                with open(path, "w", encoding="utf8") as f:
                    f.write(json.dumps(chat_context, indent=4))
            case "quit" | "exit":
                sys.exit(0)
            case "share":
                os.makedirs(SHARE_PATH, exist_ok=True)
                path = os.path.join(SHARE_PATH, f"{CHAT_ID}.txt")
                data = chat_context[-1]
                with open(path, "w+", encoding="utf8") as f:
                    f.write(
                        f"""prompt: {data["prompt"]}\nresponse: {data["response"]}"""
                    )
                print("Saved to: ", path)
            case "model":
                if args[0]:
                    Settings.llm = Ollama(model=args[0], request_timeout=360.0)
                    print(f"Model set to: {args[0]}")
                else:
                    print(f"Current model: {Settings.llm.model}")


def main():
    parser = argparse.ArgumentParser(description="Query the vector store.")
    parser.add_argument(
        "query", type=str, nargs="*", help="The query string to search for."
    )
    parser.add_argument(
        "--citation", action="store_true", help="Print sources for the response."
    )
    parser.add_argument("--chat", action="store_true", help="Start a chat session.")
    parser.add_argument("--model", type=str, help="specify the model to use.")
    args = parser.parse_args()

    whoami = os.getlogin()
    global chat_engine

    if args.model:
        config["model"] = args.model

    index = build_index(model=config["model"])
    if not args.query or args.chat:
        chat_engine = index.as_chat_engine()

        # in a continuous loop, gather a prompt and generate a response
        prompt_user = not args.query
        while True:
            if not prompt_user:
                prompt = " ".join(args.query)
                print(f"{whoami}$ {prompt}")
                prompt_user = True
            else:
                prompt = input(f"{whoami}$ ")

            if prompt == "":
                continue

            key, cmd, cmd_args = parse_command(prompt)

            if key:
                bindings(key, cmd, cmd_args)
                if cmd == "model":
                    chat_engine = index.as_chat_engine()
                continue

            # response = chat_engine.chat(prompt)
            streaming_response = chat_engine.stream_chat(prompt)
            print(f"{config['agent_name']}: ", end="")
            response = []
            sources = []
            for token in streaming_response.response_gen:
                response.append(token)
                print(token, end="")
            print()
            sources = {
                node.metadata["file_path"] for node in streaming_response.source_nodes
            }
            chat_context.append(
                {
                    "prompt": prompt,
                    "response": "".join(response),
                    "sources": list(sources),
                }
            )
            if args.citation:
                print(f"sources: {', '.join(sources)}")
            print()
    else:
        query_engine = index.as_query_engine()
        query_string = " ".join(args.query)
        print(f"Query: {query_string}")
        response = query_engine.query(query_string)
        print(response)


if __name__ == "__main__":
    main()
