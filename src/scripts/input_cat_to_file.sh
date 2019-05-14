#!/bin/bash

# cat to foo.txt from redirect: cat x | input_cat_to_file.sh
exec >> logs/foo.log
exec 2>&1
cat >> logs/foo.txt
echo "done with foo script"

