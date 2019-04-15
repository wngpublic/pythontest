#!/bin/bash

echo "#######################"
file="files/input2.txt"
if [ ! -f $file ]; then
  echo $file does not exit
  exit
fi
while IFS= read line
do
  echo $line
done < $file

# now read the directory and capture
echo "#######################"
base='files'
a=$(ls $base)
newarray=()
for f in ${a[@]}; do
  ls -l $base/$f
  #v=$(ls -l $f)
  #newarray+=($v)
done
for v in ${newarray}; do
  echo $v
done
echo "#######################"



