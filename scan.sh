#!/bin/bash

# download README files from repos
readme=(
    https://raw.githubusercontent.com/kindasimple/clu/refs/heads/main/README.md
    https://raw.githubusercontent.com/ollama/ollama/refs/heads/main/README.md
    https://raw.githubusercontent.com/meta-llama/llama/refs/heads/main/README.md
)
for url in "${readme[@]}"; do
    mkdir -p ./data/repos/$(dirname $(echo "$url" | sed -e 's|^[^:]*://[^/]*/||'))
    curl -s $url > ./data/repos/$(echo "$url" | sed -e 's|^[^:]*://[^/]*/||')
done


# scan the ~/Journal directory recursively for all .md files
# and find the text string "## Notes" in each file. Recreate
# the file structure in a local directory where each file
# contains the contents after the string "## Notes".
find ~/Journal -type f -name '*.md' -exec sh -c '
  root=$HOME/Journal
  dest=./data/journal/
  content=$(awk "/## Notes/{flag=1; next} flag" "{}" | sed "s/[[:space:]]*$//");
  if [ -n "$content" ]; then
    mkdir -p $dest/$(dirname "{}" | sed "s|^$root|.|");
	echo "$content" > $dest/$(echo "{}" | sed "s|^$root|.|");
  fi
' \;

# copy directories from some obsidian from markdown sources
find ~/notes -type f -name '*.md' -exec sh -c '
  root=$HOME/notes
  dest=./data/obsidian/
  content=$(cat "{}" | sed "s/[[:space:]]*$//");
  if [ -n "$content" ]; then
    folder=$(dirname "{}" | sed "s|^$root|.|");
    mkdir -p "${dest}/${folder}";
	echo "$content" > ${dest}/$(echo "{}" | sed "s|^$root|.|");
  fi
' \;

mkdir -p ./data/cli
cp $HOME/.bash_history ./data/cli/bash_history_$(date +%Y%m%d%H%M%S).txt

rm -rf ./store

./analyze.sh