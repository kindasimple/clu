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
    ./scan.sh
    ```

    Build the clu vector database index and run a query.

    ```
    uv run clu.py "how can I build the clu a notes index and run a query"
    ```


Preprocess the Journal dev log

    ./scan.sh


Build the clu.py vector database index and run a query

    uv run clu.py how can I build the clu vector database index and run a query

Console output

    Reading inline script metadata from: clu.py
    Loaded 28 documents
    Query: how can I build the clu vector database index and run a query
    Run the script using uv, specifically the command `uv run clu.py "how can I build the clu a notes index and run a query"`. This will execute the necessary steps to build the CLU vector database index and then run the query.

Start a chat

    uv run clu.py --chat give me a curl command

    clu:  The curl command is used to retrieve a list of dogs from the Petfinder API, specifically the second page of results with 20 animals per page.
    sources: /clu/notes/2023/04/23.md, /clu/notes/2023/04/27.md, /clu/notes/2020/03/09.md

    root$ :share
    Saved to:  /clu/share/a0e04b0f46c1478681bccb55af2fa227.txt

    head /clu/share/a0e04b0f46c1478681bccb55af2fa227.txt
    prompt: give me a curl command
    response:  The curl command is used to retrieve a list of dogs from the Petfinder API, specifically the second page of results with 20 animals per page.

    root$ :share
    Saving to:  /clu/chats/4ecb201b4d0b45be9d1f5e02c6117a1a.json

Add script aliases `chat` and `clu` to `~/.bashrc`

        # ~/.bashrc
        CLU_HOME=$HOME/Code/clu
        function chat() {
            uv run --project $CLU_HOME clu.py --chat --citation "$@"
        }

        function clu() {
            uv run --project $CLU_HOME $HOME/Code/clu/clu.py --citation "$@"
        }

Use the `chat` and `clu` aliases to run the chat and clu scripts

    # chat what did I do in september
    Reading inline script metadata from: clu.py
    Loaded 172 documents
    root$ what did I do in september
    clu:  It seems that in September, I was actively experimenting with different neural network architectures and optimization methods to improve their performance. This might have been a productive month for me in terms of learning and personal development!
    sources: /clu/data/obsidian/notes/main/Learning/pytorch/Review/0.1 Neural Networks.md, /clu/data/obsidian/notes/main/Latest/2024-04/2024-04-28.md, /clu/data/obsidian/notes/main/Latest/2024-03/2024-03-01.md, /clu/data/obsidian/notes/main/Latest/Daily Plan.md, /clu/data/obsidian/notes/main/Latest/2024-03/2024-03-13.md, /clu/data/obsidian/notes/main/Learning/pytorch/Review/0.2 CNN.md