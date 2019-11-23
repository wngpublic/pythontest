<?php

# run as php test.php

class Test {
  function testSyntax() {
    $v = null;
    if(is_long($v)) {
      echo "is long\n";
    } else {
      echo "is not long\n";
    }
    $v = "";
    if(is_long($v)) {
      echo "is long\n";
    } else {
      echo "is not long\n";
    }
    $v = "123";
    if(is_long($v)) {
      echo "is long\n";
    } else {
      echo "is not long\n";
    }
    $v = 123;
    if(is_long($v)) {
      echo "is long\n";
    } else {
      echo "is not long\n";
    }

    $v = false;
    if($v) {
      echo "v is true\n";
    } else {
      echo "v is false\n";
    }
    $v = False;
    if($v) {
      echo "v is true\n";
    } else {
      echo "v is false\n";
    }
    $v = true;
    if($v) {
      echo "v is true\n";
    } else {
      echo "v is false\n";
    }
    $v = True;
    if($v) {
      echo "v is true\n";
    } else {
      echo "v is false\n";
    }
    $v = TRUE;
    if($v) {
      echo "v is true\n";
    } else {
      echo "v is false\n";
    }
    $v = "hello";
    if($v) {
      echo "v is true\n";
    } else {
      echo "v is false\n";
    }
    $v = 0;
    if($v) {
      echo "v is true\n";
    } else {
      echo "v is false\n";
    }
    $v = null;
    if($v) {
      echo "v is true\n";
    } else {
      echo "v is false\n";
    }
  }
}

$t = new Test();
$t->testSyntax();
