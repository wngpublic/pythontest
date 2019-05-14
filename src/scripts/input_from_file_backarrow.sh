#!/bin/bash

# input_from_file_backarrow.sh < file
i=0
while IFS= read -r in; do
  ((i++))
  echo $i " " $in
done

