class TestBasic {
    assert = require('assert');
    constructor(v1) {
        this.v1 = v1;
        console.log('TestBasic constructor ' + v1);
    }
    hello() {
        console.log('hello world')
    }
    test_assert() {
        var assert = require('assert');
        var x = 'hello';
        console.assert(x == 'hello');
        this.assert(x == 'hello');
        assert(x == 'hello');
    }
    test_string() {
        var assert = require('assert');
        var v1 = "abc,def,ghi,123,456";
        var a1 = v1.split(/,/);
        assert(a1.length == 5);
        assert(a1[1] == 'def');
        var v2 = "abc=123&def=234&ghi=345";
        var v2a = v2.split(/&/).map(s => s.split('='));
        var v2map = new Map(v2a);
        var v2kv = {};
        v2a.forEach(([k,v]) => v2kv[k] = v);
        assert(v2map.size == 3);
        assert(Object.keys(v2kv).length == 3); // there is no length property in dict
        assert(v2kv['abc'] == '123');
        assert(v2kv['blah'] == undefined);
        assert(v2map.get('abc') == '123');

        var v3 = "abc" + "=" + "123";
        v3 += "," + "def=456";
        assert(v3 == "abc=123,def=456");

        assert(v3.search(/abc/) == 0);
        assert(v3.search(/123/) == 4);  // returns index
        assert(v3.search(/xyz/) == -1);
        assert(v3.includes('def'));
        assert(v3.indexOf('def') == 8);
        assert(!v3.includes('xyz'));
        assert(v3.indexOf('xyz') == -1);

        var v4 = "abc=123,def=456,abc=123,def=789";
        var v5 = v4.replace(/123/,'2345');
        var v6 = v4.replace(/123/g,'2345');
        assert(v4 == "abc=123,def=456,abc=123,def=789");
        assert(v5 == "abc=2345,def=456,abc=123,def=789");
        assert(v6 == "abc=2345,def=456,abc=2345,def=789");

        assert(v4.match(/\d+/));        // regex
        assert(v4.match(/\d{3}/));
        assert(!v4.match(/\d{4}/));
        assert(v4.match(/,[a-z]{3}/));
        assert(!v4.match(/;[a-z]{3}/));
        var group4 = v4.match(/,([a-z]{3})=(\d{3})/);
        assert(group4[1] == 'def');
        assert(group4[2] == '456');
        var group6 = v6.match(/,([a-z]{3})=(\d{4}),/);
        assert(group6[1] == 'abc');
        assert(group6[2] == '2345');

        console.log('pass test_string');
    }
    test_array() {
        var a_exp = ['apple','banana','cranberry'];
        var a = [];
        a.push('apple');
        a.push('banana');
        a.push('cranberry');

        this.assert(a[0] == 'apple');
        this.assert(a.length == 3);

        this.assert(a_exp != a);
        var a_act_json = JSON.stringify(a);
        var a_exp_json = JSON.stringify(a_exp);
        this.assert(a_act_json == '["apple","banana","cranberry"]');
        this.assert('["apple","banana","cranberry"]' == "[\"apple\",\"banana\",\"cranberry\"]");
        this.assert(a_act_json == a_exp_json);
        for(var i = 0; i < a.length; i++) {
            this.assert(a[i] == a_exp[i]);
        }
    }
    test_map() {
        var assert = require('assert');

        var d1 = {};
        d1['k1']='v1';
        d1['k2']='v2';
        d1['k3']='v3';
        assert(d1.length != 3); // this is not the way to get length of dict
        assert(Object.keys(d1).length == 3);
        var a1 = [];
        for(var k in d1) {
            a1.push(k);
        }
        a1.sort();
        var v1 = "";
        for(var i in a1) {      // this is index, not val
            v1 += a1[i] + ":" + d1[a1[i]] + ";";
        }
        assert(v1 == "k1:v1;k2:v2;k3:v3;");
        v1 = "";
        for(var i = 0; i < a1.length; i++) {
            v1 += a1[i] + ":" + d1[a1[i]] + ";";
        }
        assert(v1 == "k1:v1;k2:v2;k3:v3;");

        v1 = "";
        for(var k in d1) {
            v1 += k + ":" + d1[k] + ";";
        }
        assert(v1 == "k1:v1;k2:v2;k3:v3;"); // this may not always work because ordering not guaranteed

        var map = new Map();
        map.set('k1','v1');
        map.set('k2','v2');
        map.set('k3','v3');
        assert(map.get('k1') == 'v1');
        assert(map.get('blah') == undefined);
        assert(map.size == 3);
        map.clear();
        assert(map.size == 0);

        console.log('pass test_map');
    }
    test_control() {
        var a = [1,2,3,4,5];
        var ctr = 0;
        for(var v in a) ctr++;
        this.assert(ctr == 5);

        console.log('pass test_control');
    }
}

function test1() {
    t = new TestBasic("c1");
    //t.hello();
    t.test_assert();
    t.test_array();
    t.test_string();
    t.test_control();
    t.test_map();
}

function test2() {

}

test1();