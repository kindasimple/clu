#!/bin/bash
# scan the ~/Journal directory recursively for all .md files
# and find the text string "## Notes" in each file. Recreate
# the file structure in a local directory where each file
# contains the contents after the string "## Notes".
find ~/Journal -type f -name '*.md' -exec sh -c '
  content=$(awk "/## Notes/{flag=1; next} flag" "{}" | sed "s/[[:space:]]*$//");
  if [ -n "$content" ]; then
    mkdir -p ./notes/$(dirname "{}" | sed "s|^$HOME/Journal|.|");
	echo "$content" > ./notes/$(echo "{}" | sed "s|^$HOME/Journal|.|");
  fi
' \;