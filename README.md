# clu
An LLM RAG application to answer questions with insights from a work log journal


## Quickstart

Install [ollama](https://github.com/ollama/ollama) and start the LLM chat server

    curl -fsSL https://ollama.com/install.sh | sh
    ollama run llama3.2


Create a new journal entry. Here is an example of a [VSCode Journal](https://marketplace.visualstudio.com/items?itemName=pajoma.vscode-journal) entry for today.

    cat ~/Journal/2024/09/29.md

Console output

    # Sunday, September 29 2024

    ## Tasks

    ## Notes

    ```sh
    rm -rf store
    ./scan.sh
    ```

    Build the clu vector database index and run a query.

    ```
    uv run clu.py "how can I build the clu a notes index and run a query"
    ```


Preprocess the Journal dev log


    rm -rf store
    ./scan.sh


Build the clu.py vector database index and run a query

    uv run clu.py how can I build the clu vector database index and run a query

Console output

    Reading inline script metadata from: clu.py
    Loaded 28 documents
    Query: how can I build the clu vector database index and run a query
    Run the script using uv, specifically the command `uv run clu.py "how can I build the clu a notes index and run a query"`. This will execute the necessary steps to build the CLU vector database index and then run the query.
