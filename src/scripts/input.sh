#!/bin/bash

function f1 {
  read -p 'enter number a: ' a
  read -p 'enter number b: ' b
  if [ -z $a ]; then
    echo a $a is empty
    exit
  fi
  if [ -z $b ]; then
    echo b $b is empty
    exit
  fi

  if ! [[ $a =~ ^[0-9]+$ ]]; then
    echo a $a is not number
    exit
  else
    echo a $a is number
  fi
  pat='^[0-9]+$'
  if [[ ! $b =~ $pat ]]; then
    echo b $b is not number
    exit
  else
    echo b $b is number
  fi
  if(($a == $b)); then
    echo $a == $b
  else
    echo $a != $b
  fi
  echo done f1
}

f1
