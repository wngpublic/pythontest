'use strict';
const buffer = require('buffer');
const assert = require('assert');
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

    constructor(v1) {
        this.v1 = v1;
        this.v2 = 100;
        console.log('TestBasic constructor ' + v1);
        this.ten = 10;
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

        // reverse string
        s = 'abcde';
        assert(s.split('').reverse().join('') === 'edcba');

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
        //console.log(s);
        a = '["abc","efg","ijk"]';
        s = JSON.stringify(a);
        //console.log(s);
        a = JSON.parse(s);
        //console.log(a);
        s = '[4,5,6]';
        a = JSON.parse(s);
        //console.log(a);
        //console.log(s);
        assert(typeof s === 'string');
        assert(typeof s !== 'object');
        s = "a798e&*(&(*";
        assert(typeof s === 'string');
        assert(typeof s !== 'object');
        assert(!(s instanceof String));
        assert(s.constructor === String);
        s = new String("a798e&*(&(*");
        assert(typeof s !== 'string');
        assert(typeof s === 'object');
        assert(s.constructor === String);
        assert(s instanceof String);

        let d = null, n = 123, so = new String('1234');
        s = "^&*!*@hkjsdha";
        a = ['abc','def'];
        d = {k1:'abc',k2:['v1','v2'],k3:{k31:'bcd',k32:['v31','v32']}};
        n = 123;
        assert(s.constructor === String);
        assert(s.constructor !== Array);
        assert(so.constructor === String);
        assert(so.constructor !== Array);
        assert(a.constructor === Array);
        assert(a.constructor !== String);
        assert(a.constructor !== Object);
        assert(d.constructor === Object);
        assert(d.constructor !== String);
        assert(d.constructor !== Array);
        assert(n.constructor === Number);
        assert(n.constructor !== String);
        assert(n.constructor !== Object);
        assert(d['k1'].constructor === String);
        assert(d['k2'].constructor === Array);
        assert(d['k3'].constructor === Object);
        assert(d['k3']['k31'].constructor === String);
        assert(d['k3']['k32'].constructor === Array);

        // convert string to hex
        s = 'hello there';
        assert(s.toString('base64') === 'hello there');
        assert(s.toString('base16') === 'hello there');
        let buffer = Buffer.from(s);
        assert(buffer.toString('hex') === '68656c6c6f207468657265');
        assert(buffer.toString('base64') === 'aGVsbG8gdGhlcmU=');
        assert(buffer.toString() === 'hello there');
        assert(buffer.toString('binary') === 'hello there');
        assert(buffer.toString('utf8') === 'hello there');
        assert(buffer.toString('utf-8') === 'hello there');
        console.log('pass test_string');
    }

    testRegex() {
        /*
        \bX         match X at beginning word boundary
        X\b         match X at end word boundary
        \BX         match X NOT at a word boundary
        //g         global
        //i         case insensitive
        //m         multiline
        //u         full unicode
        .*          0 or more
        .+          1 or more, greedy
        .*?         0 or more lazy
        .+?         1 or more lazy
        \d{n,m}     a digit n-m long
        \d{n,}      a digit at least m long
        \d{,m}      a digit at most m long, or \d{0,m} 
        \d{n}       a digit exactly n long
        [^A|B]      not A not B
        [A|B]       A or B
                    what is not A but is B?
                    what is A but not B?

        X(?=Y)      positive lookahead, look for X but match only if followed by Y, doesnt signify group
                    \d+(?=\s)(?=.*30)   digits followed by space followed by anything and a 30
                    \d+(?=(X|Y))
                    /A (?=B) C/.test('A C C') // false
                    /A (?=B) C/.test('A B C') // true

        X(?!Y)      negative look ahead, look for X but match only if not followed by Y, doesnt signify group
                    /A (?!B) C/.test('A C C') // true
                    /A (?!B) C/.test('A B C') // false

        (?<=Y)X     positive lookbehind, look for X but match only if it Y precedes it, doesnt signify group
                    /(?<=B) C/.test('A C C') // false
                    /(?<=B) C/.test('A B C') // true

        (?<!Y)X     negative look ahead, lool for X but match only if not preceded with Y, doesnt signify group
                    /(?<!B) C/.test('A C C') // true
                    /(?<!B) C/.test('A B C') // false

        \N          backreference in group
                    /(['"])(.*?)\1/g        \1 references result of group 1's (['""]) mirror
        \k<name>    backreference in group by name, alterative to \N
                    /(?<quote>['"])(.*?)\k<quote>/g     first group is named ?<quote>
        $$          for inserting character $, it can be \$ or $$ during replace

        (?:X)       non capturing group, where you need () for quantifier but do not capture the group.
                    eg  (go)+ captures go
                        (?:go)+ does not capture go

        replacement in line
        $2 $1       grouping usage
                    str.replace(/(\w+)\s+(\w+)/, '$2 $1');
        examples

        /<(.*?)>/       find beginning tag and end tag
        /a(z)?(c)?/     a followed by optional z followed by optional c, so "a" would match
        /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/
        s.replace(/(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/,'\k<day>-\k<month>-\k<year>')



        */
        let re2 = RegExp(/^(\w+)-(\d+\/\d+\.\d+)\s+.*/);
        re2 = /^(\w+)-(\d+\/\d+\.\d+)\s+(AAA|BBB)\s+.*/;
        let s = 'hello-123/456.222 AAA haskdhanmwqe';
        if(re2.test(s)) {
            console.log(`line match 2a`);
        }
        if(s.match(re2)) {
            console.log(`line match 2b`);
        }
        {
            let v = "<img tag=123 src=https://abc1.com>" + 
                    "<img tag=123 src=\"https://abc2.com>\"" + 
                    "<img tag=123 src=https://123abc234.com>";
            // look for first " ending group
            let group1 = v.match(/<img\s+.+\s+src="(http.+abc.+?)"/);
            // look backward and exclude \" but include first "
            let group2 = v.match(/<img\s+.+\s+src="(http.+abc.+?)(?<!\\")"/); 
            // capture everything between [] lazy
            // ? is optional (0 or 1, eg \d?) or lazy (repeat min number of times). in this context, it's lazy
            let group3 = v.match(/"tag":(\[.+?\])/); 
            let group4 = v.matchAll(/<img\s+.+\s+src="(http.+?)"/g);
            if(group4 !== null) {
                let arrayAll = Array.from(group4);
                for(let v1 of arrayAll) {
                    console.log(`group4: ${v1[1]}\n`);
                }
            }
        }
        {
            let v = 'A B';
            assert(/[^A]/.test('A B') === true);
            assert(/[^A|B]/.test('A B') === true);
            assert(/[^A|B]/.test('A') === false);
            assert(/[^A|B]/.test('AB') === false);
            assert(/[^A|^B]/.test('AB') === false);
            assert(/[^A|^B]/.test('AC') === true);
            assert(/[^A|^B]/.test('A B') === true); // because of space
            assert(/[^A|B]/.test('ABC') === true);
            assert(/[^A|B]/.test('A') === false);
            assert(/[^A|B]/.test('B') === false);
            assert(/[^B|A]/.test('B') === false);
            assert(/[^A|B]/.test('A B C') === true);
            assert(/[A|^B]/.test('A B C') === true);
            assert(/[A|^B]/.test('A B') === true);
            assert(/[A|^B]/.test('A C') === true);
            assert(/[A|^B]/.test('A') === true);
            assert(/[A|^B]/.test('B') === true);    // why is this A or NOT B?
            assert(/[A|^B]/.test('C') === false);
            assert(/[A|B]/.test('C') === false);
        }
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

        d = { 'k1':'v1', 'k2':'v2' };
        let keys = Object.keys(d);
        let ctr = 0;
        this.assert(keys.constructor === Array);
        for(let k of keys) {
            ctr++;
            this.assert(!(k in keys));
            this.assert(k in d);
            this.assert(keys.includes(k));
            this.assert(!keys.hasOwnProperty(k));
        }
        this.assert(ctr == 2);


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

        let sz = 3;
        a = new Array(sz);
        for(let i = 0; i < sz; i++) {
            a[i] = new Array(2);
            for(let j = 0; j < 2; j++) {
                a[i][j] = (j+i*sz);
            }
        }
        buf = [];
        for(let i = 0; i < a.length; i++) {
            buf.push(a[i].join(','));
        }
        v = buf.join(',');
        assert(v === '0,1,3,4,6,7');

        a = new Array(sz);
        for(let i = 0; i < sz; i++) {
            a[i] = new Array(2);
            a[i].fill(0);               // fill array with all 0
        }
        buf = [];
        for(let i = 0; i < a.length; i++) {
            buf.push(a[i].join(','));
        }
        v = buf.join(',');
        assert(v === '0,0,0,0,0,0');

        a = [1,2,3];
        a1 = a.map(x => x * 2);
        assert(a1.join(',') === '2,4,6');
        a = Array.of(2,3,4,5,6,7);
        assert(a.join(',') === '2,3,4,5,6,7');
        a1 = a.filter(x => x > 3 && x % 2 == 0);
        assert(a1.join(',') === '4,6');
        a1 = a.slice(3,5);
        assert(a1.join(',') === '5,6');
        a1 = a.slice(3);
        assert(a1.join(',') === '5,6,7');

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

        a = [1,2,3];
        d = { k1: [1,2,3], k2: "abc" };
        v = 'hello';
        i = 23;
        let fp = 3.14;
        let f = this.hello;
        s = new String('hello');

        assert(Array.isArray(a));
        assert(typeof a === 'object');
        assert(typeof d === 'object');
        assert(typeof v === 'string');
        assert(typeof v !== 'object');
        assert(typeof i === 'number');
        assert(typeof fp === 'number');
        assert(typeof f === 'function');
        assert(typeof s === 'object');

        assert(a instanceof Array);
        assert(a instanceof Object);
        assert(d instanceof Object);
        assert(this instanceof TestBasic);
        assert(!(v instanceof Object));
        assert(!(v instanceof String));
        assert(s instanceof String);

        assert(s == v);
        assert(s !== v);
        assert(d.length === undefined);
        assert((Object.keys(d).length) === 2);
        assert((Object.keys(v).length) === 5);
        assert(a.length === 3);
        assert(v.length === 5);

        {
            let json = {
                data: {
                    k1: 'v1',
                    k2: 'v2'
                }
            }
            assert('data' in json && json.hasOwnProperty('data'));
            assert(!('data1' in json) && !(json.hasOwnProperty('data1')));

        }
        console.log('pass test_map');
    }
    testDictRemoveInLoop() {
        let  d = {};
        for(let i = 0; i < 10; i++) {
            d[i] = i;
        }
        let state = 0;
        assert(Object.keys(d).length === 10);
        while(Object.keys(d).length !== 0) {
            for(let [k,v] of Object.entries(d)) {
                if(state === 0) {
                    if(k % 2 == 0) {
                        delete d[k];
                    }
                } else {
                    delete d[k];
                }
            }
            if(state === 0){
                assert(Object.keys(d).length === 5);
            }
            state++;
        }
        assert(Object.keys(d).length === 0);
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
    async testTimeoutCase3() {
        
    }

    async testTimeout() {
        //this.testTimeoutCase1();
        //this.testTimeoutCase2();
        this.testTimeoutCase3();
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
    multiply(x,y) {
        return x * y;
    }
    factor(x) {
        return n => n * x;
    }
    wrapNumber(x) {
        return () => x;
    }
    testClosure() {
        let f1 = this.wrapNumber(10);
        let f2 = this.wrapNumber(20);
        this.assert(f1() == 10);
        this.assert(f2() == 20);
        let f3 = this.factor;
        let f4 = this.factor(2);
        let f5 = f4(3);
        this.assert(f3(2)(3) == 6);
        this.assert(f3(3)(4) == 12);
        this.assert(f4(1) == 2);
        this.assert(f4(3) == 6);
        this.assert(f4(4) == 8);
        this.assert(f5 == 6);
    }
    getV2() {
        return this.v2;
    }
    testBind() {
        let cb1 = this.getV2;
        let cb1Bind = this.getV2.bind(this);
        let flag = false;
        let v = null;
        try {
            v = cb1();
        } catch(e) {
            flag = true;
        }
        this.assert(flag);
        this.assert(v === null);

        try {
            flag = false;
            v = cb1Bind();
        } catch(e) {
            flag = true;
        }
        this.assert(flag == false);
        this.assert(v === 100);
    }
    static testReturnStatic(v) {
        return v;
    }
    testReturnNonStatic(v) {
        return v;
    }
    testInnerFunction() {
        function testReturnNonStatic(v) {
            return v + 1;
        }

        function tcUnbinded() {
            let assert = require('assert');
            let v1 = testReturnNonStatic(10);
            assert(v1 === 11);

            let flag = false;
            try {
                let v2 = this.testReturnNonStatic(10);
            } catch (e) {
                flag = true;
            } finally {
                assert(flag);   // non binded doesnt have this keyword
            }

            try {
                flag = false;
                let v2 = TestBasic.testReturnStatic(10);
            } catch (e) {
                flag = true;
            } finally {
                assert(!flag); // non binded can use a class static function
            }
        }

        function tcBinded() {
            let v1 = testReturnNonStatic(10); // can still access inner function
            this.assert(v1 === 11);

            let flag = false;
            let v2 = null;
            try {
                v2 = this.testReturnNonStatic(10);
            } catch (e) {
                flag = true;
            } finally {
                this.assert(v2 === 10); // this is binded
                this.assert(!flag);
            }

            try {
                v2 = null;
                flag = false;
                v2 = TestBasic.testReturnStatic(10);
            } catch (e) {
                flag = true;
            } finally {
                this.assert(v2 === 10);
                this.assert(!flag);
            }
        }

        tcUnbinded();
        let cbTcBinded = tcBinded.bind(this);
        cbTcBinded();
    }
    async testStringFunction() {
        // string to function, function to string
        let sf0 = 'function f() { return 10; }';
        let sf1 = 'function f(i1) { return i1+10; }';
        let sf2 = '(i1) => i1+10';
        let sf3 = '{ "f1": "function f() { return 10; }", "f2": "function(x) { return x + 10; }" }';
        let jsonf3 = JSON.parse(sf3);
        let f0 = eval(sf0);
        let f1 = new Function('x', 'return x+10');
        let f2 = new Function(sf0)();
        let f4 = function fx() { return 10; };
        let sf4 = f4.toString();
        let sf4f1 = Function(sf4);
        let sf4f2 = Function(sf4)();
        let sf4f3 = new Function(sf4);
        let sf4f4 = new Function(sf4)();

        function func1() { return 10; }
        function func2(x,y) { return x+y+10; }
        let f5 = function() { return 10; };
        let sf5 = f5.toString();

        //let sf5f1 = new Function(sf5);
        //let sf5f2 = Function(sf5)();
        //let sf5f3 = new Function(sf5);
        //let sf5f4 = new Function(sf5)();

        let f6 = func1;
        let sf6 = f6.toString();
        let f6f1 = new Function('return ' + sf6)(); // this works!
        let f6f2 = new Function(sf6)(); // this doesnt work! needs return

        //let f6f3 = Function('return' + sf6)(); // throws error

        let f7 = func2;
        let sf7 = f7.toString();
        let f7f1 = new Function(...arguments, 'return ' + sf7)(); // this works!
        let f7f2 = new Function('return ' + sf7)(); // this works!
        let f8f1 = new Function(...arguments, 'return ' + sf1)(); // this works!
        let f9f1 = new Function('return ' + sf0)(); // this works!

        assert(f6f1() == 10);   // this works
        assert(f7f1(20,30) == 60);   // this works
        assert(f7f2(20,30) == 60);   // this works
        assert(f8f1(20) == 30);   // this works
        assert(f9f1() == 10);   // this works

        assert(sf4f1() == undefined);

        assert(f4() === 10);
        assert(f5() === 10);
    }

    addThisVar(x) {
        return (x + this.ten);
    }
    thisCallback(cb) {
        return cb(1);
    }
    testBindMethod() {
        let bindThis = (this.addThisVar).bind(this);
        this.assert(this.thisCallback(bindThis) == 11);
        let flag = false;
        try {
            
            this.assert(this.thisCallback(this.addThisVar) != 11);
        } catch(e) {
            if(e instanceof TypeError) {
                flag = true;
            }
        }
        this.assert(flag == true);
    }
    testNestedFunctions() {
        function f1(a,b) {
            function f2(a,b) {
                return (a+b);
            }
            return f2(a,b);
        }
        this.assert(f1(1,2) == 3);
    }
    jsonDiff(jold,jnew) {
        function jsonDiffTracker(jold,jnew,tracker) {
            
        }
        const tracker = {};
        jsonDiffTracker(jold,jnew,tracker);
        return tracker;
    }
    testDiff() {
        let lold = [1,2,3];
        let lnew = [2,3,4];
        let mold = {
            k1: "v1",
            k2: ["v21","v22","v23"],
            k3: {
                k31: "v31",
                k32: ["v321","v322","v333"],
                k33: {
                    k331: "v331",
                    k332: ["v3321","v3322","v3333"]
                },
                k34: 42
            },
            k4: 42
        };
        let mnew = {
            k1: "v1",
            k2: ["v22","v23","v24"],
            k3: {
                k31: "v311",
                k32: ["v322","v323","v334"],
                k33: {
                    k331: "v332",
                    k332: ["v3333","v3324","v3335"]
                },
                k34: 43
            },
            k4: 45
        };
    }
    testJsonOps() {
        let j1 = {
            k1: "v1",
            k2: ["v21","v22","v23"],
            k3: {
                k31: "v31",
                k32: ["v321","v322","v333"],
                k33: {
                    k331: "v331",
                    k332: ["v3321","v3322","v3333"]
                },
                k34: 42
            },
            k4: 42
        };
        let j2 = {
            "k1": "v1",
            "k2": ["v21","v22","v23"],
            "k3": {
                "k31": "v31",
                "k32": ["v321","v322","v333"],
                "k33": {
                    "k331": "v331",
                    "k332": ["v3321","v3322","v3333"]
                },
                "k34": 42
            },
            k4: 42
        };
        let bufk = [];
        let bufv = [];
        for(let [k,v] of Object.entries(j1)) {
            bufk.push(k);
            bufv.push(v);
        }
        this.assert(bufk.join() === 'k1,k2,k3,k4');
        this.assert(bufk.length === 4);
        bufk = [];
        bufv = [];
        this.assert(bufk.length === 0);
        for(let [k,v] of Object.entries(j1['k3'])) {
            bufk.push(k);
            bufv.push(v);
        }
        this.assert(bufk.join() === 'k31,k32,k33,k34');
        this.assert('k1' in j1);
        this.assert('k31' in j1['k3']);
        this.assert(!('k9' in j1));
        this.assert(!('k99' in j1['k3']));

        let s1 = "hello";
        let s2 = new String("hello");
        let s3 = "hello";
        let s4 = new String("hello");
        this.assert(!(s1 instanceof String));
        this.assert((s2 instanceof String));
        this.assert(typeof s1 === 'string');
        this.assert(s1 === "hello");
        this.assert(s2 !== "hello");
        this.assert(s2 == "hello");
        this.assert(s1 !== s2);
        this.assert(s1 === s3);
        this.assert(s2 !== s4);
        this.assert(s2 != s4);
        
        this.assert(typeof j1['k1'] === 'string');
        this.assert(typeof j1['k1'] !== 'object');
        this.assert(!(j1['k1'] instanceof String));

        this.assert(Array.isArray(j1['k2']));
        this.assert(j1['k2'] instanceof Array);
        this.assert(typeof j1['k2'] === 'object');

        this.assert(j1['k3'] instanceof Object);
        this.assert(typeof j1['k3'] === 'object');

        this.assert(typeof j1['k4'] === 'number');
    }
    testUint8Array() {
        
    }
    testByteBuffer() {
        
    }
    testInnerFunctions() {
        class C {
            ID = 0;
            constructor(k,v1,v2) {
                this.id = C.ID++;
                this.k = k;
                this.v1 = v1;
                this.v2 = v2;
            }
        }
        class C1 extends C {
            constructor(k,v1,v2,v3) {
                super(k,v1,v2);
                this.v3 = v3;
            }
            add() {
                return this.v1 + this.v1 + this.v2;
            }
        }
        function iF1(cb) {
            let c = new C('k1',10,20);
            C.prototype.add = function() {
                return this.v1 + this.v2;
            };
            C.prototype.mul = function() {
                return this.v1 * this.v2;
            };
            let v = c.add();
            assert(v === 30);
            v = cb(v);
            assert(v === 60);

            let c1 = new C1('k1',10,20,30);
            v = c1.add();
            assert(v === 40);
            C1.prototype.add = function() {
                return this.v1 + this.v2;
            };
            v = c1.add();
            assert(v === 30);
            v = cb(v);
            assert(v === 60);
        }
        function iF2(x) {
            function iiF1(x) {
                return x * 2;
            }
            return iiF1(x);
        }
        iF1(iF2);
    }
    test() {
        /*
        this.test1();
        this.testSleep();
        this.testAsync1();
        this.testTimeout1();
        this.testTimeout2SubAsync();
        this.testReturnAfterTimeoutPromise();
        this.testAsync2();
        this.testAsync3();
        this.testAsync4();
        this.testAsync5();
        this.testPromise1();
        this.testReturnFunc();
        this.test_assert();
        this.test_control();
        this.test_map();
        this.test_numberFormat();
        this.testDate();
        this.test_random();
        this.testBase64OnNode();
        this.testClosure();
        this.testBind();
        this.testInnerFunction();
        this.test_array_map_set();
        this.testStringFunction();
        this.testTimeout();
        this.testUint8Array();
        this.testByteBuffer();
        this.test_string();
        this.testDictRemoveInLoop();
        this.testRegex();
        */
        this.testInnerFunctions();
        console.log('pass TestFunctions');
    }
}

function test() {
    /*
    t.test_assert();
    t.test_array_map_set();
    t.test_string();
    t.test_control();
    t.test_map();
    t.test_numberFormat();
    t.testDate();
    t.test_random();
    t.testBase64OnNode();
    t.testBindMethod();
    t.testJsonOps();
    t.testNestedFunctions();
    */
    let t = new TestBasic("c1");
    t.test();
}
test();
