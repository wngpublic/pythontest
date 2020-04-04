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

        // array of arrays
        $aa = array();
        for($i = 0; $i < 3; $i++) {
            $k = "k.$i";
            $aa[$k] = array();              // this works!
            for($j = 0; $j < 3; $j++) {
                $kk = "$k.$j";
                $aa[$k][$kk] = $j;
            }
        }
        //echo "aa: " . var_export($aa,true) . "\n";
        assert(array_key_exists("k.1",$aa));
        $a = $aa["k.1"];
        assert(array_key_exists("k.1.2",$a));
        assert($a["k.1.2"] == 2);
        assert(count($aa) == 3);
        assert(count($aa['k.1']) == 3);

        $aa1 = array();
        $aa2 = array();
        $aa3 = array();
        $a1 = array();
        $a2 = array();
        $aa1['a1'] = $a1; // this doesnt work, copies $a1 into $aa1, which is empty
        $aa1['a2'] = $a2; // this doesnt work
        $aa3['a1'] = &$a1; // this works, copies $a1 into $aa1, which is reference
        $aa3['a2'] = &$a2; // this works
        for($j = 0; $j < 2; $j++) {
            $a1["a1.$j"] = $j;
        }
        for($j = 0; $j < 2; $j++) {
            $a2["a2.$j"] = $j;
        }
        $aa2['a1'] = $a1;  // this works, copies $a1 into $aa2, which is populated
        $aa2['a2'] = $a2;  // this works

        //echo "aa1: " . var_export($aa1,true) . "\n";
        //echo "aa2: " . var_export($aa2,true) . "\n";
        //echo "aa3: " . var_export($aa3,true) . "\n";
        $va1 = $aa1['a1'];
        $va2 = $aa2['a1'];
        $va3 = $aa3['a1'];
        assert(!array_key_exists('a1.1',$aa1['a1']));
        assert(array_key_exists('a1.1',$aa2['a1']));
        assert(array_key_exists('a1.1',$aa3['a1']));
        assert(!array_key_exists('a1.1',$va1));
        assert(array_key_exists('a1.1',$va2));
        assert(array_key_exists('a1.1',$va3));
        assert(count($aa1) == 2);
        assert(count($aa1['a1']) == 0);
        assert(count($aa2['a1']) == 2);
        assert(count($aa3['a1']) == 2);

        // array of arrays, this is broken!
        $aa = array();
        for($i = 0; $i < 2; $i++) {
            $a = array();
            $aa["k.$i"] =  $a;      // this doesnt work!! why?? because $a gets reassigned
            //$aa["k.$i"] = &$a;      // this doesnt work!! why??
            for($j = 0; $j < 2; $j++) {
                $a["$k.$j"] = $j;
            }
        }
        assert(count($aa['k.1']) == 0);
        assert(count($aa) == 2);

        //echo "aa: " . var_export($aa,true) . "\n";

        //assert(array_key_exists("k.1",$aa));
        //$a = $aa["k.1"];
        //echo "a " . var_export($a,true) . "\n";
        //assert(array_key_exists("k.1.2",$a));
        //assert($a["k.1.2"] == 2);

        // this works!!
        $aa = array();
        for($i = 0; $i < 2; $i++) {
            $a = array();
            for($j = 0; $j < 2; $j++) {
                $a["k.$i.$j"] = $i * 10 + $j;
            }
            $aa["k.$i"] =  $a;
        }
        //echo "aa: " . var_export($aa,true) . "\n";
        assert(count($aa) == 2);
        assert(count($aa['k.0']) == 2);
        assert(count($aa['k.1']) == 2);
        assert($aa['k.0']['k.0.0'] == 0);
        assert($aa['k.0']['k.0.1'] == 1);
        assert($aa['k.1']['k.1.0'] == 10);
        assert($aa['k.1']['k.1.1'] == 11);

        $aa = array();
        for($i = 0; $i < 2; $i++) {
            $aa["k.$i"] = array();
            $a = $aa["k.$i"];
            for($j = 0; $j < 2; $j++) {
                $a["k.$i.$j"] = $j;
            }
        }
        //echo "aa: " . var_export($aa,true) . "\n";
        assert(count($aa) == 2);
        assert(count($aa['k.0']) == 0);
        assert(count($aa['k.1']) == 0);

        $a = array('k8'=>'v8','k2'=>'v2','k4'=>'v4','k1'=>'v1');
        ksort($a);
        //echo "sorted " . var_export($a,true) . "\n";

        $a = array();
        for($i = 0; $i < 100; $i++) {
            $a[$i] = "k.$i";
        }
        $chunks_of_10 = array_chunk($a,10);
        $chunks_of_25 = array_chunk($a,25);
        $chunks_of_5 = array_chunk($chunks_of_10, 5);

        assert(count($chunks_of_10) == 10);
        assert(count($chunks_of_25) == 4);
        assert(count($chunks_of_5) == 2); // chunks 0-4 and 5-10 of chunks_of_10
        //echo "count: " . count($chunks_of_25) . " count: " . count($chunks_of_5) . " count: " . count($chunks_of_10) . "\n";
        //echo "\n------chunks_of_25:\n " . var_export($chunks_of_25,true) . "\n";
        //echo "\n------chunks_of_10:\n " . var_export($chunks_of_10,true) . "\n";
        //echo "\n------chunks_of_5:\n " . var_export($chunks_of_5,true) . "\n";
        //assert(count($chunks_of_20) == 50);

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

        $str_num = "123.45";
        $str_cat = "cat";
        assert(is_numeric($str_num));
        assert(!is_numeric($str_cat));
        $v_int = (int)$str_num;
        assert($v_int == 123);
        $v_f = (float)$str_num;
        assert($v_f == 123.45);
        $v_d = (double)$str_num;
        assert($v_d == 123.45);
        $v = $str_cat . $v_int;
        assert($v == "cat123");
        assert(intval("10") == 10);
        assert(intval("-10") == -10);
        assert(!is_int("10"));
        assert(is_int(10));
        assert(!is_int(10.1));
        assert(is_string("10"));
        assert(is_array(array()));

        $v = null;
        assert($v !== FALSE);
        assert($v === null && $v == null && $v == NULL && $v == Null);

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

    function test_json() {
        $s_val = '{"k1":{"k11":"v11","k12":"v12","k13":"v13"},"k2":[{"k211":"v211","k212":"v212"},{"k221":"v221","k222":"v222"},{"k231":"v231","k232":"v232"}],"k3":"v3"}';
        $json_val = json_decode($s_val,true);

        assert($json_val != null);
        assert($json_val["k3"] == "v3");
        assert(is_array($json_val["k1"]));
        assert(is_array($json_val["k2"]));
        assert(!is_array($json_val["k3"]));
        assert(!key_exists("k1111",$json_val["k1"]));
        assert(key_exists("k11",$json_val["k1"]));
        assert(key_exists(1,$json_val["k2"]));
        assert($json_val["k2"][1]["k221"] == "v221");
        assert(!key_exists(10,$json_val["k2"]));

        $s_val = '{"k1":[["v11","v12","v13"],["v21","v22","v23"],["v31","v32","v33"]]}';
        $json_val = json_decode($s_val,true);
        //echo var_export($json_val,true);

        $this->dbg("test_json",$this->dbg_lvl_end);
    }

    function test_time() {
        $time_str_pst = "Tuesday, March 10, 2020 11:35:00 AM";
        $time_str_gmt = "Tuesday, March 10, 2020 6:35:00 PM";
        $time_str_mil_pst = "2020-03-10 11:35";
        $time_str_mil_gmt = "2020-03-10 18:35";
        $time_sec_1 = 1583840100;   # Tuesday, March 10, 2020 11:35:00 AM GMT or Tuesday, March 10, 2020 4:35:00 AM GMT-07:00 DST PST
        $time_sec = 1583865300;
        $time_1   = 1583840100;
        $time_dif = $time_sec - $time_1;
        $v1 = strtotime($time_str_mil_pst);
        $v2 = strtotime($time_str_mil_gmt);
        //echo "time_sec: $time_sec translated pst/gmt:$v1/$v2 time_dif = $time_dif\n";
        $date = new DateTime();
        $time_zone = $date->getTimezone();
        //echo $time_zone->getName() . "\n";
        //echo date_default_timezone_get() . "\n";
        //$timezone_get_1 = date_timezone_get();
        //echo var_export($timezone_get_1,true);
        //assert($v1 == $time_sec);
        //t0: 2020-03-10 11:40 t1: 2020-03-10 11:45 t0_sec: 1583865600  t1_sec: 1583865900
        $time_s1 = "2020-03-10 11:40";
        $time_i1 = strtotime($time_s1);
        //echo "time s1: $time_s1 i:$time_i1\n";

        $time_s1 = "2020-03-10 18:40";
        $time_i1 = strtotime($time_s1);
        //echo "time s1: $time_s1 i:$time_i1\n";

    }
}

openlog("mylog.php.log", LOG_CONS, LOG_USER);
$t = new Test();
$t->test_ranges();
$t->test_syntax();
$t->test_array();
$t->test_strings();
$t->test_json();
$t->test_url();
$t->test_time();
closelog();

?>
