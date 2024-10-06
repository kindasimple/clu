#!/bin/bash

# determine the most frequent bash commands

find ./data/cli -type f -name bash_history_*.txt -exec sh -c '
    echo "cmd count" > ./data/cli/frequency_$(basename "{}" .txt).txt
    cat {} | awk '"'"'{cmd[$1]++} END { for (c in cmd) print c, cmd[c]}'"'"' | sort -rnk 2 >> ./data/cli/frequency_$(basename "{}" .txt).txt
' \;

