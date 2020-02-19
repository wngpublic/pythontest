<?php

# run as php test.php

class Test {
    public $dbg = true;
    public $dbglvl = 5;
    public $dbg_lvl_end = 10;

    function pout($log_level, $msg) {
        echo $msg;
    }

    function dbg($msg, $dbglvl=0, $returnmsg=false) {
        if(!$this->dbg) return;
        if($dbglvl < $this->dbglvl) return;
        if($returnmsg) return $msg;
        echo $msg . "\n";
    }

    function test_ranges() {
        $a0 = array();
        for($i = 0; $i < 10; $i++) {
            $s = "val:".$i;
            array_push($a0, $s);
        }
        $ctr = 0;
        foreach($a0 as $v) {
            $ctr++;
        }
        assert($ctr == 10);
        $v1 = "123abc456";
        $v2 = "123-abc-456";
        assert(!preg_match("/-abc-/",$v1));
        assert(preg_match("/abc/",$v1));
        assert(preg_match("/-abc-/",$v2));
        assert(preg_match("/abc/",$v2));

        $this->dbg("test_ranges",$this->dbg_lvl_end);
    }

    function test_structures() {
        $a0 = array();
        assert($a0 == null);
        assert(count($a0) == 0);
        array_push($a0, 1);
        array_push($a0, 2);
        assert(count($a0) == 2);
        assert($a0 != null);
        assert(count(null) == 0);

        assert(is_array($a0));
        assert(!is_array("not"));
        $a1 = null;
        assert(!isset($a1));
        $a1 = array();
        assert(isset($a1));
        array_push($a1, 1);
        assert(isset($a1));
        assert(count($a1) == 1);
        unset($a1);
        assert(count($a1) == 0);

        $a = array();
        assert(count($a) == 0);
        $a["k1"]="v1";
        $a["k2"]="v2";
        $a["k3"]="v3";
        assert(count($a) == 3);
        $lk = array();
        $lv = array();
        foreach($a as $k=>$v) {
            array_push($lk,$k);
            array_push($lv,$v);
        }
        assert(count($lk) == 3);
        assert(count($lk) == count($lv));
        assert(array_key_exists("k1",$a));
        assert(array_key_exists('k1',$a));
        assert(in_array('k1',$lk));
        assert(in_array("k1",$lk));
        assert(!array_key_exists("k1",$lk));
        assert(in_array("v1",$lv));
        assert(!array_key_exists("v1",$lv));

        $l = array();
        foreach($lk as $k) {
            array_push($l,$k);
        }

        assert(count($l) == 3);
        assert(count(array_diff($lk,$l)) == 0);

        $a1 = [1,2,3,4,5];
        $a2 = [2,3,4,5,6];
        $a3 = array_diff($a1,$a2);  // returns only values in a1 not in a2
        assert(count($a3) == 1);
        assert(in_array(1,$a3));
        $a3 = array_diff($a2,$a1);  // returns only values in a2 not in a1
        assert(count($a3) == 1);
        assert(in_array(6,$a3));

        $a1 = [1,2,3,4,5];
        $a2 = [2,3,4];
        $a3 = array_diff($a1,$a2);
        assert(count(array_diff($a3,[1,5])) == 0);
        assert(count(array_diff($a3,[5,1])) == 0);  // ordering doesnt matter

        assert([1,2,3] == [1,2,3]);
        assert([1,2,3] != [2,1,3]);
        assert([1,2,3] === [1,2,3]);
        assert([1,2,3] !== [2,1,3]);
        assert(count(array_diff([1,2,3],[2,1,3])) == 0);
        $a1 = [1,2,3];
        $a2 = [2,1,3];
        assert($a1 != $a2);

        $a1 = [2,3,4];
        $a2 = [1,2,3,4,5];
        $a3 = array_diff($a1,$a2);
        assert(count($a3) == 0);

        $a1 = [
            'k1'=>'v1',
            'k2'=>'v2',
            'k3'=>'v3'
        ];
        assert(count($a1) == 3);
        assert(array_key_exists('k1',$a1));

        $a1 = [
            k1=>'v1',
            k2=>'v2',
            k3=>'v3'
        ];
        assert(count($a1) == 3);
        assert(array_key_exists('k1',$a1));
        assert(!array_key_exists('k10',$a1));

        $this->dbg("test_structures",$this->dbg_lvl_end);
    }

    function test_strings() {
        assert(strcmp("A/B/c","A/B/c") == 0);
        assert(strcmp("A/B/c","A/B/C") != 0);
        assert(strcmp("A/B/c","A/B/c ") != 0);

        assert(strlen("abc") == 3);
        assert(strlen("a/b/c") == 5);
        assert(strlen("a/b/c \n ") == 8);

        assert(strtolower("A/B/c") == "a/b/c");

        assert("aCb" != "abc");
        assert("abc" == "abc");
        assert("abc" != "abC");

        $l = explode(" ","the cat in the hat");
        assert($l == ["the","cat","in","the","hat"]);

        $l = explode(" ","  the  cat  in   the hat");
        assert($l == ["","","the","","cat","","in","","","the","hat"]);

        $l = preg_split("/\s+/","  the  cat  in   the hat");
        assert($l == ["","the","cat","in","the","hat"]);
        assert($l[1] == "the");

        $l = preg_split("/\s+/","the  cat  in   the hat");
        assert($l == ["the","cat","in","the","hat"]);
        assert($l[0] == "the");
        $s = implode(" ",$l);
        assert($s == "the cat in the hat");

        preg_match("/cat/",$s,$res);
        assert(is_array($res));
        assert(count($res) == 1);
        assert($res == ['cat']);

        preg_match("/\w+/",$s,$res);
        assert(is_array($res));
        assert(count($res) == 1);
        assert($res == ['the']);    // only first match

        preg_match_all("/\w+/",$s,$res);
        assert(is_array($res));
        assert(count($res[0]) == 5);
        assert($res == [["the","cat","in","the","hat"]]); // all matches

        $this->dbg("test_strings",$this->dbg_lvl_end);
    }

    function test_syntax() {
        assert(!is_long(null));
        assert(!is_long(""));
        assert(!is_long("123"));
        assert(is_long(123));
        $v = false;
        assert(!$v);
        $v = False;
        assert(!$v);
        $v = true;
        assert($v);
        $v = True;
        assert($v);
        $v = TRUE;
        assert($v);
        assert("hello");
        assert(!0);
        assert(1);
        $v = null;
        assert($v == null);
        assert(!$v);

        $this->dbg("hello\n");
        assert($this->dbg("hello1\n",5,true) == "hello1\n");

        $this->dbg("test_syntax",$this->dbg_lvl_end);
    }
}

openlog("mylog.php.log", LOG_CONS, LOG_USER);
$t = new Test();
$t->test_ranges();
$t->test_syntax();
$t->test_structures();
$t->test_strings();
closelog();

?>
