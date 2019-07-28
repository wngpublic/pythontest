#!/bin/bash

#!/bin/bash -x

# ./syntax.sh to run
# bash ./syntax.sh to run
# bash -x syntax.sh  to debug

myfunc() {
    cat testtext.txt | grep 30
}

function f1 {
    v1=$1
    v2=$2
    #echo called f1. args are 1:$v1 2:$v2
    if [ -z $1 ]; then
        return 1
    fi
    if [ $1 = "hellospecific" ]; then
        #echo hellospecific is arg1
        return 2
    fi
    return 0
}

# bash does not return value to caller. when bash function ends,
# its return value is only its status
function f2 {
    if [ -z "$1" ]; then
        #echo error: f2 needs arg1
        return 1
    fi
    if [ -z $2 ]; then              # not sure if $2 is same as "$2"
        #echo error: f2 needs arg2
        return 2
    fi
    #echo called f2 args 1:$1 and 2:$2
    return 3
}

function f3 {
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

}

function f3_1 {
    is_echo=0
    if [ $1 == "echo" ]; then
        is_echo=1
    fi
    if [ -z $2 ]; then
       return 4
    fi
    if [ -n $2 ]; then
        if [ $is_echo == 1 ]; then
            return 1
        fi
        return 2
    fi
    return 3
}

# alternative way of expressing function
f3_3() {
    if [ -z $1 ]; then
        return 1
    fi
    if [ $1 == "v10" ]; then
        return 10
    fi
    if [ -z $2 ]; then
        return 2
    fi
    if [ -z $3 ]; then
        return 3
    fi
    return 4
}

# return number of args
f3_4() {
    v=$#
    return $v
}

# return length of string
f3_5() {
    if [ -z $1 ]; then
        return 0
    fi
    v=${#1}
    return $v
}

function f_function_args {
    #echo ================f1
    f1 'hello1' 'hello2'
    if [ $? != 0 ]; then
        echo error code expected $?
    fi
    f1 hello1 hello2
    if [ $? != 0 ]; then
        echo error code expected $?
    fi
    f1 hellospecific
    if [ $? != 2 ]; then
        echo error code expected $?
    fi
    f1  # this should throw error
    if [ $? != 1 ]; then
        echo error code expected $?
    fi

    #echo ================f2
    f2 hi1 hi2
    if [ $? != 3 ]; then
        echo error code expected $?
    fi
    f2 hi   # this should have error
    if [ $? != 2 ]
    then
        echo error code expected $?
    fi

    #echo ================f2 assign function to var

    #result=f2 onearg   # this is illegal syntax
    # this does not call the method, only assigns
    result=$(f2 onearg twoarg threearg)

    #echo echo before call
    #echo echo f4.06 result1 = $result
    $result
    # was expecting $result == 3, but seems like $result is the function, so it's 0
    if [ $? != 0 ]; then
        echo error code expected $?
    fi

    f2 1arg 2arg
    if [ $? != 3 ]; then
        echo error code expected $?
    fi
    # cannot use $? again, gets reset
    if [ $? != 0 ]; then
        echo error code expected $?
    fi

    # $? seems to already got reset, so it's 0
    result=$?
    if [ $? != 0 ]; then
        echo f4.10 error code expected $?
    fi
    if [ $result != 0 ]; then
        echo f4.11 error code expected $result
    fi

    f2 1arg 2arg
    result=$?
    if [ $? != 0 ]; then
        echo f4.12 error code expected $?
    fi
    if [ $result != 3 ]; then
        echo f4.13 error code expected $result
    fi
    # result is preserved, $? is not preserved
    if [ $result != 3 ]; then
        echo f4.13 error code expected $result
    fi

    f3_1 "echo" "something1"
    if [ $? != 1 ]; then
        echo f4.14 error code expected $?
    fi

    f3_1 "echo1" "something2"
    if [ $? != 2 ]; then
        echo f4.15 error code expected $?
    fi

    f3_1 "some1" "something3"
    if [ $? != 2 ]; then
        echo f4.16 error code expected $?
    fi

    f3_1 "some1"
    if [ $? != 4 ]; then
        echo f4.17 error code expected $?
    fi

    f3_3 "v1" "v2"
    if [ $? != 3 ]; then
        echo f4.18 error code expected $?
    fi

    f3_3 v1 v2
    if [ $? != 3 ]; then
        echo f4.19 error code expected $?
    fi

    # do quotes matter? nope
    f3_3 v10 v2
    if [ $? != 10 ]; then
        echo f4.20 error code expected $?
    fi

    # do quotes matter? nope
    f3_3 "v10" v2
    if [ $? != 10 ]; then
        echo f4.21 error code expected $?
    fi

    # returns number of args
    f3_4
    if [ $? != 0 ]; then
        echo f4.22 error code expected $?
    fi
    f3_4 v1 v2 v3
    if [ $? != 3 ]; then
        echo f4.22 error code expected $?
    fi

    # returns string length
    f3_5 v1234
    if [ $? != 5 ]; then
        echo f4.23 error code expected $?
    fi

    echo f4 done
}

function f5 {

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

}

f_print_date_var() {
    v=var-$(date +%m-%d-%Y)
    echo $v
    echo $(date)
}

f_command_captures() {
    v=`ls -l`

    # no quote puts output into one line
    #echo $v

    # quote puts output into multi line
    #echo "$v"

    # string length
    #echo ${#v}

}


my_contains() {
    numargs=$#
    if [ $numargs != 2 ]; then echo contains needs 2 args, has $# args; return 0; fi
    k=$1
    a=$2
    for v in ${a[@]}; do
        if [ $k == $v ]; then
            #echo found key $k
            return 1;
        fi
    done
    #echo not found key $k
    return 0
}

is_valid_date() {
    input=$1
    cmd=$(date -j -f %d-%m-%Y $input +%s 2>1)
    return $?
}

f_list_string_manip() {
    v1="abc  "
    # this gets trimmed
    if [ $v1 != "abc" ]; then
        echo p1 mismatch $v1
    fi

    v1='abc  '
    # this gets trimmed
    if [ $v1 != 'abc' ]; then
        echo p2 mismatch $v1
    fi
    # same as $v1
    if [ ${v1} != 'abc' ]; then
        echo p2 mismatch $v1
    fi

    if [ "abc" != 'abc' ]; then
        echo p3 mismatch abc
    fi

    if [ "abc " = 'abc' ]; then
        echo p4 mismatch abc
    fi

    # string concatenation
    v1="abc"
    v2=$v1
    v2+="def"
    if [ $v2 != "abcdef" ]; then
        echo p5 mismatch $v2
    fi

    # splitting into tokens
    v1="a1 a2 a3 a4"
    ctr=0
    for v in $v1; do
        ((ctr++))
    done
    if [ $ctr != 4 ]; then
        echo p6 mismatch $ctr
    fi

    v=0
    v1=5
    if (( $v1 < 3 )) ; then
        v=3
    elif (( $v1 < 6 )) ; then
        v=1
    else
        v=4
    fi
    if [ $v != 1 ]; then
        echo p7 mismatch $v
    fi
    if (( $v != 1 )); then
        echo p8 mismatch $v
    fi

    # substitute digits
    v=234abcdefghijklmn123
    v1=`echo $v | sed -E s!\[0-9]+!!g`
    if [ $v1 != abcdefghijklmn ]; then
        echo p9 mismatch $v1
    fi

    v1=`echo $v | sed s!2!1!g`
    if [ $v1 != 134abcdefghijklmn113 ]; then
        echo p10 mismatch $v1
    fi

    # list and set operations
    a=(v1 v2 v3)
    a+=(v4 v5 v6)
    b=(v6 v5 v4 v3 v2 v1)
    c=(v3 v1 v6 v4 v5 v2)
    d=( "v1a v1b1" v2 v3 "v4a v4b" )

    if [ ${#d[@]} != 4 ]; then echo p20 mismatch ${#d[@]}; fi
    if [ ${#d[*]} != 4 ]; then echo p21 mismatch ${#d[@]}; fi
    if [ ${#d} != 8 ]; then echo p22 length of first var in array mismatch ${#d}; fi
    if [ ${#d[0]} != 8 ]; then echo p22 length of first var in array mismatch ${#d[0]}; fi

    # how to check if element is in array? must iterate through loop, or put in function

    # how to check if two arrays are the same?
    #echo $(sort ${a[@]}) $(sort ${b[@]})
    #echo $(sort ${a[@]})

    #echo v1 ${c[@]}        # same
    #echo v2 ${c[*]}        # same
    v=$(echo "${c[*]}" | sort) # sort doesn't work for single line
    a_new=()
    for v in ${a[@]}; do
        a_new+="$v"
        a_new+="\n"
    done
    #echo ${a_new[@]}
    # this works for sort
    v=$(echo "${c[*]}" | tr " " "\n" | sort)
    #echo ${v[@]}

    #echo ============
    aa=()
    aa+=(v1 v2 v3)
    aa+=(v4 v5 v6)
    #for k in "${!aa[@]}"; do echo $k; done # this prints indices 0-$#
    #for v in "${aa[@]}"; do echo $v; done  # this prints values
    if [ ${aa[0]} != v1 ]; then echo mismatch p20 ${aa[0]}; fi
    if [ ${aa[3]} != v4 ]; then echo mismatch p20 ${aa[3]}; fi

    #result=$(my_contains v5 "${aa[*]}")    # this does not work, use $? instead
    my_contains v5 "${aa[*]}"
    result=$?
    if [ $result == 0 ]; then echo mismatch p21 $result; fi
    my_contains v9 "${aa[*]}"
    result=$?
    if [ $result != 0 ]; then echo mismatch p22 $result; fi
    #echo ============

    # string substitution
    a=abcdefg
    b=${a/bcd/123}
    if [ $b != a123efg ]; then echo mismatch p23 $b; fi

    # associative arrays are only in v4+
    # only arrays available before v4
    #echo BASH_VERSION:"${BASH_VERSION}"
    #echo ============
    #kv=()
    #declare -A kv
    #kv[k1]+=v1
    #kv[k2]+=v2
    #kv[k3]+=v3
    #for k in "${!kv[@]}"; do echo $k; done
    #for v in "${kv[@]}"; do echo $v; done
    #echo ============

    # this tests for existence in array/set
    #echo a:${a[*]}
    #echo a:${a[v1]}
    ctr=0
    #if [[ ${a["v1"]} ]]; then (($ctr++)); fi
    #echo $ctr

    #v2=${v[a]}
    #echo $v2

    #if [[ $v2 == "1 2 3 4 5 6" ]]; then echo expected value $v2; fi

    #echo $v
    #echo ${v[*]}
    #echo $(echo ${c[@]} | sort)
    #result=`diff $(sort ${a[@]}) $(sort ${b[@]})`
    # wont work because sort is line based, need tr to replace space with newline
    #echo p13 $result
    #if [[  ]]; then
    #    echo p13 mismatch
    #fi
    #if [[ 3 == ${a[@]} ]]; then
    #    echo p12 mismatch "$a"
    #fi
    #echo ${a[@]}
    #if [ $a != $b ]; then
    #    echo p11 mismach ${a[@]}
    #fi
    #echo $a

    a1=(1 2 3)
    # do newline separator
    b=$(IFS=$'\n'; echo "${a1[*]}") # the upper indices are still populated with previous data for $b!!
    b1=$(IFS=$'\n'; echo "${a1[*]}")
    #echo "${b[@]}"
    #echo "${b1[@]}"
    #echo ${b1[@]}
    result=$(printf "%s " "${a1[@]}")
    result=$(IFS= ; echo "${a1[@]}")
    if [[ "${#a1[@]}" != 3 ]]; then echo mismatch size of array "${#a1[@]}"; fi
    if [[ $result != "1 2 3" ]]; then echo mismatch q1 $result; fi

    # pattern matching DD-MM-YYYY
    pattern="^[0-9]{2}-[0-9]{2}-[0-9]{4}$"
    if [[ ! "11-22-3333"  =~ $pattern ]]; then echo mismatch q2 "11-22-3333"; exit 1; fi
    if [[   "11-22-33333" =~ $pattern ]]; then echo mismatch q3 "11-22-33333"; exit 1; fi
    if [[   "11-22--3333" =~ $pattern ]]; then echo mismatch q4 "11-22--3333"; exit 1; fi
    if [[   "11-22-33"    =~ $pattern ]]; then echo mismatch q5 "11-22-33"; exit 1; fi

    input=""
    #cmd=$(date -j -f %d-%m-%Y $input +%s 2>1)
    #val=$(date -j -f %d-%m-%Y $input +%s 2>1)
    cmd="date -j -f %d-%m-%Y $input +%s 2>1"
    eval $cmd # cannot replace $input each time you call, so use function

    input="10-12-2000"
    is_valid_date $input
    if [ $? != 0 ]; then echo $input is not valid date.; exit 1; fi

    input="11-22-3333"
    is_valid_date $input
    if [ $? == 0 ]; then echo $input is not valid date.; exit 1; fi

    input="11-22-2000"
    is_valid_date $input
    if [[ $? == 0 ]]; then echo $input is not valid date.; exit 1; fi

    input="22-11-2000"
    is_valid_date $input
    if [[ $? != 0 ]]; then echo $input is not valid date.; exit 1; fi

    input="11-22-18"
    is_valid_date $input
    if [[ $? == 0 ]]; then echo $input is not valid date.; exit 1; fi

    input="22-08-18"
    is_valid_date $input
    if [[ $? == 0 ]]; then echo $input is not valid date.; exit 1; fi

    if [[ "$OSTYPE" != "darwin"* ]]; then echo mismatch q6 $OSTYPE; exit 1; fi
    if [[ "$OSTYPE" == "linux"* ]]; then echo mismatch q7 $OSTYPE; exit 1; fi

    # urlencoding

    val="[ab,cd] and abc=def;"
    out=""
    #for (( i=0; i<${#val}; i++ )); do
      #c="${val:$i:1}"
      #if [ $c in  ]; then
      #  out+=
      #else
      #  out+=$c
      #fi
    #done

    echo done f_string_manip
}

test_read_file() {
    filei=data.in.4.txt
    #k01 ip01 mval
    #k02 ip02 mval
    #k03 ip03 mval

    if [ -f $filei ]; then
        v=$(cat $filei)
        ctr=0
        for l in ${v[@]}; do
            (( ctr++ ))
            #echo $l
        done
        if [ $ctr != 9 ]; then
            echo test_read_file 1 mismatch $ctr
        fi
        ctr=0
        for l in ${v}; do
            (( ctr++ ))
            #echo $l
        done
        if [ $ctr != 9 ]; then
            echo test_read_file 2 mismatch $ctr
        fi
        ctr=0
        for l in $v; do
            (( ctr++ ))
            #echo $l
        done
        if [ $ctr != 9 ]; then
            echo test_read_file 3 mismatch $ctr
        fi

        if [ ${#v} != 41 ]; then
            echo test_read_file 4 string length mismatch ${#v}
        fi

        #k01 ip01 mval
        #k02 ip02 mval
        #k03 ip03 mval

        if [ ${v:4:1} != i ]; then
            echo test_read_file expected letter i
        fi
        if [ ${v:5:1} != p ]; then
            echo test_read_file expected letter p
        fi
        if [ ${v:6:2} != 01 ]; then
            echo test_read_file expected substring 01
        fi
        if [ ${v:9:4} != mval ]; then
            echo test_read_file expected substring mval
        fi
        # syntax error if single bracket for compound if statement
        if [[ ${v:14:3} != "k02" || ${v:14:3} != k02 ]]; then
            echo test_read_file expected substring k02
        fi

        # cannot figure how to split by newline. below is non working
        # use IFS internal field separator to split by newline
        #IFS='\n' read -ra array <<< "$v"
        #for token in "${array[@]}"; do
        #    echo $token
        #done
        #IFS='\n';array=($v);unset IFS;

        ##array=(${v//\n/})
        #for token in "${array}"; do
        #    echo 1 $token
        #done

        # prints each line
        #echo "$v"

        #echo -e 1 '\n'"${v[*]}"     # prints the newline and all the data
        #echo 1 '\n'"${v[*]}"        # prints \n and all the data
        #echo -e 2 '\n'"${#v[*]}"    # not sure what this is
        #echo -e 3 '\n'"${v[0]}"     # prints all the data
        #echo -e 4 '\n'"${v[1]}"     # prints nothing

    fi
    echo done test_read_file
}

test_math() {
    v1=5
    v2=4

    # this is string concat
    v3=$v1+$v2
    if [ $v3 != "5+4" ]; then
        echo test_math 1 mismatch $v3
    fi

    # this is math op
    let v3=$v1+$v2
    if [ $v3 != 9 ]; then
        echo test_math 2 mismatch $v3
    fi

    echo test_math done
}

test_read_cmdline_input() {
    # input from stdin example
    echo ============================
    echo "type single word: "
    read a
    echo "you typed $a"
    echo ============================
    echo "type three words: "
    read a b c
    echo "you typed $a,$b,$c"
    echo ============================
}

print_cmdline_args() {
    #in=$@
    #echo in: $in
    #echo numargs $# : $@
    #echo numargs $BASH_ARGC : $BASH_ARGV
    if [ $# != 0 ]; then
        echo args != 0: $0: $@
    elif [ $# == 0 ]; then
        echo args == 0: $0: $@
    fi
}

test_print_cmdline_args() {
    print_cmdline_args $@
    print_cmdline_args
}

function mainfunction {
    #test_print_cmdline_args $@
    #f_function_args
    f_list_string_manip
    #test_read_file
    #test_math
    #f_command_captures
    #test_read_cmdline_input
}

mainfunction $@
