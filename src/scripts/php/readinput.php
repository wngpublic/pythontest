<?php

assert_options(ASSERT_BAIL, 1); // exit if fail assert
date_default_timezone_set('America/Los_Angeles');

function test_hello_world($argv) {  // pass array by copy
    $_ARG = array();
    // php -f readinput.php a b "c d e f"
    print "hello world\n";
    if($argv) {
      $i=0;
      foreach($argv as $arg) {
        print "$i: $arg\n";
        $i++;
        //var_dump($arg);
      }

    }
}

function test_assert() {
    $v = 1;
    assert($v == 1);
    //assert($v == 2);
}

function test_args_by_reference_and_copy_priv($a1, &$a2, $v1, &$v2) {
    // arrays are assigned by copy, while objects are assigned by reference
    assert(count($a1) == 3);
    assert(count($a2) == 3);
    $a1[0]='v1a';
    $a2[0]='v1a';
    $v1++;
    $v2++;
}

function test_args_by_copy_priv_return($a1) {
    return $a1;
}

function test_args_by_ref_priv_return(&$a1) {
    return $a1;
}

function &test_args_by_ref_priv_return_1(&$a1) {
    return $a1;
}

function test_args_and_return_1() {
    return array (1,2,3);
}

function test_args_by_reference_and_copy_arrays($token_in=0) {
    $a1 = array('v1','v2','v3');
    $a2 = array('v1','v2','v3');
    $v1 = 1;
    $v2 = 1;
    $v3 = NULL;
    $v4;

    test_args_by_reference_and_copy_priv($a1, $a2, $v1, $v2);
    assert($a1[0] == 'v1');
    assert($a1[1] == 'v2');
    assert($a1[2] == 'v3');

    assert($a2[0] == 'v1a');
    assert($a2[1] == 'v2');
    assert($a2[2] == 'v3');

    // test reference vs copy
    assert($v1 == 1);
    assert($v2 == 2);

    // test return values, modify return value and compare with original
    assert(count($a1) == 3);
    $a3 = test_args_by_copy_priv_return($a1);
    array_push($a3,'v4');
    assert(count($a1) == 3);
    assert(count($a3) == 4);

    assert(count($a1) == 3);
    $a3 = test_args_by_ref_priv_return($a1);
    array_push($a3,'v4');
    assert(count($a1) == 3);
    assert(count($a3) == 4);

    $a3 = &test_args_by_ref_priv_return_1($a1);
    array_push($a1,'v4');
    assert(count($a1) == 4);
    assert(count($a3) == 4);
    array_push($a3,'v5');
    assert(count($a1) == 5);
    assert(count($a3) == 5);

    // assignment of array to vars
    list ($v0, $v1) = test_args_and_return_1();
    assert($v0 == 1 && $v2 == 2);

    $a = test_args_and_return_1();
    assert(count($a) == 3);
    assert($a[0] == 1 && $a[1] == 2 && $a[2] == 3);

    return $token_in;
}

function test_arrays($token_in=0) {
    $a1 = array('v1','v2','v3');
    assert(count($a1) == 3);
    array_push($a1, 'v4','v5');
    assert(count($a1) == 5);
    $a1[] = 'v6';   # append
    $a1[] = 'v7';
    assert(count($a1) == 7);

    $a1 = array('v1','v2','v3');
    $a2 = array('v1','v2','v3');
    $v1 = 1;
    $v2 = 1;
    $v3 = NULL;
    $v4;

    assert(is_array($a1));
    assert(!is_array($v1));
    assert($v3 == NULL && empty($v3));
    assert($v4 == NULL);

    $a4 = array();
    assert(is_array($a4) && empty($a4));

    // assign by copy vs assign by reference
    $a6 = array('v1','v2','v3');
    $a3 = $a6; // by copy
    $a5 = &$a6; // by reference
    assert(count($a3) == 3);
    assert(count($a5) == 3);
    assert(count($a6) == 3);
    array_push($a6,'x1');
    assert(count($a6) == 4);
    assert(count($a3) == 3);
    assert(count($a5) == 4);

    assert(count($a1) == 3);
    assert($a1[0] == 'v1');
    assert($a1[1] == 'v2');
    assert($a1[2] == 'v3');

    // append and test unset/pop
    array_push($a1, 'v4','v5');
    $cnt = 0;
    for( $i = 0; $i < count($a1); $i++ ){
        //print("$a1[$i]\n");
        $cnt++;
    }
    assert($cnt == 5);

    array_pop($a1);
    unset($a1[3]);
    assert(count($a1) == 3);


    $a1 = array('v1','v2','v3');
    list($va1,$va2,$va3)=$a1;
    assert($va1 == 'v1');
    assert($va2 == 'v2');
    assert($va3 == 'v3');

    // array assignments
    $a1 = array(
        'x1'=>'v1',
        'x2'=>'v2',
        'x3'=>'v3'
    );
    assert($a1['x2'] == 'v2');
    $a1['x4']='v4';
    assert(count($a1) == 4);
    $cnt = 0;
    $a1 = array(
        'x1'=>1,
        'x2'=>2,
        'x3'=>3
    );
    $a1['x4']=4;
    $vk="";
    $vv=0;
    foreach($a1 as $x=>$y) {
        $vk=$vk.$x;
        $vv+=$y;
        $cnt++;
    }
    assert($vk == "x1x2x3x4");
    assert($vv == 10);
    assert($cnt == 4);
    assert(count($a1) == 4);
    unset($a1['x4']);
    assert(count($a1) == 3);

    $a1 = array('v1','v2','v3');
    $a2 = array('v1','v2','v3');
    assert($a1 == $a2);
    $a2 = array('v1','v2','va');
    assert($a1 != $a2);
    $a3 = $a2 + $a1;    // different from $a1 + $a2

    $a1 = array('v1','v2','v3');

    $vk = "";
    for($i=0; $i < count($a1); $i++){
      $vk = $vk.$a1[$i];
    }
    assert($vk == "v1v2v3");

    $vk = "";
    foreach($a1 as $v){
      $vk = $vk.$v;
    }
    assert($vk == "v1v2v3");

    $a1 = array(
        'k1'=>array(1,2,3),
        'k2'=>array(4,5,6,7),
        'k3'=>array(8,9,10,11,12)
    );
    assert(count($a1) == 3);
    assert(count($a1['k1']) == 3);
    assert(count($a1['k2']) == 4);
    assert(count($a1['k3']) == 5);

    $a1 = array(
        'k 1'=>0,
        'k 2'=>0,
        'k 3'=>0
    );

    assert(!isset($a1['k 4']));
    assert($a1['k 4'] == null);
    assert($a1['k 4'] == 0);
    $a1['k 4']=1;
    assert($a1['k 4'] != null);

    assert(isset($a1['k 2']));
    assert($a1['k 2'] == 0);
    assert($a1['k 2'] == null);

    $a1['k 2']++;
    $a1['k 2']++;
    assert($a1['k 2'] == 2);

    return $token_in;
}


function test_strings($token_in=0) {
    $v1='abc';
    $v2='defg';
    $v3=$v1.$v2;
    assert($v1 == 'abc' && $v2 == 'defg');
    assert($v1 != 'ab');
    assert(strlen($v3) == 7);
    // TR F seems to all be 1
    assert(is_string($v3) && is_string($v3) == true && is_string($v3) == TR && is_string($v3) == F);
    $v4='path?q="a1:v1&a2:v2 AND v3&v4:[v4a,v4b]"';
    $v5=urlencode($v4);
    $v6=urldecode($v5);
    assert($v5 == 'path%3Fq%3D%22a1%3Av1%26a2%3Av2+AND+v3%26v4%3A%5Bv4a%2Cv4b%5D%22');
    assert($v4 == $v6);

    $v7='the cat in the cat hat';
    $v8=str_replace('cat','bat',$v7);
    assert($v8 == 'the bat in the bat hat');
    $v8=preg_replace("/cat/","bat",$v7);
    assert($v8 == 'the bat in the bat hat');
    //print_r($v8 . "\n");
    $v7='the cat in the  cat  hat';
    $a1=preg_split("/\s+/",$v7);
    //print_r($a1); // print human readable of array
    assert(count($a1) == 6);
    assert($a1[5] == 'hat');
    $v7='the  hat  cat in   the cat hat';
    assert(!preg_match("/dog/",$v7));
    assert(preg_match("/cat/",$v7));
    assert(preg_match_all("/cat/",$v7));
    assert(!preg_match("/cat$/",$v7));
    assert(preg_match("/ hat$/",$v7));
    assert(preg_match("/^the\s+\w+\s+\w+\s+\w+\s+\w+\s+\w+\s+hat$/",$v7));
    assert(!preg_match("/^the\s\w+\s+\w+\s+\w+\s+\w+\s+\w+\s+hat$/",$v7));
    assert(preg_match("/^the[\w\s]+\s+hat$/",$v7));
    $v8=preg_replace("/\s+/"," ",$v7);
    assert($v8 == "the hat cat in the cat hat");
    assert(strlen($v8) == 26);

    $v1="hello there";
    $a=str_split($v1);
    $v2="";
    $cnt=0;
    foreach($a as $v) {
        $cnt++;
        $v2=$v2.$v;
    }
    assert($cnt == 11);
    assert($v1 == $v2);

    $v2="";
    $cnt=0;
    for($i=0; $i < strlen($v1); $i++) {
      $v2=$v2.$v1[$i];
      $cnt++;
    }
    assert($cnt == 11);
    assert($v1 == $v2);

    assert(substr("hello there",0,5) == "hello");
    assert(substr("hello there",6,5) == "there");

    return $token_in;
}

function test_math($token_in=0) {
    $v1 = 5.5;
    $v2 = 2.1;
    $v3 = $v1 + $v2;
    assert($v3 == 7.6);

    return $token_in;
}

function test_time($token_in=0) {
    // manual/en/timezones.america.php
    // manual/en/function.date.php
    date_default_timezone_set('America/Los_Angeles');
    $vdatestr='2019-07-01 13:14:15';
    $vdate=date_create($vdatestr);
    $v1=date_format($vdate,'d-m-Y s:i:H');
    assert($v1 == '01-07-2019 15:14:13');
    $v1=date_format($vdate,'d-m-Y');
    assert($v1 == '01-07-2019');

    return $token_in;
}

function test_json($token_in=0) {
    //$v1 = '{"a1":"v1","a2":"v2","a3":["v3a","v3b","v3c"],"a4":{"a4a":"v4a","a4b":"v4b"},"a5":["a5a"=>"v5a","a5b"=>"v5b"]}';
    $v1 = '{"a1":"v1","a2":"v2","a3":["v3a","v3b","v3c"],"a4":{"a4a":"v4a","a4b":"v4b"}}';
    $json = json_decode($v1);
    assert($json->{"a1"} == "v1");
    assert($json->{"a1"} != "v2");
    assert($json->{"a4"}->{"a4a"} == "v4a");
    assert($json->{"bad"} == null);
    assert($json->{"bad"} == NULL);
    assert($json->{"a2"} != null);
    assert($json->{"a3"} != null && is_array($json->{"a3"}));
    assert(count($json->{"a3"}) == 3);
    assert(count($json->{"a4"}) == 1);

    $a1 = array(
        "a1"=>"v1",
        "a2"=>"v2",
        "a3"=>["v3a","v3b","v3c"],
        "a4"=>array(
            "a4a"=>"v4a",
            "a4b"=>"v4b"
        )
    );
    $a1_str = json_encode($a1);
    //print($a1_str . "\n");
    assert($a1_str == $v1);

    return $token_in;
}

function test_readfile() {

}

function test_date_to_epoch($in_date) {
    $date = new DateTime($in_date);
    if($date != null) {
      return $date->format('U');
    }
    return 0;
}

function test_date($token_in=0) {
    $s=test_date_to_epoch('2019/07/01 12:00:00');
    $d=new DateTime("@$s");
    $vdate=$d->format('m/d/Y H:i:s');
    assert($s == 1562007600);
    assert($vdate == '07/01/2019 19:00:00');

    $s=test_date_to_epoch('07/01/2019 12:00:00');
    $d=new DateTime("@$s");
    $vdate=$d->format('m/d/Y H:i:s');
    assert($s == 1562007600);
    assert($vdate == '07/01/2019 19:00:00');

    //print("s:$s\ndate:$vdate\n");
    //print("date: ". test_date_to_epoch('201907/01') . "\n");

    return $token_in;
}


function main_test(&$argv) {    // pass array by reference
    //test_args_and_returns();
    //test_hello_world($argv);
    //test_assert();
    //test_args_by_reference_and_copy_arrays();
    # this is shell style comment line
    $cnt=0;

    $cnt += test_strings(1); # shell comment style
    $cnt += test_json(1);    // c comment style
    $cnt += test_math(1);
    $cnt += test_time(1);
    $cnt += test_arrays(1);
    $cnt += test_date(1);


    if($cnt == 6) {
      print("passed main_test");
    }
}

main_test($argv);

?>

