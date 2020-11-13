'use strict';
const buffer = require('buffer');

let gF1 = function() {
    return 10;
}

let gF2 = function(s1,s2) {
    return (s1+' '+s2);
}

let gF3 = function(i1,i2) {
    return (i1*i2);
}

let gF4Callback = function(v1,v2,cb) {
    return cb(v1,v2);
}

let gF5 = function(v) {
    return v;
}

class TestBasic {
    assert = require('assert');

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
        var a = 10, b = 20, c = {};
        var x = 'hello';
        console.assert(x == 'hello');
        this.assert(x == 'hello');
        assert(x == 'hello');
        let _ = 'hello';
        this.assert(_ == 'hello'); // _ and $ have no special meaning
        let $ = 'hello';
        this.assert($ == 'hello');
        const y = 'hello';
        let flag = false;
        let eType = 0;
        try {
            y = 'this should fault';
        } catch(e) {
            if(e instanceof TypeError) {
                eType = 1;
            }
            flag = true;
        } finally {
            this.assert(flag == true);
            this.assert(y == 'hello');
        }
        this.assert(10 == '10');    // equality with conversion first, does not check data type
        this.assert(10 !== '10');   // strict inequality with no conversion
        this.assert(!(10 != '10'));    // this will convert to same type first, then compare
        this.assert(10 === 10);     // strict equality with no conversion, checks data type
        this.assert('10' === '10');
    }
    test_numberFormat() {
        let v = (12.345).toFixed(2);
        this.assert(v == "12.35");
        this.assert(v == 12.35);
        v = (12.3).toFixed(2);
        this.assert(v == 12.30);
        this.assert(v == "12.30");
        this.assert(v != "12.300");

        let s = "1234.56";
        v = Number(s);
        this.assert(v == 1234.56);
        s = (1234.45).toString();
        this.assert(s == "1234.45");
        s = (1234).toString(16); // base16
        this.assert(s == '4d2');
        v = Number.MAX_VALUE;
        
        v = Number.parseInt("123");
        this.assert(v == 123);
        this.assert(!Number.isSafeInteger("123"));
        this.assert(Number.isSafeInteger(123));

        v = parseInt(123.45);
        this.assert(v == 123);

        console.log('pass test_NumberFormat');
    }
    testDate() {
        const fIsLeapYear = (y) => {
            if(y % 4 != 0) {
                return false;
            } else if (y % 100 != 0) {
                return true;
            } else if (y % 400 != 0) {
                return false;
            } else {
                return true;
            }
        }
        const fNumLeapYears = (y1,y2) => {
            let ctr = 0;
            for(let y = y1; y <= y2; y++) {
                if(fIsLeapYear(y)) {
                    ctr++;
                }
            }
            return ctr;
        }
        let assert = require('assert');
        let date;
        date = new Date(2020,0,1);
        assert(date.toString() == 'Wed Jan 01 2020 00:00:00 GMT-0800 (Pacific Standard Time)');
        let ms = date.getTime();  // time in millis
        assert(ms == 1577865600000);
        let numS = ms/1000;
        let numSecInDay = 60 * 60 * 24;
        let numSecInCommonYear = numSecInDay * 365;
        let numSecInLeapYear = numSecInDay * 366;
        let numLeapYears1970To2019 = fNumLeapYears(1970,2019);
        assert(numLeapYears1970To2019 == 12);

        let numYears1970To2019 = 2019-1970+1;
        let numSecs1970To2019 = (numYears1970To2019-numLeapYears1970To2019)*numSecInCommonYear +
            numLeapYears1970To2019 * numSecInLeapYear;
        let diffExp = Math.abs(numSecs1970To2019-numS);
        let diffExpHours = diffExp/60/60;
        assert(diffExpHours < 24); // because of time zone vs UTC
        date = new Date('January 2, 2020');
        date = new Date();

        /*
        // available on browser
        let t0 = performance.now();
        setTimeout(()=>{},100);
        let t1 = performance.now();
        diffExp = t1-t0;
        assert(diffExp > 100);
         */

        let t0 = Date.now();
        let t2 = 0;
        setTimeout(()=>{t2 += Date.now();},100);
        let t1 = Date.now();
        let diffExp2 = Math.abs(t2-t0);
        assert(diffExp2 == t0);
        diffExp = t1-t0;
        assert(diffExp < 10);

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
        v3 += "," + "def=456" + ',' + String(123);
        assert(v3 == "abc=123,def=456,123");

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

        let s = 'abcd efg';
        let l = []
        for(let i = 0; i < s.length; i++) {
          l.push(s.charAt(i));
        }
        assert(JSON.stringify(l) == JSON.stringify(['a','b','c','d',' ','e','f','g']));
        assert(l.join() != s);
        assert(l.join('') == s);
        assert(s.slice(0,s.length) == s);
        assert(s.slice(1,s.length-1) == 'bcd ef');

        // compare array and regex
        s = 'ababa123 345 cbcb999 123 456 222 33 789 88 5555 777 888 11 789 ababa';
        let re = /(\d{3})\s+(\d{2})\b/g;  // 3digits 2digits word boundary
        let res = s.match(re);
        assert(res != ['222 33','789 88','888 11']);
        assert(res != JSON.stringify(['222 33','789 88','888 11']));
        assert(JSON.stringify(res) == JSON.stringify(['222 33','789 88','888 11']));

        re = /\b\w{4}\d{3}\b/g;
        res = s.match(re);
        assert(res.length == 1 && res[0] == 'cbcb999');

        s = '<h1>abab</h2>';
        res = s.match(/<(.*?)>/g);
        assert(res.length == 2);
        assert(res[0] == '<h1>');
        assert(res[1] == '</h2>');

        s = ' the cat in  the  hat ';
        l = s.trim().split(/\s+/);
        assert(l.length == 5 && l.join(' ') == 'the cat in the hat');

        //   0          1         2         3
        //   0 2 4  6 8 0 2 4 6 8 0 2 4 6 8 0
        s = ' "abc\'s here","hello",,"what",,';
        s = JSON.stringify(s);
        let delimiter = ",";
        let bound = "'";
        let escape = "\\";
        let cprev = null;
        for(let i = 0; i < s.length; i++) {
            let c = s.charAt(i);
            //console.log(`c:${c} i:${i}`);
            if(c === delimiter && cprev != "\\") {
                //console.log(`${c} is delimited at ${i}`);
            }
            if(c === bound && cprev != "\\") {
                //console.log(`${c} is bound at ${i}`);
            }
            cprev = c;
        }
        
        let a = ["abc","efg","ijk"];
        s = JSON.stringify(a);
        console.log(s);
        a = '["abc","efg","ijk"]';
        s = JSON.stringify(a);
        console.log(s);
        a = JSON.parse(s);
        console.log(a);
        s = '[4,5,6]';
        a = JSON.parse(s);
        console.log(a);
        console.log(s);
        console.log('pass test_string');
    }

    test_array_map_set() {
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

        let r;
        a = ['aa','bb','cc','dd'];

        this.assert(a.length == 4 && a[0] == 'aa' && a[3] == 'dd');

        r = a.pop();
        this.assert(a.length == 3 && a[0] == 'aa' && a[2] == 'cc');
        this.assert(r == 'dd');

        r = a.shift();    // removes from front of list
        this.assert(a.length == 2);
        this.assert(r == 'aa');

        a.unshift('abc'); // adds to front of list
        this.assert(a.length == 3 && a[0] == 'abc');


        let ll = [];
        for(let i = 0; i < 3; i++) {
          ll.push([]);
          for(let j = 0; j < 2; j++) {
            ll[i].push(i*10+j);
          }
        }
        let exp = [[0,1],[10,11],[20,21]];
        this.assert(ll.length == 3 && ll[0].length == 2);
        for(let i = 0; i < 3; i++) {
          for(let j = 0; j < 2; j++) {
            this.assert(exp[i][j] == ll[i][j]);
          }
        }

        const fString2CharArray = (s) => {
            let l = [];
            for(let i = 0; i < s.length; i++) {
                l.push(s.charAt(i));
            }
            return l;
        }

        let s = 'abcdefg';
        this.assert(s.length == 7);
        a = fString2CharArray(s);
        let buf = [];

        // this is index, not val, in vs of
        for(let i in a) {
            buf.push(i);
        }
        r = buf.join(',');
        this.assert(r == '0,1,2,3,4,5,6');
        buf = [];
        for(let c of a) {
            buf.push(c);
        }
        r = buf.join(',');
        this.assert(r == 'a,b,c,d,e,f,g');

        // copy array and copy dict
        a = fString2CharArray(s);
        let acopy = [...a];
        this.assert(JSON.stringify(a) === JSON.stringify(acopy));
        this.assert(a != acopy);

        let d = {k1:'v1',k2:'v2',k3:'v3'}
        let dcopy = {...d}; // is this the copy syntax?
        this.assert(JSON.stringify(d) === JSON.stringify(dcopy));
        this.assert(d != dcopy);

        d = { 'k1':'v1', 'k2':'v2' };
        this.assert('k1' in d);
        this.assert(!('k10' in d));
        for(let k of Object.keys(d)) {
            let v = d[k];
            //console.log(`k:v = ${k} ${v}`);
        }
        //console.log(`\n`);
        for(let k in d) {
            if(d.hasOwnProperty(k)) {
                let v = d[k];
                //console.log(`k:v = ${k} ${v}`);
            }
        }
        
        d = {};
        
        this.assert(d.length != 0);
        this.assert(d !== {});
        this.assert(d != {});
        this.assert(Object.keys(d).length == 0);
        this.assert(JSON.stringify(d) === '{}');

        a = [];
        this.assert(a.length == 0);

        a = [1,2,3,4,5];
        let a1 = a.slice(2);
        this.assert(a1 !== [3,4,5]);                                    // array comparison fail
        this.assert(JSON.stringify(a1) === JSON.stringify([3,4,5]));    // do this way

        let a2 = [];
        a.forEach(x => a2.push(x+1));
        this.assert(JSON.stringify(a2) == JSON.stringify([2,3,4,5,6]));
                
        var assert = require('assert');

        let d10 = {
            'k1':1,
            'k2':2,
            'k3':3
        };

        // iterate json key value
        let a10 = [];
        Object.keys(d10).forEach(k => a10.push(k));
        assert(JSON.stringify(a10) == JSON.stringify(['k1','k2','k3']));

        var d1 = {};
        d1['k1']='v1';
        d1['k2']='v2';
        d1['k3']='v3';
        assert(d1.length != 3); // this is not the way to get length of dict
        assert(Object.keys(d1).length == 3);
        assert('k3' in d1);
        assert(!('k10' in d1));

        s = JSON.stringify(d1);
        assert(s == '{"k1":"v1","k2":"v2","k3":"v3"}');
        let json = JSON.parse(s);
        assert(JSON.stringify(json) == s);

        var lk = [];
        var lv = [];
        for(let [k,v] of Object.entries(d1)) {
            lk.push(k);
            lv.push(v);
        }

        // this could be out of order sometimes?
        assert(lk.join('') == 'k1k2k3');
        assert(lv.join('') == 'v1v2v3');

        a1 = [];
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

        d = {};                                 // map to json
        map.forEach((v,k) => { d[k] = v });
        assert(JSON.stringify(d) === '{"k1":"v1","k2":"v2","k3":"v3"}');

        let m = new Map();
        for(let [k,v] of Object.entries(d)) {   // json to map
            m.set(k,v);
        }
        d = {};                                 // map to json
        m.forEach((v,k) => { d[k] = v });
        assert(JSON.stringify(d) === '{"k1":"v1","k2":"v2","k3":"v3"}');

        m.clear();                              // validating if back and forth work
        for(let k in d) {                       // json to map
            m.set(k,d[k]);
        }
        d = {};                                 // map to json
        m.forEach((v,k) => { d[k] = v });
        assert(JSON.stringify(d) === '{"k1":"v1","k2":"v2","k3":"v3"}');
        
        let res = ''
        // for loop, using 'of' vs 'in'
        for(const [k,v] of map.entries()) {
          res += `${k},${v} `;
        }
        assert(res == 'k1,v1 k2,v2 k3,v3 ');

        map.delete('k2');
        assert(map.size == 2);
        map.clear();
        assert(map.size == 0);

        m = {
            k1:'aa',
            k2:'bb',
            k3:'cc'
        }
        assert(m['k1'] == 'aa');
        assert(m.length != 3); // because this is not a map, it's a property
        res = '';
        for(const prop in m) {
          res += `${prop},${m[prop]} `;
        }
        assert(res == 'k1,aa k2,bb k3,cc ');

        let d2 = {};
        let j1 = {};
        let j2 = {};
        let v = '', v2 = '', v3 = '';
        let s1 = null, s2 = null, a3 = [];

        // find/search in array

        a = [1,2,3,4,5];
        a1 = a.filter(x => x % 2);
        this.assert(JSON.stringify(a1) === '[1,3,5]');
        a1 = [];
        a.forEach(x => { if(x % 2) { a1.push(x); }});
        this.assert(a1.join() === '1,3,5');
        
        a1 = Array(5);
        this.assert(a1.length === 5);
        this.assert(a1.join() === ',,,,');
        a1.fill(3);
        this.assert(a1.length === 5);
        this.assert(a1.join() === '3,3,3,3,3');

        a1 = [10,20,30,40];
        a2 = Array.from([10,20,30,40]);
        assert(JSON.stringify(a1) === JSON.stringify(a2));

        assert(a1.constructor === [].constructor);
        assert(a2.constructor === [].constructor);

        buf = [];
        for(let v in a1) {
            buf.push(v);
        }
        assert(buf.join() === '0,1,2,3');

        buf = [];
        for(let v of a1) {
            buf.push(v);
        }
        assert(buf.join() === '10,20,30,40');

        buf = [];
        for(let v in a2) {
            buf.push(v);
        }
        assert(buf.join() === '0,1,2,3');

        buf = [];
        for(let v of a2) {
            buf.push(v);
        }
        assert(buf.join() === '10,20,30,40');

        buf = [];
        a1.forEach(x => buf.push(x));
        assert(buf.join() === '10,20,30,40');

        buf = [];
        a1.map(x => buf.push(x*2));                 // map
        assert(buf.join() == '20,40,60,80');
        assert(a1.reduce((accumulator,v) => accumulator + v) === (10+20+30+40));

        a3 = [];
        a3.fill(10,0,5);
        assert(a3.length == 0);
        a3 = [0,0,0,0,0];
        assert(a3.length == 5);
        a3.fill(10,2,4);
        assert(JSON.stringify(a3) == '[0,0,10,10,0]');
        a3.fill(1);
        assert(JSON.stringify(a3) == '[1,1,1,1,1]');
        
        assert(!(20 in a1));        // doesnt work
        assert(a1.find((x,i) => { if(x === 20) return i; }) === 20); // why 20 and not index???
        assert(a1.find(x => x === 20) === 20);
        v = 20;
        assert(a1.find(x => x === v) === v);
        v = 100;
        assert(a1.find(x => x === v) === undefined);
        assert(a1.findIndex(x => x === 20) === 1);
        assert(a1.findIndex(x => x === 100) == -1);

        assert( a1.find(x => x === 100) === undefined && 
                a1.find(x => x === 100) == null &&
                a1.find(x => x === 100) !== null);
        assert(!(20 in a2));        // doesnt work
        assert(a2.find(x => x === 20) === 20);
        assert( a2.find(x => x === 100) === undefined && 
                a2.find(x => x === 100) == null &&
                a2.find(x => x === 100) !== null);

        let aa1 = [
            [1,2,3],
            [3,4,5],
            [5,6,7]
        ];
        assert(aa1[2][0] == 5);
        assert(aa1[2][2] == 7);

        // find/search in and json

        d1 = { 'k1':10, 'k2':20, 'k3':30 };
        d2 = { 'k1':10, 'k2':20, 'k3':30 };
        j1 = { 'k1':10, 'k2':20, 'k3':30 };
        j2 = { 'k1':10, 'k2':20, 'k3':30 };

        assert(d1.constructor === ({}).constructor);
        
        buf = [];
        for(let k in Object.keys(d1)) {
            buf.push(k);
        }
        assert(buf.join() === '0,1,2');

        buf = [];
        for(let k of Object.keys(d1)) {
            buf.push(k);
        }
        assert(buf.join() === 'k1,k2,k3');

        buf = [];
        let d3 = { 1:10, 2:20, 3:30 };
        for(let [k,v] of Object.entries(d3)) {
            buf.push(`${k}:${v}`);
        }
        assert(buf.join() === '1:10,2:20,3:30');
        
        let m1 = new Map();
        d2 = {};
        m1.forEach((v,k) => d2[k] = v);
        assert(JSON.stringify(d2) === '{}');
        for(let [k,v] of Object.entries(d1)) {
            m1.set(k,v);
        }
        m1.forEach((v,k) => d2[k] = v);         // iterate k,v of map. the kv are backwards!
        assert(JSON.stringify(d2) === '{"k1":10,"k2":20,"k3":30}');
        assert(m1.has('k1'));
        assert(!m1.has('k100'));
        assert(m1.get('k1') === 10);
        assert(m1['k1'] != 10);                 // map object cannot use [] notation!
        assert(m1.get('k100') === undefined && m1.get('k100') == null);
        
        assert(d1.hasOwnProperty('k1'));        // find key
        assert(!d1.hasOwnProperty('k100'));
        assert('k1' in d1);                     // find key
        assert(!('k100' in d1));
        assert( d1['k100'] === undefined &&     // find key
                d1['k100'] !== null &&
                d1['k100'] == null);
        assert( d1['k1'] === 10);

        assert(JSON.stringify(Object.keys(d1).sort()) === '["k1","k2","k3"]');
        assert(JSON.stringify(Object.values(d1).sort()) === '[10,20,30]');

        buf = [];
        d2 = {};
        for(let [k,v] of Object.entries(d1)) {
            d2[k] = v;
            buf.push(`${k}:${v}`);
        }
        assert(JSON.stringify(d1) === JSON.stringify(d2));
        assert(buf.join() === 'k1:10,k2:20,k3:30');

        // iterate/look in array, set, and json
        
        
        // functional syntax
        const fGetVal = k => { return m[k]; }
        res = fGetVal('k2');
        assert(res == 'bb');

        console.log('pass test_map');
    }
    test_random() {
        let min = 0;
        let max = 10;
        let d = {};
        let numcases = 100;
        for(let i = 0; i < numcases; i++) {
            let r = Math.random(); // random returns number between 0 and 1
            let v = Math.floor(r*(max-min)+min);
            if(!(v in d)) {
                d[v] = 0;
            }
            d[v]++;
        }
        for(let [k,v] of Object.entries(d)) {
            //console.log(`${k}:${v}`);
            this.assert(k < max);
        }

    }
    splitRow(row) {
        let delimiter = ',';
        let boundary = "'";
        let escape = "\\";
        let result = [];
        let sz = row.length;
        let inboundary = false;
        let markerCnt = 0;
        let lastpos = 0;
        let buffer = [];
        let prevchar = null;
        console.log(`row: ${row}`);
        for(let i = 0; i < sz; i++) {
            let c = row.charAt(i);
            if(c === delimiter) {
                if(inboundary) {
                    buffer.push(c);
                } else {
                    if(i == 0 || i == (sz-1) || prevchar == delimiter || prevchar === ' ') {
                        result.push(null);
                    } else {
                        throw `splitRow delimiter not in boundary: ${row} ${i} ${c}`;
                    }
                }
            }
            else if(c === boundary) {
                if(boundary) {
                    if(prevchar === escape) {
                        buffer.push(c);
                    } else {
                        let s = (buffer.length == 0) ? null : buffer.join();
                        buffer = [];
                        result.push(s);
                    }
                }
                inboundary = !inboundary;
            }
            else if(c === escape) {
            }
            else {
                if(inboundary) {
                    buffer.push(c);
                } else if(c !== ' ') {
                    throw `splitRow char not in boundary: ${row} ${i} ${c}`;
                }
            }
            prevchar = c;
        }
        return result;
    }

    test_control() {
        var a = [1,2,3,4,5];
        var ctr = 0;
        for(var v in a) ctr++;
        this.assert(ctr == 5);

        console.log('pass test_control');
    }

    test1() {
        let i1 = 10;
        let i2 = 20;
        let s1 = 'hello';
        let s2 = 'world';
        let r;
        r = gF4Callback(i1,i2,gF3);
        this.assert(r == 200);
        r = gF4Callback(s1,s2,gF2);
        this.assert(r == 'hello world');
    }
    testRetV1() {
        //let promise = new Promise(resolve => )
    }
    mySleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    mySleep2(ms) {
        return new Promise(resolve => setTimeout(resolve(10), ms));
    }
    mySleep3(ms,v) {
        return new Promise(resolve => setTimeout(resolve(v),ms));
    }
    async testSleep2() {
        await this.mySleep(100);
    }
    async testTimeoutCase1() {
        let l = [];

        const cb = (l) => { l.push(1); };
        let v = setTimeout(cb, 0, l);

        //await v;

        this.assert(v != null);
    }

    async testTimeoutCase2() {
        let x = 0;
        const cb = () => { this.assert(x == 100); };
        let handler = setTimeout(cb, 100);
        // setTimeout is executed after x = 100 assignment
        x = 100;
        // dont need this, just to show what handler can be used for
        clearTimeout(handler);
    }

    testTimeoutUse() {
        this.testTimeoutCase1();
        this.testTimeoutCase2();
    }
    testSleep() {
        let l = [];
        this.mySleep(100)
            .then(() => { l.push(10); })
            .then(() => { this.assert(l.length == 1 && l[0] == 10); });
        this.assert(l.length == 0 || l.length == 1); // this may or may not be true depending on if it gets completed
        //console.log(l);
        //this.assert(l.length == 1 && l[0] == 10); //this will not evaluate because async

        return;
    }
    testTimeout1() {
        let l = [];
        let ms = 10;
        let v = 100;
        const fTO = (ms,v) => { setTimeout((v) => { l.push(v); }, ms); };
        let handler = fTO(ms,v);
        // this is 0 because setTimeout hasn't finished executing
        this.assert(l.length == 0);
        // you cannot wait for timeout to finish executing. need to do await or promise
    }
    async caseTimeout2(ms,v,l,cb) {
        let lret = [];
        await setTimeout(cb,ms,v,l);
        lret.push(v);
        return lret;
    }
    // this await seems to work
    async testTimeout2SubAsync() {
        const cb = (x,l) => { l.push(x*2); }
        let l = [];
        let lret = await this.caseTimeout2(1000,5,l,cb);
        this.assert(lret.length == 1 && lret[0] == 5);

        // this hasnt executed yet
        this.assert(l.length == 0); // there is 100ms delay
        // this waits after it's finished executing to evaluate
        setTimeout(_ => {this.assert(l.length == 1 && l[0] == 10);}, 1000);

        let doAwait = true;
        if(doAwait) {
            // this will wait 1000ms and then the cb would have evaluated
            await this.mySleep(1000);
            this.assert(l.length == 1 && l[0] == 10);
        } else {
            // this hasn't finished executing original yet
            this.assert(l.length == 0);
        }
    }

    returnAfterTimeoutPromise(x,l,ms) {
        let y = 2*x;
        return new Promise(resolve => {
           setTimeout(() => {
               l.push(y);
               resolve(l);      // this returns l
           }, ms);
        });
    }
    async caseReturnAfterTimeoutPromise() {
        let lin = []
        let x = 10;
        let ms = 100;
        let lret = await this.returnAfterTimeoutPromise(x,lin,ms);
        // this part seems to work
        this.assert(lret.length == 1 && lret[0] == 2*x);
    }
    async caseReturnAfterTimeoutPromise2() {
        let lin = []
        let x = 10;
        let ms = 100;
        // this part seems to work because of "then"
        let lret = this.returnAfterTimeoutPromise(x,lin,ms)
                .then((lx) => this.assert(lx.length == 1 && lx[0] == 2*x));
        // but this part does not seem to work.
        let flag = false;
        try {
            this.assert(lret.length == 1 && lret[0] == 2*x);
        } catch(e) {
            flag = true;
        } finally {
            this.assert(flag);
        }
        // how to access promise now?
        //await lret;
        //lret.then((_ => this.assert(lret.length == 1 && lret[0] == 2*x)));
    }
    testReturnAfterTimeoutPromise() {
        this.caseReturnAfterTimeoutPromise();
        this.caseReturnAfterTimeoutPromise2();
    }
    async awaitSleepReturn1() {
        return await this.mySleep(10).then(v => 10);
    }
    async awaitSleepReturn2() {
        return await this.mySleep2(10).then((v) => { v+= 10; });
    }
    async testAsync1() {
        let v1 = this.awaitSleepReturn1();
        let v2 = await this.mySleep2(20);
        let v3 = this.awaitSleepReturn2();
        this.assert(v1 instanceof Promise);
        this.assert((v2 instanceof Promise) == false);
        this.assert(v3 instanceof Promise);
        this.assert(v1 != 10);
        this.assert(v2 == 10);
        this.assert(v3 != 20);

        // i dont understand this. doesnt do anything...
        let v4 = Promise.resolve(v3);
        this.assert(v4 != 20);
    }
    async testAsync2() {
        let promise = new Promise((res,rej) => {
            setTimeout(() => { res('hello'); },100);
        });
        // wait til promise is resolved
        // you cannot access promise status, must use via then()
        this.assert(promise instanceof Promise);
        let result = await promise;
        this.assert(result == 'hello');
    }
    async testAsync3() {
        let l = [];
        let x = 50;
        let promise = new Promise((res,rej) => {
            setTimeout(() => { l.push(x); res(x*2); },100);
        });
        // not executed yet
        this.assert(l.length == 0);
        let result = await promise;
        // executed
        this.assert(l.length == 1 && l[0] == x);
        this.assert(result == x*2);
    }
    async testAsync4() {
        // chaining promise
        let l = [];
        let x = 50;

        // not executed yet
        let promise = new Promise((res,rej) => {
            setTimeout(() => { l.push(x); res(x*2); },100);
        });
        let l2 = [];

        // this executes first. but what does it really do?
        promise.then(()=>{ l2.push(123); return l2; }).then(()=>{ l2.push(1234); });

        // but why is l still empty?
        this.assert(l.length == 0);

        // executed second
        let result = await promise;
        l2.push(result);

        this.assert(l2.join(',') == '123,100');

        // promise is done already, so no more
        promise.then((r)=>{ l2.push(456); });
        this.assert(l2.join(',') == '123,100');

        // l is no longer empty
        this.assert(l.length == 1 && l[0] == x);
        this.assert(result == x*2);

    }
    async testAsync5() {
        const f1Async = async () => {
            return await this.mySleep3(10,123);
        }
        const f2Sync = (x) => {
            return ('hello ' + String(x));
        }
        const f3Async = async (x) => {
            let v = await this.mySleep3(10,x);
            return v;
        }
        const f4Async = async () => {
            let v = await this.mySleep2(100);
            return v;
        }
        let t0,t1,tdiff;
        let debug = false;
        let v1 = await f1Async();
        this.assert(v1 == 123);
        let v2 = f2Sync('bob');
        this.assert(v2 == 'hello bob');
        let v3 = await f3Async(345);
        this.assert(v3 == 345);
        let v4 = await f4Async();
        this.assert(v4 == 10);

        const f5AsyncWaitGet = async (x,ms) => {
            return await this.mySleep3(ms,x);
        };
        const f5Async = () => {
            let l = [];
            l.push(100);
            for(let i = 0; i < 10; i++) {
                let v = f5AsyncWaitGet(i,1000);
                l.push(v);
            }
            l.push(200);
            return l;
        }
        t0 = Date.now();
        let l1 = f5Async();
        t1 = Date.now();
        tdiff = t1-t0;
        if(debug) {
            // this timing doesnt make sense..
            console.log(tdiff);
        }
        this.assert(l1.length == 12);
        this.assert(l1[0] == 100 && l1[1] instanceof Promise && l1[2] instanceof Promise && l1[l1.length-1] == 200);

        this.assert(l1[2] instanceof Promise);
        let v = await l1[2];
        this.assert(v == 1);

        const f6Async = async () => {
            let l = [];
            l.push(100);
            for(let i = 0; i < 10; i++) {
                let v = await f5AsyncWaitGet(i,1000);
                l.push(v);
            }
            l.push(200);
            return l;
        }
        t0 = Date.now();
        let l2 = await f6Async();
        t1 = Date.now();
        tdiff = t1-t0;
        if(debug) {
            // this timing doesnt make sense..
            console.log(tdiff);
        }
        this.assert(l2.length == 12);
        this.assert(l2[0] == 100 && l2[1] == 0 && l2[2] == 1 && l2[3] == 2 && l2[l2.length-1] == 200);

        t0 = Date.now();
        let l = [];
        let ms = 1000;
        v = await this.mySleep3(ms,10);
        l.push(v);
        v = await this.mySleep3(ms,20);
        l.push(v);
        v = await this.mySleep3(ms,30);
        l.push(v);
        t1 = Date.now();
        tdiff = t1-t0;
        if(debug) {
            // this timing doesnt make sense..
            console.log(tdiff);
        }

        t0 = Date.now();
        l = [];
        ms = 1000;
        v = await this.mySleep3(ms,10);
        l.push(v);
        v = await this.mySleep3(ms,20);
        l.push(v);
        v = await this.mySleep3(ms,30);
        l.push(v);
        t1 = Date.now();
        tdiff = t1-t0;

        l = [];
        ms = 1000;
        const delay = (x,ms) => new Promise(resolve => setTimeout(resolve(x), ms));
        t0 = Date.now();
        v = await delay(10,ms);
        l.push(v);
        v = await delay(20,ms);
        l.push(v);
        v = await delay(30,ms);
        l.push(v);
        t1 = Date.now();
        tdiff = t1-t0;

    }
    async testPromise1() {
        const promise1 = new Promise((resolve,reject) => {
            resolve(123);
        });
        const promise2EvenOdd = (x) => {
            return new Promise((resolve,reject) => {
                // no need for setTimeout(x,...), x is from scope
                setTimeout(() => {
                    if (x % 2 == 0) {
                        resolve(true);
                    } else {
                        reject(false);
                    }
                }, 100);
            });
        };
        let flag = false;
        let res1 = 0;
        let res2 = 0;
        let ctr = 0;
        let v1 = await promise2EvenOdd(2);
        let promise2 = promise2EvenOdd(3)
            .then((r) => {
                ctr++;
            })
            .catch(_ => { flag = true; res1 = 1; });
        // this should be true because of catch, but promise2EvenOdd not executed yet.
        //this.assert(flag);
        flag = false;
        let v3 = await promise2EvenOdd(4)
            .then((r) => {
                ctr++;
                return r;
            })
            .then((r) => {
                ctr++;
                return r;
            })
            .catch(_ => { flag = true; res2 = 2; });
        this.assert(flag);
        this.assert(v1 == true);
        this.assert(promise2 instanceof Promise);
        this.assert(v3 == true);        // because v3 then() returns v

        this.assert(ctr == 2);
        let v4 = await promise2EvenOdd(4)
            .then((r) => {
                ctr++;
            });

        this.assert(ctr == 3);
        this.assert(v4 == undefined); // because v4 then() doesn't return anything

        let promise5 = promise2EvenOdd(4)
            .then((r) => {
                ctr++;
                return r;
            })
            .then((r) => {
                ctr++;
                return r;
            })
            .catch(_ => { flag = true; res2 = 2; });

        let v5 = await promise5;
        this.assert(ctr == 5);

        const promiseInc = (x) => {
            return new Promise((resolve,reject) => {
                // no need for setTimeout(x,...), x is from scope
                setTimeout(() => {
                    x++;
                    resolve(x);
                }, 100);
            });
        };

        let promise6 = promiseInc(8)
            .then(x => { x++; return x; })
            .then(x => { x++; return x; })
            .catch(e => { flag = true; });
        let v = await promise6;     // this is how to wait for promise
        this.assert(v == 11);

        let promise7 = promiseInc(8)
            .then(x => { x++; return x; })
            .then(x => { x++; return x; })
            .catch(e => { flag = true; });
        let promise8 = promiseInc(9)
            .then(x => { x++; return x; })
            .then(x => { x++; return x; })
            .catch(e => { flag = true; });
        let promise9 = promiseInc(10)
            .then(x => { x++; return x; })
            .then(x => { x++; return x; })
            .catch(e => { flag = true; });
        let promiseAll = Promise.all([promise7,promise8,promise9]);

        let valsPromises = await promiseAll;

        this.assert(valsPromises.length == 3);
        this.assert(valsPromises[0] == 11 && valsPromises[1] == 12 && valsPromises[2] == 13);
        return;
    }
    async retV1(s1,ms) {
        await sleep(ms);
        return s1;
    }
    returnFunc(ftype=null) {
        let f;

        if(ftype == null) {
            f = () => { return 2;}
        }
        else if(ftype == 1) {
            f = (x) => { return x;}
        }
        else {
            f = (x,y) => { return (x+y); };
        }
        return f;
    }
    testReturnFunc() {
        let v = this.returnFunc()();
        this.assert(v == 2);
        v = this.returnFunc(1)(2);
        this.assert(v == 2);
        v = this.returnFunc(2)(5,6);
        this.assert(v == 11);
    }
    testBase64OnBrowser() {
        let s = 'hello world';
        // this is not supported on node. use buffer.Buffer.from(s).toString
        let b64encoded = btoa(s);
        let b64decoded = atob(b64encoded);
        this.assert(s === b64decoded);
    }
    testBase64OnNode() {
        let s = 'hello world';
        let b64encoded = buffer.Buffer.from(s).toString('base64');
        let b64decoded = buffer.Buffer.from(b64encoded, 'base64').toString();
        this.assert(s === b64decoded);
    }
    test() {
        this.test1();
        this.testSleep();
        this.testAsync1();
        this.testTimeout1();
        this.testTimeout2SubAsync();
        this.testReturnAfterTimeoutPromise();
        this.testTimeoutUse();
        this.testAsync2();
        this.testAsync3();
        this.testAsync4();
        this.testAsync5();
        this.testPromise1();
        this.testReturnFunc();
        console.log('pass TestFunctions');
    }
}

function test() {
    let t = new TestBasic("c1");
    /*
    t.test_assert();
    t.test_array_map_set();
    t.test_string();
    t.test_control();
    t.test_map();
    t.test_numberFormat();
    t.testDate();
    t.test_random();
    */
    t.testBase64OnNode();
}
test();
