const yargs = require('yargs');
const args = yargs.argv;
const https = require('https');
const http = require('http');
const fetch = require('node-fetch');
const crypto = require('crypto');
const assert = require('assert');
const { consolelib } = require('console');
const { pathlib } = require('path');
const zlib = require('zlib');
const fs = require('fs');
const stream = require('stream');
const util = require('util');
const jsdom = require('jsdom');
const xml2js = require('xml2js');
const axios = require('axios').default;

const charslc = 'abcdefghijklmnopqrstuvwxyz';
const charsuc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const charsn  = '0123456789';
const charsp  = '~!@#$%^&*(){}[]|';
const alphanum = charslc + charsuc + charsn;
const DEBUG   = 1;
const events = require('events');
const { textChangeRangeIsUnchanged } = require('typescript');

function debug(s) {
    if(DEBUG === 0) {
        return;
    }
    console.log(s);
}

class MyAsync {
    constructor(id) {
        this.id = id;
        var assert = require('assert');
    }
    addItemsSleep(x,y) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                let z = x+y;
                let a = 0;
                for(let i = 0; i < 10000000; i++) {
                    a += 1;
                }        
                let error = false;
                if(z % 2 == 0) {
                    error = true;
                }
                if(error) {
                    reject('error, was mod % 2 == 0');
                }
                else {
                    resolve(z);
                    }
            }, 1000);
        });
    }
    
    resolve(z) {
        console.log(`result is ${z}`);
        return Date.now();
    }

    // async does not need .then
    async addItemsAsync(x, y) {
        let msBeg = Date.now();

        await new Promise((resolve, reject) => setTimeout(() => {
            let z = x+y;
            let a = 0;
            for(let i = 0; i < 10000000; i++) {
                a += 1;
            }        
            let error = false;
            if(z % 2 == 0) {
                error = true;
            }
            if(error) {
                reject('error, was mod % 2 == 0');
            }
            else {
                resolve(z);
            }
        }, 1000));

        let msEnd = Date.now();
        console.log(`vdate5 ${msBeg} -> \n       ${msEnd}`);

    };

}
class TestAsync {
    constructor() {
        this.myasync = new MyAsync();
        this.jsonpayload1 = {
            'k1':'v1',
            'k2':{
                'k2.1':'v2.1',
                'k2.2':'v2.2'
            },
            'k3':['v3.1','v3.2']
        };
        this.jsonpayload1str = JSON.stringify(this.jsonpayload1);
        this.gvarint1 = 100;
        this.gvarint2 = 200;
        this.emitter = new events.EventEmitter();
    }
    test1() {
        let msBeg = Date.now();
        //outside = this;
        this.myasync.addItemsSleep(10,11)
            .then(result => this.myasync.resolve(result))
            .then(ms => { 
                let msNow = Date.now(); 
                console.log(`vdate2 ${msNow}`);
                console.log('----------------------1');
            })
            .catch(e => console.log(e));
        let msEnd = Date.now();
        let msDif = msEnd - msBeg;
        console.log(`vdate1 ${msBeg} -> \n       ${msEnd}`);
        
        console.log('----------------------2');
        this.myasync.addItemsAsync(10,11);
    }
    test2() {
        const fs = require('fs');
        console.log(`${__dirname}`);
        const fname = '../main/input/testinputsmall.json';
        // this is async, but you cannot await, cannot .then()
        fs.readFile(fname, (err,data) => {  
            if(err) {
                console.log(`err: ${err}`);
            } else {
                //console.log(`ok: ${data}`);
                console.log(`file read done`);
            }
        });
        // test2.1 will output first because of async
        console.log('test2.1');
    }
    test3() {
        const fs = require('fs');
        const fname = 'tmp/out.1.txt';
        // this is async
        if(!fs.existsSync('./tmp')) {
            fs.mkdir('./tmp', (err) => {
                if(err){
                    console.log(err);
                } else {
                    fs.writeFile(fname, 'hello world', () => console.log('file write done'));
                }
            });
        } else {
            fs.writeFile(fname, 'hello world', () => console.log('file write done'));
        }
        // test3.1 will output first because of async
        console.log('test3.1');
    }
    test4() {
        const fs = require('fs');
        const fname = '../main/input/testinputlarge.json';
        const readStream = fs.createReadStream(fname, { encoding: 'utf8' });

        // listen on data chunk event and get it as chunk
        readStream.on('data',(chunk) => {

        });
        // read streams
    }
    async testMakeHttpRequestGet1() {
        let flag = false;
        try {
            const url = 'http://localhost:3000/getjson1/v1/v2';
            const res = await fetch(url);
            const dat = await res;
            console.log(dat.headers);
            //console.log(res.then(r => r.text()));
        } catch(e) {
            console.log(e);
            throw new e;
        }
    }
    async testMakeHttpRequestPost1() {
        // curl -X POST 'localhost:3000/postjson1/v1/v2' -d '{ "k1":"v1","k2":"v2" }' -H 'Content-Type: application/json'
        try {
            const url = 'http://localhost:3000/postjson1/v1/v2';
            const headers = {
                'Accept': 'application/json',
                'Content-Type':'application/json'
            };
            const bodyJSONData = {
                'k1':'v1',
                'k2':'v2'
            };
            const bodyJSONStr = JSON.stringify(bodyJSONData);
            const res = await fetch(url, { method:'POST', headers: headers, body: bodyJSONStr });   // body cannot be json
            const dat = await res.json();
            const jsonStr = JSON.stringify(dat);
            console.log(`post example: ${jsonStr}`);
        } catch(e) {
            console.log(e);
            throw new e;
        }
    }

    testAsync() {
        this.test1();
        ctr++;
        console.log(`|-----------------------${ctr}`);
        
        this.test2();
        ctr++;
        console.log(`|-----------------------${ctr}`);
        
        this.test3();
        ctr++;
        console.log(`|-----------------------${ctr}`);
    }
    testJson1(){
        let jsonstr = this.jsonpayload1str;
        let json = this.jsonpayload1;
        console.log(json);
    }
    testBloomFilterSerdes() {
        const numBitsAllocate = 256 * 256;
        const numHashFunctions = 4;
        let bf1 = new bloomfilter.BloomFilter(numBitsAllocate,numHashFunctions);
        const numCases = 10000;
        for(let i = 0; i < numCases; i++) {
            const s = `value_${i}`;
            bf1.add(s);
        }
        for(let i = 0; i < numCases; i++) {
            const s = `value_${i}`;
            assert(bf1.test(s));
        }
        const max = numCases * 10;
        let numFalsePositives = 0;
        for(let i = numCases; i < max; i++) {
            const s = `value_${i}`;
            if(bf1.test(s)) {
                numFalsePositives++;
            }
        }
        let ratioFalsePositives = numFalsePositives/max;
        console.log(`ratio falsePositives1 ${numBitsAllocate} ${numHashFunctions} ${ratioFalsePositives}`);

        let serializedObject = JSON.stringify(bf1);
        let deserializedObject = JSON.parse(serializedObject);
        let bf2 = Object.create(bloomfilter.BloomFilter.prototype, Object.getOwnPropertyDescriptors(deserializedObject));

        numFalsePositives = 0;
        for(let i = numCases; i < max; i++) {
            const s = `value_${i}`;
            if(bf2.test(s)) {
                numFalsePositives++;
            }
        }
        ratioFalsePositives = numFalsePositives/max;
        console.log(`ratio falsePositives2 ${numBitsAllocate} ${numHashFunctions} ${ratioFalsePositives}`);
    }
    testBloomFilter() {
        const bloomfilter = require('bloomfilter');
        let assert = require('assert');
        

        for(let factor = 1; factor < 1024; factor *= 2) {
            for(let hashFactor = 1; hashFactor < 32; hashFactor *= 2) {
                for(let numItems = 16; numItems < 512; numItems *= 2) {
                    //const numBitsAllocate = 256 * 256; // 64k
                    const numBitsAllocate = 256 * factor;
                    const numHashFunctions = hashFactor;
                    let bf1 = new bloomfilter.BloomFilter(numBitsAllocate,numHashFunctions);
                    for(let i = 0; i < numItems; i++) {
                        const s = `value_${i}`;
                        bf1.add(s);
                    }
                    for(let i = 0; i < numItems; i++) {
                        const s = `value_${i}`;
                        assert(bf1.test(s));
                    }
                    const max = numItems * 10;
                    let numFalsePositives = 0;
                    for(let i = numItems; i < max; i++) {
                        const s = `value_${i}`;
                        if(bf1.test(s)) {
                            numFalsePositives++;
                        }
                    }
                    let ratioFalsePositives = numFalsePositives/max;
                    let serializedObject = JSON.stringify(bf1);
                    let szSerialized = serializedObject.length;
                    let s = `ratio falsePositives1 ` + 
                        `${numItems.toString().padStart(8,' ')} ` + 
                        `${numBitsAllocate.toString().padStart(8,' ')} ` + 
                        `${numHashFunctions.toString().padStart(8,' ')} ` + 
                        `${szSerialized.toString().padStart(8,' ')} ` + 
                        `${ratioFalsePositives.toFixed(5).toString().padStart(8,' ')}`;
                    //console.log(s);
                }
            }
        }
    }
    testCrypto() {
        const secret = 'helloworld';
        let v = 'the cat in the hat';
        const hash = crypto.createHmac('sha256', secret).update(v).digest('hex');
        console.log(hash);
    }
    test2() {
        this.testBloomFilter();
        this.testCrypto();
    }
    test3() {
        let s = 'this is a string\n' + 'another line\n' + 'final line\n';
        let lines = s.split('\n');
        let ctr = 0;
        // this shows numbers
        for(let line in lines) {
            console.log(`${ctr.toString().padStart(5,' ')} ${line}`);
            ctr++;
        }

        ctr = 0;
        // this shows the values
        for(let line of lines) {
            console.log(`${ctr.toString().padStart(5,' ')} ${line}`);
            ctr++;
        }
    }
    test4() {
        let re1 = RegExp(/^(\d+\.\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+\.\d+):\s+[POST|GET]\s+([\w\d\/]+)\s+HTTP.*/);
        //       1                         2                             3            4
        re1 = /^(\d+\.\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+\.\d+)\:\s+(POST|GET)\s+([\w\/]+)\s+HTTP\/1.1/;
        let s  = '010.031.051.120.53378-010.131.136.331.08000: POST /x/i/b65/foo HTTP/1.1';
        let s1 = '010.032.0a9.150.51378-010.161.16b.131.08000: POST /x/i/b67/foo HTTP/2.0';
        if(re1.test(s)) {
            console.log(`line match 1a`);
        }
        if(s.match(re1)) {
            console.log(`line match 1b`);
        }

        let res = re1.exec(s);
        if(res) {
            console.log(`${res.length},${res[1]},${res[2]},${res[3]},${res[4]}`);
        } else {
            console.log('res1 is null');
        }
        res = re1.exec(s1);
        if(res) {
            console.log(`${res.length},${res[1]},${res[2]},${res[3]},${res[4]}`);
        } else {
            console.log('res2 is null');
        }

        re1 = /^((\d+\.){4}(\d+))-((\d+\.){4}(\d+))\:\s+(POST|GET)\s+([\w\/]+)\s+HTTP.*/;
        if(re1.test(s)) {
            console.log(`line match 1c`);
        }
        if(s.match(re1)) {
            console.log(`line match 1d`);
        }

        let re2 = RegExp(/^(\w+)-(\d+\/\d+\.\d+)\s+.*/);
        re2 = /^(\w+)-(\d+\/\d+\.\d+)\s+(AAA|BBB)\s+.*/;
        s = 'hello-123/456.222 AAA haskdhanmwqe';
        if(re2.test(s)) {
            console.log(`line match 2a`);
        }
        if(s.match(re2)) {
            console.log(`line match 2b`);
        }
        {
            let v = "";
            // look for first " ending group
            let group1 = v.match(/<img\s+.+\s+src="(http.+abc.+?)"/);
            // look backward and exclude \" but include first "
            let group2 = v.match(/<img\s+.+\s+src="(http.+abc.+?)(?<!\\")"/); 
            // capture everything between [] lazy
            let group3 = v.match(/"tag":(\[.+?\])/); 
            let group4 = v.matchAll(/<img\s+.+\s+src="(http.+?)"/g);
            if(group4 !== null) {
                let arrayAll = Array.from(group4);
                for(let v1 of arrayAll) {
                    console.log(`group4: ${v1[1]}\n`);
                }
            }
        }
    }
    async testAxiosFiles() {
        let enable = false;
        if(enable)
        {
            let filename = 'file.pdf';
            axios({
                method: 'get',
                url: `https://www.website.com/${filename}`,
                responseType: 'stream'
            })
            .then((r) => {
                r.data.pipe(fs.createWriteStream(filename));
            });
        }
        if(enable)
        {
            let p = new Promise((resolve, reject) => {
                let filename = 'file.pdf';
                const writer = createWriteStream(filename);
                axios({
                    method: 'get',
                    url: `https://www.website.com/${filename}`,
                    responseType: 'stream'
                })
                .then((r) => {
                    return new Promise((resolve1,reject1) => {
                        r.data.pipe(writer);
                        let error = null;
                        writer.on('error', (e) => {
                            error = e;
                            writer.close();
                            reject(e);
                        });
                        writer.on('close', () => {
                            if(error === null) {
                                resolve();
                            }
                        });
                    });
                });
            });
            let result = await p;
        }
    }
    async testJSDOM() {
        let v = "";
        let dom = new jsdom.JSDOM(v);
        let collection = dom.window.document.getElementsByTagName('script');
        for(let i = 0; i < 100; i++) {
            let item = collection.item(i);
            if(item === null) {
                break;
            }
            let contents = item.text;
            if(contents.match(/tag/)){
                let group1 = contents.match(/"tag":(\[.+?\])/);
                if(group1 !== null) {
                    let list = JSON.parse(group1[1].trim().replace(/\n/,''));
                }
            }
        }
    }
    iSaidSomething1() {
        let s = "i said something";
        return s;
    }
    iSaidNothing1() {
        let s = `i said nothing`;
        return s;
    }
    whatDidISay1() {
        let s = `what did i say?`;
        return s;
    }
    iSaidSomethingAppend(vin) {
        let s = `i said something and ${vin}`;
        return s;
    }
    iSaidNothing2Append(vin) {
        let s = `i said nothing and ${vin}`;
        return s;
    }
    whatDidISay2Append(vin) {
        let s = `what did i say and ${vin}?`;
        return s;
    }
    async iSaidSomethingDelayReturn(timeoutValue) {
        let waitingDone = false;
        let r = setTimeout(() => {
            waitingDone = true;
            return 100;
        }, timeoutValue);
        assert(waitingDone === false);
        assert(typeof r === 'object');
        assert(r instanceof Object);    // r is handler to use for clearTimeout
        assert(!(r instanceof Promise)); 

        let v = await r;
        assert(typeof r === 'object');
        assert(r instanceof Object);    // r is handler to use for clearTimeout
        assert(v !== 100);
        assert(waitingDone === false);
        return "i said something";
    }
    async iSaidSomethingDelayReturnPromise(timeoutValue) {
        let t1 = Date.now();
        let waitingDone = false;
        let r = setTimeout(() => {
            waitingDone = true;
            return 100;  // this doesnt return capture, you need to do in callback to return
        }, timeoutValue);
        assert(waitingDone === false);
        assert(typeof r === 'object');
        assert(r instanceof Object);    // r is handler to use for clearTimeout
        assert(!(r instanceof Promise)); 
        let p = new Promise((resolve, reject) => { resolve(r); });
        assert(p instanceof Promise);
        let v = await p;        
        let t2 = Date.now();
        assert((t2-t1) < timeoutValue); // this doesnt elapse timeoutValue
        assert(typeof v === 'object');
        assert(v instanceof Object);    // r is handler to use for clearTimeout
        assert(v !== 100);
        assert(waitingDone === false);

        let externalValue = 100;
        let waitingDone2 = false;
        let p2 = new Promise((resolve, reject) => {
            setTimeout(() => {
                waitingDone2 = true;
                resolve(externalValue);
            }, timeoutValue);
        })
        assert(p2 instanceof Promise);
        let v2 = await p2;
        let t3 = Date.now();
        assert((t3-t2) >= 1000);    // this actually waits
        assert(v2 === 100);
        assert(waitingDone2 === true);
        assert(waitingDone === true);   // this is because of the second promise

        return "i said something";
    }
    async testPromise1() {
        let resolve = Promise.resolve();
        let r = resolve
            .then(() => this.iSaidSomething1())
            .then(() => this.iSaidNothing1())
            .then(() => this.whatDidISay1())
            .catch(e => console.log(`i got error ${e}`));
        assert(r instanceof Object);
        assert(r instanceof Promise);
        let v = await r;
        assert(typeof v === 'string');
        assert(v === 'what did i say?');
    }
    async testPromise2() {
        let resolve = Promise.resolve();
        let s = 'hello';
        let r = resolve
            .then(() => this.iSaidSomethingAppend(s))
            .then((s) => this.iSaidNothing2Append(s))
            .then((s) => this.whatDidISay2Append(s))
            .catch(e => console.log(`i got error ${e}`));
        assert(r instanceof Object);
        assert(r instanceof Promise);
        let v = await r;
        assert(typeof v === 'string');
        assert(v === 'what did i say and i said nothing and i said something and hello?');
    }
    async testPromise3() {
        let s = 'hello';
        let r = new Promise((resolve, reject) => resolve())
            .then(() => this.iSaidSomethingAppend(s))
            .then((s) => this.iSaidNothing2Append(s))
            .then((s) => this.whatDidISay2Append(s))
            .catch(e => console.log(`i got error ${e}`));
        assert(r instanceof Object);
        assert(r instanceof Promise);
        let v = await r;
        assert(typeof v === 'string');
        assert(v === 'what did i say and i said nothing and i said something and hello?');
    }
    async testPromise4() {
        let s = 'hello';
        let r = new Promise((resolve, reject) => resolve(this.iSaidSomethingAppend(s)))
            .then((s) => this.iSaidNothing2Append(s))
            .then((s) => this.whatDidISay2Append(s))
            .catch(e => console.log(`i got error ${e}`));
        assert(r instanceof Object);
        assert(r instanceof Promise);
        let v = await r;
        assert(typeof v === 'string');
        assert(v === 'what did i say and i said nothing and i said something and hello?');
    }
    async testPromise5() {
        let s = 'hello';
        let r = new Promise((resolve, reject) => resolve(this.iSaidSomethingAppend(s)))
            .then((s) => this.iSaidNothing2Append(s))
            .then((s) => this.whatDidISay2Append(s))
            .catch(e => console.log(`i got error ${e}`));
        let v = await r;
        assert(r instanceof Object);
        assert(r instanceof Promise);
        assert(typeof s === 'string');
        assert(v === 'what did i say and i said nothing and i said something and hello?');
    }
    async testPromise6() {
        let s = 'hello';
        let r = await new Promise((resolve, reject) => resolve(this.iSaidSomethingAppend(s)))
            .then((s) => this.iSaidNothing2Append(s))
            .then((s) => this.whatDidISay2Append(s))
            .catch(e => console.log(`i got error ${e}`));
        assert(typeof r === 'string');
        assert(typeof r !== 'String');
        assert(typeof r !== String);
        assert(!(r instanceof String));
        assert(!(r instanceof Object));
        assert(!(r instanceof Promise));
        assert(r === 'what did i say and i said nothing and i said something and hello?');
    }
    async testPromise7() {
        let s = 'hello';
        let r = new Promise((resolve, reject) => resolve(this.iSaidSomethingAppend(s)))
            .then((s) => this.iSaidNothing2Append(s))
            .then((s) => this.whatDidISay2Append(s))
            .catch(e => console.log(`i got error ${e}`));
        let v = await r;
        assert(r instanceof Promise);
        assert(typeof v === 'string');
        assert(v === 'what did i say and i said nothing and i said something and hello?');
    }
    async testTimeoutDelay(timeoutValue) {
        let t1 = Date.now();
        let r = this.iSaidSomethingDelayReturn();
        let t2 = Date.now();
        assert((t2-t1) < timeoutValue);
        assert(!(typeof r === 'string'));
        try {
            assert(r instanceof Promise);
            let v = await r;
            let t3 = Date.now();
            assert((t3-t2) < timeoutValue);
            assert(typeof v === 'string');
            assert(v === 'i said something');
    
        } catch(e) {
            console.log(e);
        }
    }
    async testTimeoutDelayPromise(timeoutValue) {
        let t1 = Date.now();
        let r = this.iSaidSomethingDelayReturnPromise(timeoutValue);
        let t2 = Date.now();
        assert((t2-t1) < timeoutValue);
        assert(!(typeof r === 'string'));
        try {
            assert(r instanceof Promise);
            let v = await r;
            let t3 = Date.now();
            assert((t3-t2) >= timeoutValue);
            assert(typeof v === 'string');
            assert(v === 'i said something');
    
        } catch(e) {
            console.log(e);
        }
    }
    async testTimeoutCaseAddClassVar(x) {
        let v = x + this.gvarint1;
        return v;
    }
    async assertExpected(exp,act) {
        console.log(`assert ${exp} === ${act}`);
        assert(exp === act);
    }
    async testTimeoutCases(timeoutValue) {
        let localVar1 = null;
        assert(this.gvarint2 === 200);
        let handle1 = setTimeout(async (x) => {
            this.gvarint2 = await this.testTimeoutCaseAddClassVar(x);
        }, timeoutValue, 50);
        assert(this.gvarint2 === 200);

        let promise = new Promise((resolve, reject) => resolve(null), timeoutValue);
        await promise;
        assert(this.gvarint2 === 200);


        let cb = this.testTimeoutCaseAddClassVar.bind(this);
        handle1 = setTimeout((x) => {
            var y = cb(x);
            this.gvarint2 = y;
        }, timeoutValue, 50);

        assert(this.gvarint2 === 200);

        promise = new Promise((resolve, reject) => resolve(null), timeoutValue);
        await promise;


        handle1 = setTimeout(async () => { this.assertExpected(150, this.gvarint2); }, timeoutValue, 150, this.gvarint2);
        assert(this.gvarint2 === 200);
    }
    assertGvarint2(exp) {
        assert(this.gvarint2 === exp);
    }
    getGvarint2() {
        return this.gvarint2;
    }
    async testTimeoutSimple(timeoutValue) {
        let handle = null;
        let handle2 = null;
        let flag = false;
        let t1=null,t2=null,t3=null,t4=null,t5=null,t6=null;
        let promise1=null,promise2=null,promise3=null,promise4=null,promise5=null;
        let handle3 = null, handle4=null, handle5=null;
        let flag2 = null;

        {
            t1 = Date.now();
            handle = setTimeout(() => {}, timeoutValue);
    
            t2 = Date.now();
            assert((t2-t1) < timeoutValue);
            handle = setTimeout(() => {
                let t3 = Date.now();
                assert((t3-t2) >= timeoutValue);
            }, timeoutValue);
            t3 = Date.now();
            assert((t3-t2) < timeoutValue);
        }

        {
            assert(this.gvarint2 === 200);
            handle = setTimeout(() => {
                this.assertGvarint2(300);
            }, timeoutValue);
            assert(this.gvarint2 === 200);
            this.gvarint2 = 300;
        }

        {
            handle = setTimeout(() => {
                assert(false);  // this should not execute because clearTimeout
            }, timeoutValue);
            clearTimeout(handle);    
        }

        {
            flag = 1;
            handle2 = setTimeout(() => {
                flag = 2;   // this executes because timeoutValue*2
            }, timeoutValue);
            assert(flag === 1);

            promise1 = new Promise((resolve, reject) => {
                setTimeout(() => {
                    clearTimeout(handle2);
                    resolve(null);
                }, timeoutValue*2);
            });
            await promise1;
            assert(flag === 2);

        }

        {
            flag = 1;
            handle3 = setTimeout(() => {
                flag = 2;   // this doesnt execute because timeoutValue/2
            }, timeoutValue);
            assert(flag === 1);

            promise3 = new Promise((resolve, reject) => {
                setTimeout(() => {
                    clearTimeout(handle3);
                }, timeoutValue/2);
                resolve(null);
            });
            await promise3;
            assert(flag === 1);
        }


        {
            flag = 1;
            t1 = Date.now();
            handle4 = setTimeout(() => flag = 2, timeoutValue);
            flag2 = 100;
            promise4 = new Promise((resolve, reject) => {
                setTimeout(() => {
                    clearTimeout(handle4);
                    flag2 = 200;
                    let t2 = Date.now();
                    assert((t2-t1) >= (timeoutValue/2));
                }, timeoutValue/2);
                assert(flag2 === 100);
                resolve(flag2); // resolve outside setTimeout, so doesnt wait
            });
            assert(flag2 === 100);
            t2 = Date.now();
            assert((t2-t2) < (timeoutValue/2));
            let v4 = await promise4;
            t3 = Date.now();
            assert((t3-t1) < (timeoutValue/2));
            assert(flag === 1);
            assert(flag2 === 100);  // 100 because await finished before setTimeout
                                    // wait timeoutValue/2 and flag2 will change
            assert(v4 === 100);

            t4 = Date.now();
            let promise4a = new Promise((resolve, reject) => setTimeout(() => resolve(),timeoutValue/2));
            await promise4a;
            t5 = Date.now();
            assert((t5-t4) >= (timeoutValue/2));
            assert(flag2 === 200);  // 200 now because promise4 setTimeout actually finished    
        }

        {
            /*
            - handle5 has timeoutValue and sets flag=2
            - promise5 has setTimeout that clears handle5 in timeoutValue/2, so flag=2 doesnt
                get set. but flag5 and flag5a get set. resolve is in timeout
            - flag5a gets set before the resolve in promise5
            - await promise5, which waits for the resolve. at that point, flag5a and flag5 
                get set.
            */
            flag = 1;
            handle5 = setTimeout(() => flag = 2, timeoutValue);
            let flag5 = 100;
            let flag5a = 100;
            promise5 = new Promise((resolve, reject) => {
                setTimeout(() => {
                    clearTimeout(handle5);
                    flag5 = 200;
                    flag5a = 300;
                    resolve(flag5); // resolve in setTimeout, so it waits for timeout
                }, timeoutValue*2);
                flag5a = 200;
            });
            assert(flag5a === 200); // immediate, so flag5a = 200
            let v5 = await promise5; // now do inner set flag5a = 300
            assert(flag === 2);
            assert(v5 === 200);
            assert(flag5 === 200);
            assert(flag5a === 300);
        }



        /*
        what happens with setTimeout and callback? does callback recognize this?
        */

    }
    async testMultipleSequentialPromises() {
        {
            const a = (i) => new Promise((resolve,reject) => resolve(i+100));
            const b = (i) => new Promise((resolve,reject) => resolve(i+200));
            const c = (i) => new Promise((resolve,reject) => resolve(i+300));
            let promise = Promise
                .resolve(50)
                .then(a)
                .then(b)
                .then(c)
                .then((v) => {
                    assert(v === (50+100+200+300));
                    return v;
                })
                .catch((e) => console.error(e))
                .finally(v => assert(v === undefined));
            let v = await promise;
            assert(v === (50+100+200+300));
        }
        {
            const a = (i) => new Promise((resolve,reject) => resolve(i+100));
            const b = (i) => new Promise((resolve,reject) => resolve(i+200));
            const c = (i) => new Promise((resolve,reject) => resolve(i+300));
            let promise1 = new Promise((resolve,reject) => resolve(50));
            let promise2 = promise1.then(a)
                .then(b)
                .then(c)
                .then((v) => {
                    assert(v === (50+100+200+300));
                    return v;
                })
                .catch((e) => console.error(e))
                .finally(v => assert(v === undefined));
            let v1 = await promise1;
            assert(v1 === 50);
            let v2 = await promise2;
            assert(v2 === (50+100+200+300));
        }
        {
            const a = (i) => new Promise((resolve,reject) => resolve(i+100));
            const b = (i) => new Promise((resolve,reject) => resolve(i+200));
            const c = (i) => new Promise((resolve,reject) => resolve(i+300));
            let promise = Promise
                .all([a(1),b(2),c(3)])
                .then((l) => {
                    assert(l instanceof Array);
                    let sum = 0;
                    for(let x of l) {
                        sum += x;
                    }
                    return sum;
                })
                .catch((e) => console.error(e))
                .finally(() => {});
            let v = await promise;
            assert(v === (100+1+200+2+300+3));
        }
        {
            const a = (i) => new Promise((resolve,reject) => setTimeout(() => resolve(i+'a'), 200));
            const b = (i) => new Promise((resolve,reject) => setTimeout(() => resolve(i+'b'), 100));
            const c = (i) => new Promise((resolve,reject) => setTimeout(() => resolve(i+'c'), 300));
            let promise = Promise.resolve('0')
                .then(a)
                .then(b)
                .then(c)
                .catch((e) => console.error(e))
                .finally(v => assert(v === undefined));
            let v = await promise;
            assert(v === '0abc');
        }
        {
            const a = new Promise((resolve,reject) => setTimeout(() => resolve('a'), 200));
            const b = new Promise((resolve,reject) => setTimeout(() => resolve('b'), 100));
            const c = new Promise((resolve,reject) => setTimeout(() => resolve('c'), 300));
            let promise = Promise
                .all([a,b,c])
                .then(async (l) => {
                    let r = '';
                    for(let x of l) {
                        r += x;
                    }
                    return r;
                })
                .catch((e) => console.error(e))
                .finally(v => assert(v === undefined));
            let v = await promise;
            assert(v === 'abc');
        }
        {
            const a = new Promise((resolve,reject) => setTimeout(() => resolve('a'), 200));
            const b = new Promise((resolve,reject) => setTimeout(() => resolve('b'), 100));
            const c = new Promise((resolve,reject) => setTimeout(() => resolve('c'), 300));
            let promise = Promise
                .all([a,b,c])
                .catch((e) => console.error(e))
                .finally(v => assert(v === undefined));
            let v = await promise;
            assert(v.join('') === 'abc');
        }
        // timing order is bac, but promise order is abc
        {
            const q = [];
            const a = new Promise((resolve,reject) => setTimeout(() => { q.push('a'); resolve('a'); }, 200));
            const b = new Promise((resolve,reject) => setTimeout(() => { q.push('b'); resolve('b'); }, 100));
            const c = new Promise((resolve,reject) => setTimeout(() => { q.push('c'); resolve('c'); }, 300));
            let promise = Promise
                .all([a,b,c])
                .catch((e) => console.error(e))
                .finally(v => assert(v === undefined));
            let v = await promise;
            assert(v.join('') === 'abc');
            assert(q.join('') === 'bac');
        }
        // race, b finishes first, do the assert by waiting
        {
            const a = new Promise((resolve) => setTimeout(() => resolve('a'), 200));
            const b = new Promise((resolve) => setTimeout(() => resolve('b'), 100));
            const c = new Promise((resolve) => setTimeout(() => resolve('c'), 300));
            let promise = Promise
                .race([a,b,c])
                .catch((e) => console.error(e))
                .finally(v => assert(v === undefined));
            let v = await promise;
            assert(v === 'b');
        }
        // do the assert within then
        {
            const a = new Promise((resolve) => setTimeout(() => resolve('a'), 200));
            const b = new Promise((resolve) => setTimeout(() => resolve('b'), 100));
            const c = new Promise((resolve) => setTimeout(() => resolve('c'), 300));
            Promise
                .race([a,b,c])
                .then(v => assert(v === 'b'))
                .catch((e) => console.error(e))
                .finally(v => assert(v === undefined));
        }
    }
    returnAddThisArg(vint) {
        return this.gvarint1 + vint;
    }
    return42() {
        return 42;
    }
    return43() {
        return 43;
    }
    returnAdd2Arg(vint1,vint2) {
        return vint1+vint2;
    }
    async testPromiseSimple() {
        {
            let p1 = new Promise((resolve,reject) => resolve(this.return42()));
            p1.then(x => assert(x === 42)).catch(e => console.log(`error: ${e}`));
            p1.then(x => assert(x === 43)).catch(e => assert(e.name === 'AssertionError'));
        }

        // the resolve/reject needs to be awaited or consumed in then. sequential doesnt work
        // follow q for sequence number
        {
            let flag = false;
            let q = [];
            let inx = 3;
            let p1 = new Promise((resolve,reject) => {
                if(inx % 2 == 0) {
                    q.push(0);
                    resolve(0);
                } else {
                    q.push(0);          // this happens first!
                    reject(100);
                }
            });

            q.push(1);
            let p2 = p1
                .then((x) => assert(x === undefined))
                .catch(e => {
                    flag = true;
                    assert(e === 100);
                })
                .finally(() => {
                    assert(flag === true);
                    q.push(2);          // this happens late!
                });
            assert(flag === false);     // flag is still false because p1 didnt except yet
            q.push(3);
            let localflag = false;
            try {
                await p1;
            } catch(e) {
                localflag = true;       // this will execute
                assert(e === 100);
            } finally {
                assert(localflag === true);
                assert(flag === false); // flag is still false because p1 didnt except yet
                q.push(4);
            }
            try {
                localflag = false;
                await p2;               // this waits for p1 to except
            } catch(e) {
                localflag = true;       // this will not execute
            } finally {
                assert(flag === true);  // flag is because await p2 waited for exception
                assert(localflag === false);
                q.push(5);
                assert(q.join(',') === '0,1,3,4,2,5');
            }
        }
        {
            let q1 = [];
            let q2 = [];
            let f = function(x, q) {
                return new Promise((resolve,reject) => {
                    q.push(x);
                    if(x % 2 == 0) {
                        resolve(200);
                    } else {
                        reject(100);
                    }
                });
            }
            f(2,q1).then((x) => {
                    q1.push(x);
                })
                .catch(e => q1.push(11))
                .finally(() => assert(q1.join(',') === '2,200'));

            f(3,q2).then((x) => {
                    q2.push(x);
                    q2.push(20);
                })
                .catch(e => q2.push(e))
                .finally(() => assert(q2.join(',') === '3,100'));
            assert(q1.join(',') === '2');
            assert(q2.join(',') === '3');
        }
    }
    async testPromiseCases() {
        let timeoutValue = 1000;

        /*
        this.testPromise1();
        this.testPromise2();
        this.testPromise3();
        this.testPromise4();
        this.testPromise5();
        this.testPromise6();
        this.testPromise7();
        this.testTimeoutDelay(timeoutValue);
        this.testTimeoutDelayPromise(timeoutValue);
        this.testTimeoutCases(timeoutValue);
        */

        this.testTimeoutSimple(timeoutValue);
        this.testPromiseSimple();
    }
    async testPromiseOrdering() {
        const f1 = function(ms, x, q) {
            return new Promise((resolve,reject) => 
                setTimeout(() => {
                    q.push(x);
                    resolve(x);
                }, ms));
        };
        // this completes in input order
        {
            let inputq = [200,300,100,500,150,250];
            let resultq = [];
            let sequence = Promise.resolve();   // seeder
            inputq.forEach(x => {
                sequence = sequence.then(() => 
                    f1(x,x,resultq)
                        .then(y => y+1)
                        .then(z => resultq.push(z)));
            });
            sequence.finally(() => assert(resultq.join(',') === '200,201,300,301,100,101,500,501,150,151,250,251'));
            assert(resultq.join(',') === '');   // because no promise has resolved yet
        }
        // this completes in timing order
        {
            let inputq = [200,300,100,500,150,250];
            let resultq = [];
            let promises = [];
            let sequence = Promise.resolve();
            inputq.forEach(x => {
                let p = f1(x,x,resultq)
                    .then(y => {
                        return(y+1);
                    })
                    .then(z => resultq.push(z));
                promises.push(p);
            });
            promises.forEach(async p => sequence = sequence.then(() => p));
            sequence.then(() => assert(resultq.join(',') === '100,101,150,151,200,201,250,251,300,301,500,501'));
            assert(resultq.join(',') === '');
        }
        // this completes in timing order
        {
            let inputq = [200,300,100,500,150,250];
            let resultq = [];
            let promises = [];
            inputq.forEach(x => {
                let p = f1(x,x,resultq)
                    .then(y => {
                        return(y+1);
                    })
                    .then(z => resultq.push(z));
                promises.push(p);
            });
            Promise.all(promises)
                .then((l) => assert(resultq.join(',') === '100,101,150,151,200,201,250,251,300,301,500,501'));
            assert(resultq.join(',') === '');   // because no promise has resolved yet
        }
        // this doesnt wait for any result
        {
            let inputq = [200,300,100,500,150,250];
            let resultq = [];
            let promises = [];
            inputq.forEach(x => {
                let p = f1(x,x,resultq)
                    .then(y => {
                        return(y+1);
                    })
                    .then(z => resultq.push(z));
                promises.push(p);
            });
            promises.forEach(async p => await p);
            assert(resultq.join(',') === '');
        }
        // this waits for final counter result, notice async p
        {
            let inputq = [200,300,100,500,150,250];
            let resultq = [];
            let promises = [];
            inputq.forEach(x => {
                let p = f1(x,x,resultq)
                    .then(y => {
                        return(y+1);
                    })
                    .then(z => resultq.push(z));
                promises.push(p);
            });
            let ctr = 0;
            promises.forEach(async p => {
                let x = await p;
                ctr++;
                if(ctr == inputq.length) {
                    assert(resultq.join(',') === '100,101,150,151,200,201,250,251,300,301,500,501');
                }
            });
            assert(resultq.join(',') === '');
        }
        // this awaits sequentially because not using async within forEach
        {
            let inputq = [200,300,100,500,150,250];
            let resultq = [];
            let promises = [];
            inputq.forEach(x => {
                let p = f1(x,x,resultq)
                    .then(y => {
                        return(y+1);
                    })
                    .then(z => resultq.push(z));
                promises.push(p);
            });
            for(let p of promises) {
                await p;
            }
            assert(resultq.join(',') === '100,101,150,151,200,201,250,251,300,301,500,501');
        }
        // simple await of a promise
        {
            const f1 = () => new Promise((resolve,reject) => resolve('someone'));
            const f2 = async () => {
                let x = await f1();
                return x + ' else';
            };
            let v;
            v = await f1();
            assert(v === 'someone');
            v = await f2();
            assert(v === 'someone else');
        }
    }
    fWrapped(f,...args) {
        return f(...args); // do not do f(args)!
    }
    async fWrappedTimeout(ms,f,...args) {
        try {
            let h = setTimeout(() => { throw 'timeoutThrown'; }, ms);
            let v = f(...args,h);
            //clearTimeout(h);
            return v;
        } catch(e) {
            console.log(`catch: ${e}`);
            if(e === 'timeoutThrown') {
                console.log(e);
            } else {
                throw e;
            }
        }
    }
    // this doesnt work yet.. how to get handler and get reject?
    async fWrappedTimeoutPromise(ms,f,...args) {
        let h = null;
        let pto = new Promise((resolve,reject) => {
            h = setTimeout(() => reject('timeout'), ms);
        });
        let pf = new Promise((resolve,reject) => {
            let v = f(...args);
            resolve(v);
        });
        let x = Promise.race([pto,pf])
            .then((x) => {
                if(x === 'timeout') {
                    console.log(`log: ${x}`);
                } else {
                    return x;
                }
            })
            .catch((e) => {
                console.log('catch: ' + e);
            })
            .finally(() => {
                clearTimeout(h);
            });
        let v = await x;
        return v;
    }
    async fWrappedTimeoutUseless(ms,f,...args) {
        let flag = false;
        try {
            let h = setTimeout(() => { throw 'timeoutThrown'; }, ms);
            let v = f(...args);
            clearTimeout(h);    // this always clears
            return v;
        } catch(e) {
            if(e === 'timeoutThrown') {
                flag = true;
                //console.log(e);
            } else {
                throw e;
            }
        } finally {
            assert(flag === false);
        }
    }
    async testWrappedTimeout() {
        {
            let f = function(a,b,c) {
                //console.log(`a:${a},b:${b},c:${c}`);
                return a+b+c;
            };
            assert(f(1,2,3) === 6);
            assert(this.fWrapped(f,1,2,3) === 6);
        }
        {
            let f = function(a,b,c) {
                setTimeout(() => {}, 1000);
            };
            assert(f(1,2,3) === undefined);
            assert(this.fWrapped(f,1,2,3) === undefined);
        }
        {
            let f = function(a,b,c,h) {
                setTimeout(() => {
                    clearTimeout(h);
                }, 1000);
            };
            this.fWrappedTimeout(2000,f,1,2,3); // ok because never throws
            try {
                // setTimeout is run in main loop, so you cannot catch
                // error from setTimeout. instead, wrap timeout into
                // promise -> reject and catch it within a promise...
                // that means this code would never work!
                this.fWrappedTimeout(100,f,1,2,3); 
            } catch(e) {
                console.log(`logging e: ${e}`);
            }
        }
        {
            let f = function(a,b,c,h) {
                setTimeout(() => {
                    clearTimeout(h);
                }, 1000);
            };
            this.fWrappedTimeout(2000,f,1,2,3); // ok because never throws
            try {
                // setTimeout is run in main loop, so you cannot catch
                // error from setTimeout. instead, wrap timeout into
                // promise -> reject and catch it within a promise...
                // that means this code would never work!
                //this.fWrappedTimeout(100,f,1,2,3); 
            } catch(e) {
                console.log(`logging e: ${e}`);
            }
        }
        {
            let f = function(a,b,c,h) {
                setTimeout(() => {
                    clearTimeout(h);
                }, 1000);
            };
            let f2 = function(a,b,c) {
                return a+b+c;
            };
            let v = await this.fWrappedTimeoutPromise(2000,f2,1,2,3);
            assert(v === 6);
        }

    }
    async testTime() {
        let t1 = Date.now();
        let t2 = new Date('2020/01/01');
    }
    async testHelper1() {}
    randInt(min, max) {
        // [min,max)
        let r = Math.random() * (max-min) + min;
        let i = Math.floor(r); 
        return i;
    }

    async asyncGeneric(q,i) {
        return new Promise(resolve => {
            q.push(i);
            resolve(i);
        });
    }
    async asyncLoopAwait(q) {
        for(let i = 0; i < 3; i++) {
            q.push(100*(i+1)+i);
            let v = await this.asyncGeneric(q,100*(i+1)+i+1);
            q.push(100*(i+1)+i+2);
        }
        q.push(500);
        return 10;
    }
    async testAsyncOrderingAsyncFunctions() {
        let q = [];
        q.push(1);
        let v = await this.asyncLoopAwait(q);
        q.push(2);
        assert(q.join(',') === '1,100,101,102,201,202,203,302,303,304,500,2');
    }
    testAsyncOrderingLoop() {
        for(let i = 0; i < 10; i++) {
            this.testAsyncOrdering();
        }
    }
    async testAsyncOrdering() {
        let q = [];

        // this is called whenever it is called
        let f1 = function() {
            setTimeout(() => {
                q.push(10);
                assert(q.join(',') === '1,2,3,4,5,6,7,8,9,10');
            }, 10);
            q.push(6);
            assert(q.join(',') === '1,2,3,4,5,6');
        };

        // promise is activated immediately
        let f2 = new Promise((resolve,reject) => {
            setTimeout(() => {
                q.push(11);
                assert(q.join(',') === '1,2,3,4,5,6,7,8,9,10,11');
                resolve('f2');
            }, 15);
            q.push(1);
            assert(q.join(',') === '1');
        });

        // promise is activated immediately
        let f3 = new Promise((resolve,reject) => {
            setTimeout(() => {
                q.push(15);
                assert(q.join(',') === '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15');
            }, 20);
            q.push(2);
            assert(q.join(',') === '1,2');
            resolve('f3');
        });

        // promise is activated immediately
        let f4 = new Promise((resolve) => {
            q.push(3);
            assert(q.join(',') === '1,2,3');
            resolve(100);
        })

        q.push(4);

        // promise is activated immediately, but there is some lag
        let v4 = f4
            .then(x => {
                q.push(8);
                assert(q.join(',') === '1,2,3,4,5,6,7,8');
                return x+10;
            })
            .then(x => {
                q.push(9);
                assert(q.join(',') === '1,2,3,4,5,6,7,8,9');
                return x+11;
            });

        q.push(5);
        assert(q.join(',') === '1,2,3,4,5');

        // timer function now called
        f1();
        q.push(7);
        assert(q.join(',') === '1,2,3,4,5,6,7');

        let v2 = await f2;
        q.push(12);
        assert(q.join(',') === '1,2,3,4,5,6,7,8,9,10,11,12');

        let v3 = await f3;
        assert(v3 === 'f3');
        q.push(13)
        assert(q.join(',') === '1,2,3,4,5,6,7,8,9,10,11,12,13');

        // this is small loop of async functions, 0 wait
        let v5 = await this.testAsyncOrderingAsyncFunctions();

        q.push(14);
        assert(q.join(',') === '1,2,3,4,5,6,7,8,9,10,11,12,13,14');
    }

    testRandInt() {
        var numchars = (args.numchars !== undefined) ? parseInt(args.numchars) : 0;
        var outfile  = (args.outfile !== undefined) ? args.outfile : null;
        var compress = (args.compress !== undefined) ? true : false;
        var hex      = (args.hex !== undefined) ? true : false;
        var array = [];
        var bytes = [];
        const limit = 1_000_000;
        const sz = alphanum.length;
        debug(`numchars:${numchars} outfile:${outfile} compress:${compress}`);
        assert(numchars < limit);
        for(let i = 0; i < numchars; i++) {
            let v = this.randInt(0,sz);
            let c = alphanum.charAt(v);
            let x = c.charCodeAt(0);
            array.push(c);
            bytes.push(x);
        }

        var s = array.join('');
        var encoded = new TextEncoder('utf-8').encode(s);
        var decoded = new TextDecoder('utf-8').decode(encoded);
        var uint8Array = new Uint8Array(bytes);

        debug(s);
        debug('encoded    ' + encoded);
        debug('decoded    ' + decoded);
        debug('array      ' + array);
        debug('bytes      ' + bytes);
        debug('uint8array ' + uint8Array);
        
        if(hex) {
            {
                var h = Array.prototype.map.call(uint8Array, x => ('0x' + x.toString(16)));
                var hs = h.join(',');
                debug(hs);
            }
            {
                var h = Array.from(uint8Array, x => ('0x' + x.toString(16)));
                var hs = h.join(',');
                debug(hs);
            }
        }
    }
    promisifyCb(err,in1) {
        return in1;
    }
    async promisifyFunction(in1,cb1) {
        var i = in1;
        return cb1(null, i);
    }
    async testPromisify() {
        // changes callback(err,val) to promise(err,val)
        {
            let v = await this.promisifyFunction(10,this.promisifyCb);
            assert(v === 10);
        }
        {
            const promisifiedF = util.promisify(this.promisifyCb).bind(this);
            let v = await promisifiedF(null, 10);
            assert(v === 10);
            v = await this.promisifyFunction(11,promisifiedF);
            assert(v === 11);
        }
        {
            let in1 = 10;
            const promisifiedF = new Promise((resolve,reject) => {
                let v = this.promisifyCb(null, in1);
                resolve(v);
            });
            let v = await promisifiedF;
            assert(v === 10);
        }
    }
    async testGzipZlib() {
        let l = [];
        let sz = 50;
        for(let i = 0; i < sz; i++) {
            let s = `this is line num ${i}`;
            l.push(s);
        }
        let s = l.join('\n');
        let flag = false;
        {
            zlib.deflate(s, (err, bufzip) => {
                if(err) { throw `ZIP ERROR: ${e}`; }
                //console.log(bufzip.toString('base64'));
                zlib.unzip(bufzip, (err, bufunzip) => {
                    if(err) { throw `UNZIP ERROR: ${e}`; }
                    //console.log(bufunzip.toString());
                    assert(bufunzip.toString() === s);
                });
            });
        }
        {
            zlib.gzip(s, (err, bufzip) => {
                if(err) { throw `ZIP ERROR: ${e}`; }
                zlib.unzip(bufzip, (err, bufunzip) => {
                    if(err) { throw `UNZIP ERROR: ${e}`; }
                    assert(bufunzip.toString() === s);
                });
            });
        }
        {
            var bufzip = zlib.gzipSync(s);
            var szip = bufzip.toString('base64');
            //console.log(szip.length);
            var bufunz = zlib.gunzipSync(bufzip);
            var sunz = bufunz.toString();
            assert(sunz === s);
        }
        {
            var bufzip = zlib.deflateSync(s);
            var szip = bufzip.toString('base64');
            //console.log(szip.length);
            var bufunz = zlib.inflateSync(bufzip);
            var sunz = bufunz.toString();
            assert(sunz === s);
        }
        if(flag)
        {
            // this doesnt work because createReadStream input should be file, not content
            const pipeline = util.promisify(stream.pipeline).bind(this);
            const gzip = zlib.createGzip();
            const src = fs.createReadStream(s); // this doesnt work, ENAMETOOLONG, must be file
            //const src = fs.createReadStream(Buffer.from(s)); // doesnt work
            src.on('error', e => console.log('R:', e));
            let bufzip = new ArrayBuffer();
            const dst = fs.createWriteStream(bufzip);
            dst.on('error', e => console.log('W:',e));
            await pipeline(src, gzip, dst);
            console.log(dst);
        }
    }
    async testStreams() {
        let l = [];
        let sz = 100;
        for(let i = 0; i < sz; i++) {
            let s = `this is line num ${i}`;
            l.push(s);
        }
        let s = l.join('\n');
        let filename = './dirinput/test_string_data.txt';
        let q = [];

        let fwritefile1 = async (file,data) => {
            return new Promise((resolve,reject) => {
                fs.writeFile(file, data, (e) => {
                    q.push(1);
                    if(e) {
                        reject(e);
                    } else {
                        resolve();
                    }
                });
            });
        }
        let result = await fwritefile1(filename,s);
        assert(q.join(',') === '1');
        assert(result === undefined);
        // at this point, filename is done
        var continueflag = false;
        {
            // pipe reader to writer gzip
            let filenameout1 = './diroutput/test_string_data.txt.gzip';
            let readStream = fs.createReadStream(filename);
            let writeStream = fs.createWriteStream(filenameout1);
            let gzipFilter = zlib.createGzip();
            let cb1 = (e,d) => {
                if(e) {
                    console.error(`zip error:`, e);
                } else {
                    console.log('done with gzip pipeline');
                    readStream.close();
                    writeStream.close();
                    gzipFilter.end();
                    continueflag = true;

                    funzip();   // callback style is better than spin loop. 
                                // promise of this block should also work.
                                // just put promise resolve here, and wait, and
                                // then execute the unzip promise.
                }
            };
            stream.pipeline(readStream, gzipFilter, writeStream, cb1);
        }
        // at this point, the above write may not have finished yet. so above should
        // either be at a spin loop, promise, or callback. so the spin loop doesnt work.
        // instead put it as a callback, so that the unzip starts only after the zip is done.
        // the commented out waitAWhile spinloop also works, but just do callback.

        // this doesnt work
        //while(!continueflag) {
        //}

        // waitAWhile is workable code, and is alternative to funzip callback, and
        // is alternative to 2 promises, or promise chain
        /*

        var waitAWhile = new Promise((resolve,reject) => setTimeout(()=> resolve(),100));
        continueflag = false;
        while(!continueflag) {
            var resultWait = await waitAWhile;
        }

        */

        var funzip = () => 
        {
            // pipe reader of gzip to text file write
            let filenamein1 = './diroutput/test_string_data.txt.gzip';
            let filenameout1 = './diroutput/test_string_data.txt';
            let readStream = fs.createReadStream(filenamein1);
            let writeStream = fs.createWriteStream(filenameout1);
            let gunzipFilter = zlib.createGunzip();
            let cb1 = (e,d) => {
                if(e) {
                    console.error(`gunzip error: `, e);
                } else {
                    console.log('done with ungzip pipeline');
                    readStream.close();
                    writeStream.close();
                    gunzipFilter.end();
                }
            };
            stream.pipeline(readStream, gunzipFilter, writeStream, cb1);
        };
    }
    async testSingleCase() {
        let l = [];
        let sz = 10;
        for(let i = 0; i < sz; i++) {
            let s = `this is line num ${i}`;
            l.push(s);
        }
        let s = l.join('\n');
        {
            const pipeline = util.promisify(stream.pipeline).bind(this);
            const gzip = zlib.createGzip();
            const src = fs.createReadStream(s);
            let bufzip = new ArrayBuffer();
            const dst = fs.createWriteStream(bufzip);
            await pipeline(src, gzip, dst);
            src.end();
            dst.end();
            //console.log(dst);
        }


    }
    async testListenEventsCB(v, q, max) {
        q.push(v);
        console.log(`received event ${v}`);
        if(q.length === max){
            console.log(`q length max:`, q);
        }
    }
    async testListenEvents(arg1, q, cb, max) {
        cb(arg1, q, max);
    }
    async testEmitEvents() {
        let ctr = 0;
        let q = [];
        let max = 5;
        this.emitter.on('event1', () => {
            this.testListenEvents(ctr++, q, this.testListenEventsCB, max);
        })
        while(q.length != 5) {
            this.emitter.emit('event1');
        }
    }
    registerEmitEvents2(sharedq) {
        let ctr = 0;
        let max = 5;
        // a class can also extends EventEmitter, and the class can do class.on('blah')
        this.emitter.on('event1', () => {
            this.testListenEvents(ctr++, sharedq, this.testListenEventsCB, max);
        })
        let q = [];
        this.emitter.on('event2', () => {
            this.testListenEvents(ctr++, q, this.testListenEventsCB, max);
        })
    }
    testEmitEvents2FunctionsHelper1(q) {
        while(q.length != 5) {
            this.emitter.emit('event1');
        }
    }
    testEmitEvents2FunctionsHelper2() {
        for(let i = 0; i < 5; i++) {
            this.emitter.emit('event2');
        }
    }
    // this is to see if registration of emit can be separated from emit section. yes
    testEmitEvents2Functions() {
        let sharedq = [];
        this.registerEmitEvents2(sharedq);
        this.testEmitEvents2FunctionsHelper1(sharedq);
        this.testEmitEvents2FunctionsHelper2();
    }
    testSetTimeoutCbArgsHelper2(ms,n,x,y) {
        console.log(`testSetTimeoutCbArgsHelper2 ms:${ms} n:${n} x:${x} y:${y}`);
        let cb1 = this.testSetTimeoutCbArgs;
        let cb2 = this.testSetTimeoutCbArgsHelper2;
        let bindedCb1 = cb1.bind(this); // must be binded
        setTimeout(bindedCb1, 10, n, cb2);
        let bindedCb2 = cb2.bind(this); // this doesnt have to be binded
        //setTimeout(bindedCb1, 10, n, bindedCb2);
    }
    testSetTimeoutCbArgsHelper1(cb, ms,n,x,y) {
        console.log(`testSetTimeoutCbArgsHelper1 ms:${ms} n:${n} x:${x} y:${y}`);
        assert(cb !== undefined);
        setTimeout(cb, 10, ms,n,x,y);
    }
    testSetTimeoutCbArgs(n,cb) {
        console.log(`testSetTimeout ${n}`);
        assert(cb !== undefined);
        if(n > 0) {
            let x = n*2;
            let y = n;
            n--;
            let bindedCb = cb.bind(this);   // must be binded
            setTimeout(this.testSetTimeoutCbArgsHelper1, 10, bindedCb, 10, n, x, y);
        }
    }
    // this doesnt exit immediately!
    testSetTimeout(i) {
        if(i <= 0) {
            return;
        }
        console.log(`testSetTimeout ${i}`);
        i--;
        setTimeout(() => this.testSetTimeout(i), 50);
    }
    async testPromisesAnyHelper1(ms, i) {
        return new Promise((resolve,reject) => {
            setTimeout(() => {
                resolve(i);
            }, ms);
        });
    }
    async testPromisesAnyHelperQueryable(ms, i) {
        let isPending = true;
        let isRejected = false;
        let isFulfilled = false;
        let promise = new Promise((resolve,reject) => {
            setTimeout(() => {
                isPending = false;
                isFulfilled = true;
                resolve(i);
            }, ms);
        });
        promise.isPending = () => { return isPending; };
        promise.isRejected = () => { return isRejected; };
        promise.isFulfilled = () => { return isFulfilled; };
        return promise;
    }
    async testPromisesAnyHelper2Cb(i, resolve) {
        resolve(i);
    }
    async testPromisesAnyHelper2(ms, i, cb) {
        return new Promise((resolve,reject) => {
            setTimeout(() => {
                cb(i, resolve);
            }, ms);
        });
    }
    async tmpcode() {
        let q = [];
        let max = 10;
        for(let i = 0; i < max; i++) {
            let p = this.testPromisesAnyHelper1(10,i);
            q.push(p);
        }
        let completed = [];
        while(completed.length < max) {
            let p = await Promise.any(q);
            completed.push(p);
            console.log(`p `,p);
        }
        console.log('done');

    }
    async testPromisesAnyHelper3(ms, i, d, c) {
        return new Promise((resolve,reject) => {
            setTimeout(() => {
                delete d[i];
                c[i] = i;
                resolve(i);
            }, ms);
        });
    }
    async sleepPromise(ms) {
        return new Promise((resolve) => {
            setTimeout(() => resolve(), ms);
        });
    }
    async testPromisesAny() {
        let flag = true;
        {
            let q = [];
            let max = 10;
            for(let i = 0; i < max; i++) {
                let p = await this.testPromisesAnyHelper1(10,i);
                assert(p === i);
            }    
        }

        // this works. just use a sleep function
        {
            let d = {};
            let c = {};
            let max = 10;
            for(let i = 0; i < max; i++) {
                let p = this.testPromisesAnyHelper3(10,i, d, c);
            }

            // this loop doesnt work because p.isFulfilled is undefined!
            while(Object.keys(c).length !== 10) {
                await this.sleepPromise(10);
            }
            assert(Object.keys(d).length === 0);
            assert(Object.keys(c).length === 10);
            console.log('done');
        }

        flag = false;
        if(flag)
        {
            // dont run this, since the properties are not set up correctly
            let d = {};
            let c = {};
            let max = 10;
            for(let i = 0; i < max; i++) {
                let p = this.testPromisesAnyHelperQueryable(10,i);
                d[i] = p;
            }

            let completed = {};
            // this loop doesnt work because p.isFulfilled is undefined!
            while(Object.keys(d).length !== 0) {
                for(let [k,p] of Object.entries(d)) {
                    console.log(p);
                    //console.log(`> ${p.isFulfilled} ${p.isRejected}`);
                    //if(p.isFulfilled() || p.isRejected()) {
                    //    console.log(`p is fulfilled`);
                    //    completed[k] = p;
                    //    delete d[k];
                    //}
                }
            }
            assert(Object.keys(d).length === 0);
            console.log('done');
        }
    }
    testFiles() {
        /*
        test read file sync
        test read file async
        test write file sync
        test write file async
        test append file async
        test read stream
        test write stream
        test read pipe to transform pipe to write pipe
        test create directory
        test delete file
        test if file exists
        test if directory exists
        stat method for checking if is file or is directory
        read directory filenames and directories
        */
        let enable = false;

        if(enable)
        {

        }

        {
            let path = '';
            fs.stat(path, (error, stats) => {
                if(error) {
                    throw error;
                } else {
                    if(stats.isFile()) {

                    }
                    else if(stats.isDirectory()) {

                    }
                }
            });
        }
        {
            let file = '';
            let dst = '';
            {
                fs.createReadStream(file)
                .pipe(zlib.createGzip())
                .pipe(fs.createWriteStream(dst));
            }
            {
                let readStream = fs.createReadStream(file);
                let writeStream = fs.createWriteStream(dst);
                readStream.pipe(writeStream);
            }
            {
                // add events for writeStream drain and error detection
            }
            {
                // add events
                let readStream = fs.createReadStream(file);
                readStream.on('error', (e) => {
                    console.log(e);
                })
                readStream.on('end', () => {

                });
                readStream.on('close', () => {

                })
            }
        }
        {
            let filei = '';
            let fileo = '';
            let buffer = [];
            {
                fs.readFile(filei, (error, data) => {
                    if(error) {
                        throw error;
                    } else {
                        buffer = data;
                    }
                });
            }
            {
                try {
                    buffer = fs.readFileSync(filei, 'utf8');
                    let s = buffer.toString();
                } catch(e) {
                    console.log(e);
                }
                try {
                    fs.writeFile(fileo, buffer, (err) => {
                        if(err) {
                            throw err;
                        }
                    });
                } catch(e) {
                    console.log(e);
                }
                try {
                    fs.writeFileSync(fileo, buffer, { encoding: 'utf8' });
                } catch(e) {
                    console.log(e);
                }
            }
        }
    }

    testCrypto() {
        let v = null;
        v = crypto.randomBytes(16).toString('hex');
        v = crypto.randomBytes(16).toString('base64');
    }

    test() {
        /*
        this.testMultipleSequentialPromises();
        this.testPromiseCases();
        this.testPromiseOrdering();
        this.testWrappedTimeout();
        this.testAsyncOrderingAsyncFunctions();
        this.testAsyncOrderingLoop();
        this.testPromisify();
        this.testGzipZlib();
        this.testSingleCase();
        this.testEmitEvents();
        this.testStreams();
        this.testEmitEvents2Functions();
        this.testPromisesAny();
        this.testSetTimeout(5);
        */

        this.testAxiosFiles();
        this.testFiles();
        this.testSetTimeoutCbArgs(5, this.testSetTimeoutCbArgsHelper2);

    }
}

test = new TestAsync();
test.test();

