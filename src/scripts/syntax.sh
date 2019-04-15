#!/bin/bash

# ./syntax.sh to run
# bash -x syntax.sh  to debug

myfunc() {
  cat testtext.txt | grep 30
}

function f1 {
  v1=$1
  v2=$2
  echo called f1. args are 1:$v1 2:$v2
  if [ $1 = "hellospecific" ]; then
    echo hellospecific is arg1
  fi
}

function f2 {
  if [ -z "$1" ]; then
    echo error: f2 needs arg1
    return
  fi
  if [ -z $2 ]; then              # not sure if $2 is same as "$2"
    echo error: f2 needs arg2
    return
  fi
  echo called f2 args $1 and $2
}

for i in {1..5}
do
  echo "a:" $i
done

ctr=0                  # ctr = 0 is error

for ((i=0; i<=5; i++))
do
  echo "b:" $i

  if (($i == 1))
  then                  # this must be in separate line
    ctr=$((ctr+1))
  fi

  if (($i == 0)); then
    ((ctr+=1))
  fi

  if [ $i -eq 1 ]; then
    ((ctr+=1))
  fi

  if (($i == 2))
  then
    ((ctr+=1))         #<-- must have ((x+=1)), not x+=1, not $ctr1+=1
  fi

  if (($i == 3)) 
  then
    ((ctr++))          # no $var+=1, var+=1 ok, also, ctr++ doesnt work
    break
  fi
done

echo "ctr " $ctr ". expected 5"

if [ 1 -eq 1 ]; then
  ctr=1
else
  ctr=0
fi

if [ 1 -lt 2 ]; then
  ((ctr++))
fi


echo $ctr
echo ================1
cmd=$(cat testtext.txt | grep 2)
echo ================1output
echo ${cmd[*]}                          # how to print with newline??
echo ================1outputnewline
echo "${cmd[*]}"                        # this is how
echo ================1outputbad         # prints each token, not newline
#for v in ${cmd[@]}; do
#  echo $v
#done

echo ================2
cmd='cat testtext.txt | grep 20'        # cannot do $cmd, have to do eval $cmd
eval $cmd

echo ================3
myfunc

echo ================4
#cmd="cat testtext.txt \| grep 20"        # cannot do $cmd, have to do eval $cmd
cmd="cat testtext.txt"
$cmd

echo ================5
cat testtext.txt | grep 20

echo ================f1
f1 'hello1' 'hello2'
f1 hello1 hello2
f1 hellospecific

echo ================f2
f2 hi1 hi2
f2 hi

echo ================array
a=(a b c)
for v in ${a[@]}; do
  echo $v
done

echo ================array
a=('a 1' 'b 2' 'c 3')
#a=("a 1" "b 2" "c 3")            # " and ' seems to make no difference for regular strings

printf "%s\n" "${a[@]}"           # separate line for each quoted value
echo ================array
printf "%s\n" "${a[*]}"           # expands out as single line
echo ================array
echo num elements ${#a[*]}
echo num elements ${#a[@]}
echo num elements ${!a[*]}        # all of the index values, 0 1 2
echo elements val ${#a[1]}        # i dont know what this is

echo ================array
for v in ${a[@]}; do
  #echo $v                         # this is wrong! prints a 1 b 2 c 3 in separate lines
  echo "$v"                        # this is also wrong, prints a 1 b 2 c 3 in separate lines
  printf "%s\n" "$v"
done

echo ================forloop
ctr=0
for i in 1 2 3; do
  ((ctr+=1))
done
echo $ctr

echo ================forloop
a=(10 11 12)
ctr=0
#for i in ${#a[@]}; do              # err: i is always 3 because this is size
for i in ${!a[*]}; do               # this is index
  ((ctr+=${a[$i]}))
done
echo $ctr

echo ================stringtest
v="test1"
for v in 'test1' 'test2' 'test3'; do  # (test1 test2 test3) is wrong, no (
  if [ $v = "test2" ]; then           # must have spaces for if [ 
    echo "P1: test2"
  elif [ $v = "test1" ]; then         # = is equal, -eq should be integer, -eq is error
    echo "P2: test1"
  else
    echo "not recognized $v"
  fi
done

echo ================inttest
for v in 1 2 3 4; do
  if [ $v -eq 1 ]; then
    echo "1 is $v"
  elif [ $v -eq 2 ]; then
    echo "2 is $v"
  else
    echo "other is $v"
  fi
  if (($v%2==0)) && (($v%4==0)); then
    echo "mod test ok for $v"
  fi
done


echo ================none
echo done
