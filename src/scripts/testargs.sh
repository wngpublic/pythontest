#!/bin/bash

# https://linuxconfig.org/bash-scripting-tutorial-for-beginners
# https://www.shellscript.sh/
# https://www.tldp.org/LDP/Bash-Beginners-Guide/html/index.html
# http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html

if [ $# -eq 0 ]; then
  echo no args
  exit 1
fi
if [ $# -eq 1 ]; then
  # cannot have space, eg v1 = $1 is error
  v1=$1
  if [[ $v1 =~ ^[0-9]+$ ]]; then
    echo $v1 is number
  else
    echo $v1 is not number
  fi
elif [ $# -eq 2 ]; then
  v1=$1
  v2=$2
  if [[ $v1 =~ ^[0-9]+$ ]]; then
    echo $v1 is number
    # (( is arithmetic context
    if (( $v1 % 2 == 0 )); then
      echo $v1 is divisible by 2
    else
      echo $v1 is not divisible by 2
    fi
  else
    echo $v1 is not number
  fi
  if [[ $v2 =~ ^[0-9]+$ ]]; then
    echo $v2 is number
  else
    echo $v2 is not number
    # [[ is non arithmetic context
    if [[ $v2 -eq "hello" ]]; then
      echo $v2 is eq to hello
    fi
    if [[ $v2 -ne "hello" ]]; then
      echo $v2 is ne to hello
    fi
  fi
else
  echo too many args
  exit 1
fi


