<?php

# run as php test.php

class Test {
    public $dbg = true;
    public $dbglvl = 5;
    public $dbg_lvl_end = 10;

    function pout($log_level, $msg) {
        echo $msg;
    }

    function dbg($msg, $dbglvl=10, $returnmsg=false) {
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

        $this->dbg("test_ranges",$this->dbg_lvl_end);
    }
    function test_array() {
        $amain = array();
        $a0 = array();
        for($i = 0; $i < 2; $i++) {
            $a0["k0.$i"] = "v0.$i";
        }
        $a1 = array();
        for($i = 0; $i < 2; $i++) {
            $a1["k1.$i"] = "v1.$i";
        }
        $a2 = array();
        for($i = 0; $i < 2; $i++) {
            $a2["k2.$i"] = "v2.$i";
        }

        array_push($amain, $a0);
        array_push($amain, $a1);
        array_push($amain, $a2);

        assert(is_array($amain));
        assert(count($amain) == 3);

        $collect = array();
        foreach($amain as $a) {
            foreach($a as $k=>$v) {
                $val = $k . "=" . $v;
                array_push($collect,$val);
            }
        }
        $res = var_export($collect,true);
        assert(is_array($collect));
        assert(!is_array($res));
        assert(is_string($res));
        $str_exp =
            "array (
  0 => 'k0.0=v0.0',
  1 => 'k0.1=v0.1',
  2 => 'k1.0=v1.0',
  3 => 'k1.1=v1.1',
  4 => 'k2.0=v2.0',
  5 => 'k2.1=v2.1',
)";
        assert($res == $str_exp);
        $str_exp = "array (\n  0 => 'k0.0=v0.0',\n  1 => 'k0.1=v0.1',\n  2 => 'k1.0=v1.0',\n  3 => 'k1.1=v1.1',\n  4 => 'k2.0=v2.0',\n  5 => 'k2.1=v2.1',\n)";
        assert($res == $str_exp);
        $str_exp = "array (\n  0 => 'k0.0=v0.0',\n  1 => 'k0.1=v0.1',\n2 => 'k1.0=v1.0',\n  3 => 'k1.1=v1.1',\n  4 => 'k2.0=v2.0',\n  5 => 'k2.1=v2.1',\n)";
        assert($res != $str_exp);

        $res = null;
        // this just prints it out, no assignment to $res
        //$res = var_export($collect,false);
        assert(!is_array($res));
        assert(!is_string($res));   // $res is not array or string anymore
        assert($res == null);

        $a0 = null;
        assert(!isset($a0));
        assert(empty($a0));
        $a0 = "";
        assert(isset($a0));
        assert(empty($a0));
        $a0 = [];
        assert(isset($a0));
        assert(empty($a0));
        assert(count($a0) == 0); // count fails if var is null

        $a0 = ["something"];
        assert(isset($a0));
        assert(count($a0) != 0); // count fails if var is null
        assert(!empty($a0));

        //assert(count(null) == 0);
        $a0 = array();
        assert($a0 == null);
        assert(count($a0) == 0);
        array_push($a0, 1);
        array_push($a0, 2);
        assert(count($a0) == 2);
        assert($a0 != null);

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
        //assert(count($a1) == 0);

        $a = null;
        assert(!isset($a));  // returns false if null
        assert($a == null);
        $a = array();
        assert(isset($a));
        assert(count($a) == 0);
        $exp_count = 5;
        $a["k1"]="v1";
        $a["k2"]="v2";
        $a["k3"]="v3";
        $a["k_null"]=null;
        $a['k_empty']='';
        assert(count($a) == $exp_count);
        $lk = array();
        $lv = array();
        foreach($a as $k=>$v) {
            array_push($lk,$k);
            array_push($lv,$v);
        }
        assert(count($lk) == $exp_count);
        assert(count($lk) == count($lv));
        assert(isset($a["k1"]));
        assert($a["k_null"] == null);
        assert(!isset($a["k_null"])); // returns false if null
        assert(isset($a["k_empty"]));
        assert(empty($a["k_empty"]));
        assert(empty($a["k_null"]));
        assert(empty($a["blah"]));
        assert(!empty($a["k1"]));
        assert(!isset($a["blah"]));
        assert(!key_exists("blah",$a));
        assert(key_exists("k_null",$a));
        assert(key_exists("k_empty",$a));
        assert(key_exists("k1",$a)); // this is alias of array_key_exists
        assert(array_key_exists("k1",$a));
        assert(array_key_exists('k1',$a));
        assert(in_array('k1',$lk));
        assert(in_array("k1",$lk));
        assert(!key_exists("k1",$lk));
        assert(!array_key_exists("k1",$lk));
        assert(in_array("v1",$lv));
        assert(!array_key_exists("v1",$lv));

        $l = array();
        foreach($lk as $k) {
            array_push($l,$k);
        }

        assert(count($l) == $exp_count);
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
        $a4 = [];
        $a5 = [""];
        assert(count($a1) == 3);
        assert(count($a4) == 0);
        assert(count($a5) == 1);
        $a3 = array_diff($a1,$a2);
        assert(count($a3) == 0);
        assert(!key_exists(4,$a1)); // this is referring to index?
        assert(in_array(4,$a1));
        assert(key_exists(1,$a1)); // this is referring to index?
        assert(!in_array(1,$a1));
        $a1 = ["abc","def","ghi","jkl"];
        assert(count($a1) == 4);
        $str = "";
        foreach($a1 as $v) {
            $str .= $v;         // NOT $str += $v !! that's number operator
        }
        assert($str == "abcdefghijkl");
        assert(isset($a1[0]));
        assert(!isset($a1[100]));
        assert(key_exists(1,$a1));  // this is index
        assert(!key_exists(100,$a1));  // this is index
        assert(!key_exists("def",$a1));  // this is index, so value doesnt work
        assert(in_array("def",$a1));
        assert(!in_array("xyz",$a1));
        $a1 = [
            'k1'=>'v1',
            'k2'=>'v2',
            'k3'=>'v3'
        ];
        assert(count($a1) == 3);
        assert(array_key_exists('k1',$a1));


        //$a1 = [
        //    k1=>'v1',
        //    k2=>'v2',
        //    k3=>'v3'
        //];
        assert(count($a1) == 3);
        assert(array_key_exists('k1',$a1));
        assert(!array_key_exists('k10',$a1));

        $this->dbg("test_structures",$this->dbg_lvl_end);
    }

    function is_filtered($string, &$patterns, $filter_match_include=true) {
        foreach($patterns as $filter) {
            if(preg_match("/{$filter}/",$string)) {
                return $filter_match_include;
            }
        }
        return !$filter_match_include;
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

        $l = preg_split("/,/","the,cat,in,the,hat");
        assert($l == ["the","cat","in","the","hat"]);
        assert($l[0] == "the");

        $l = preg_split("/,/","the,cat,,in,the,hat");
        assert($l == ["the","cat","","in","the","hat"]);
        assert($l[0] == "the");

        $l = preg_split("/,/","the,cat ,in, the,hat");
        assert($l == ["the","cat ","in"," the","hat"]);
        assert($l != ["the","cat "," in"," the","hat"]);
        assert($l[0] == "the");

        $l = preg_split("/,/","the");
        assert($l == ["the"]);
        assert($l[0] == "the");

        $l = preg_split("/,/","the,");
        assert($l == ["the",""]);
        assert($l[0] == "the");

        $l = preg_split("/,/","");
        assert($l == [""]);
        assert($l[0] == "");

        $l = preg_split("/,/",null);
        assert($l == [""]);
        assert($l[0] == "");

        $l = preg_split("/,/",",the,");
        assert($l == ["","the",""]);
        assert($l[1] == "the");

        $v = "";
        assert(isset($v));
        assert(strlen($v) == 0);

        $v = null;
        assert(!isset($v));
        assert(strlen($v) == 0);

        $s = "the cat in the bin hat";
        assert(preg_match("/cat/",$s));
        assert(!preg_match("/^cat/",$s));
        assert(preg_match("/^the/",$s));
        assert(preg_match("/hat/",$s));
        assert(!preg_match("/bat/",$s));
        assert(!preg_match("/the$/",$s));
        assert(preg_match("/hat$/",$s));
        assert(preg_match("/\bhat$/",$s));
        assert(!preg_match("/\bat$/",$s)); // word boundary \b
        assert(preg_match("/\bin\b/",$s));
        assert(!preg_match("/\bin\b$/",$s));


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
        assert(count($res[0]) == 6);
        assert($res == [["the","cat","in","the","bin","hat"]]); // all matches

        $v1 = "123abc456";
        $v2 = "123-abc-456";
        assert(!preg_match("/-abc-/",$v1));
        assert(preg_match("/abc/",$v1));
        assert(preg_match("/-abc-/",$v2));
        assert(preg_match("/abc/",$v2));

        $v7='the  hat  cat in   the cat hat';
        $pat_dog = "dog";
        $pat_cat = "cat";

        assert(!preg_match("/dog/",$v7));
        assert(preg_match("/cat/",$v7));
        //assert(!preg_match($pat_dog,$v7)); // delimiter must be //
        //assert(preg_match($pat_cat,$v7)); // delimiter must be //
        //assert(!preg_match("$pat_dog",$v7)); // delimiter must be //
        //assert(preg_match("$pat_cat",$v7)); // delimiter must be //
        assert(!preg_match("/$pat_dog/",$v7));
        assert(preg_match("/$pat_cat/",$v7));
        assert(!preg_match("/${pat_dog}/",$v7));
        assert(preg_match("/${pat_cat}/",$v7));
        assert(!preg_match("/{$pat_dog}/",$v7));
        assert(preg_match("/{$pat_cat}/",$v7));
        $patterns = array("cat","dog");
        $v1 = "the cat in the hat";
        $v2 = "the dog in the park";
        $v3 = "the human in the office";
        assert($this->is_filtered($v1,$patterns));
        assert($this->is_filtered($v2,$patterns));
        assert(!$this->is_filtered($v3,$patterns));
        assert($this->is_filtered($v1,$patterns,true));
        assert($this->is_filtered($v2,$patterns,true));
        assert(!$this->is_filtered($v3,$patterns,true));
        assert(!$this->is_filtered($v1,$patterns,false));
        assert(!$this->is_filtered($v2,$patterns,false));
        assert($this->is_filtered($v3,$patterns,false));

        $exp = "the cat in the hat";
        $s1 = "cat";
        $keycat = "keycat";
        $keydog = "keydog";
        $a = ["keyhuh"=>"huh","keycat"=>"cat","keydog"=>"dog"];
        assert($a["keycat"] == "cat");

        $act = "the $s1 in the hat";
        assert($act == $exp);
        $act = "the ${s1} in the hat";
        assert($act == $exp);
        $act = "the {$s1} in the hat";
        assert($act == $exp);
        $act = "the {$a['keycat']} in the hat";
        assert($act == $exp);
        $act = "the ${a['keycat']} in the hat";
        assert($act == $exp);
        $act = "the ${a["keycat"]} in the hat";
        assert($act == $exp);
        $act = "the ${a[$keycat]} in the hat";
        assert($act == $exp);
        $act = "the {$a[$keycat]} in the hat";
        assert($act == $exp);
        $act = "the ${a[$keydog]} in the hat";
        assert($act != $exp);
        $act = "the '$a[$keycat]' in the hat";
        assert($act == "the 'cat' in the hat");


        $this->dbg("test_strings",$this->dbg_lvl_end);
    }
    function test_url() {
        $decoded = "search?Abc And \"Something\"; another thing& and anoth";
        $encoded = urlencode($decoded);  // spaces are +
        $exp = "search%3FAbc+And+%22Something%22%3B+another+thing%26+and+anoth";
        assert($encoded == $exp);
        $act = urldecode($encoded);
        assert($act == $decoded);
        $encoded = rawurlencode($decoded);  // spaces are %20, not +
        $exp = "search%3FAbc%20And%20%22Something%22%3B%20another%20thing%26%20and%20anoth";
        assert($encoded == $exp);
        $act = urldecode($encoded);
        assert($act == $decoded);
        $act = rawurldecode($encoded);
        assert($act == $decoded);

        $decoded = "Abc And \"Something\"; another thing& and anoth";
        $encoded = urlencode($decoded);
        $exp = "Abc+And+%22Something%22%3B+another+thing%26+and+anoth";
        assert($encoded == $exp);
        $encoded = rawurlencode($decoded);  // spaces are %20, not +
        $exp = "Abc%20And%20%22Something%22%3B%20another%20thing%26%20and%20anoth";
        assert($encoded == $exp);
        $act = urldecode($encoded);
        assert($act == $decoded);
        $act = rawurldecode($encoded);
        assert($act == $decoded);

        $decoded = "[!@#$%^&*(;',.)]";
        $encoded = urlencode($decoded);
        $exp = "%5B%21%40%23%24%25%5E%26%2A%28%3B%27%2C.%29%5D";
        assert($exp == $encoded);
        $act = urldecode($encoded);
        assert($act == $decoded);

        $encoded = rawurlencode($decoded);
        assert($exp == $encoded);
        $act = urldecode($encoded);
        assert($act == $decoded);

        $decoded = "[!@#$%^&*(;',.)-_+=\"?/<>{}|]";
        $encoded = urlencode($decoded);
        //        [  @  #  $  %  ^  &  *  (  ;  '  ,   .  )-_  +  =  "  ?  /  <  >  {  }  |  ]
        $exp = "%5B%21%40%23%24%25%5E%26%2A%28%3B%27%2C.%29-_%2B%3D%22%3F%2F%3C%3E%7B%7D%7C%5D";
        assert($exp == $encoded);
        $act = urldecode($encoded);
        assert($act == $decoded);

        $decoded = "[!@#$%^&*(;',.)-_+=\"?/<>{}|]";
        $encoded = rawurlencode($decoded);
        //        [  @  #  $  %  ^  &  *  (  ;  '  ,   .  )-_  +  =  "  ?  /  <  >  {  }  |  ]
        $exp = "%5B%21%40%23%24%25%5E%26%2A%28%3B%27%2C.%29-_%2B%3D%22%3F%2F%3C%3E%7B%7D%7C%5D";
        assert($exp == $encoded);


        $this->dbg("test_url",$this->dbg_lvl_end);
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
        assert(!0);
        assert(1);
        $v = null;
        assert($v == null);
        assert(!$v);

        $v1 = (5 < 10) ? 5 : 10;
        $v2 = (10 > 5) ? 10 : 5;
        assert($v1 == 5 && $v2 == 10);

        //$this->dbg("hello\n");    // this works
        assert($this->dbg("hello1\n",5,true) == "hello1\n");

        $this->dbg("test_syntax",$this->dbg_lvl_end);

        $v = 10;
        $e = 0;
        if($v < 0) {
            $e = 0;
        } elseif($v < 10) {  // elseif not else if
            $e = 0;
        } else {
            $e = 1;
        }
        assert($e == 1);

    }
}

openlog("mylog.php.log", LOG_CONS, LOG_USER);
$t = new Test();
$t->test_ranges();
$t->test_syntax();
$t->test_array();
$t->test_strings();
$t->test_url();
closelog();

?>
