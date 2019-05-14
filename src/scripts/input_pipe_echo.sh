#!/bin/bash

# cat filename | input_pipe_echo.sh
i=0
while IFS= read -r in; do
  ((i++))
  echo $i " " $in
done
