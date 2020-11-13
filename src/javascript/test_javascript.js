const https = require('https');
const http = require('http');
const fetch = require('node-fetch');
const crypto = require('crypto');

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
    }
    iSaidSomething1() {
        let s = "i said something";
        console.log(s)
        return s;
    }
    iSaidNothing1() {
        let s = `i said nothing`;
        console.log(s)
        return s;
    }
    whatDidISay1() {
        let s = `what did i say?`;
        console.log(s)
        return s;
    }
    iSaidSomething2(vin) {
        let s = `i said something and ${vin}`;
        console.log(s)
        return s;
    }
    iSaidNothing2(vin) {
        let s = `i said nothing and ${vin}`;
        console.log(s)
        return s;
    }
    whatDidISay2(vin) {
        let s = `what did i say and ${vin}?`;
        console.log(s)
        return s;
    }
    testPromise1() {
        let resolve = Promise.resolve();
        let r = resolve
            .then(() => this.iSaidSomething1())
            .then(() => this.iSaidNothing1())
            .then(() => this.whatDidISay1())
            .catch(e => console.log(`i got error ${e}`));
        console.log(`r is ${r}`); // this is an object
    }
    testPromise2() {
        let resolve = Promise.resolve();
        let s = 'hello';
        let r = resolve
            .then(() => this.iSaidSomething2(s))
            .then((s) => this.iSaidNothing2(s))
            .then((s) => this.whatDidISay2(s))
            .catch(e => console.log(`i got error ${e}`));
        console.log(`r is ${r}`); // this is an object
    }
    testPromise3() {
        let s = 'hello';
        let r = new Promise((resolve, reject) => resolve())
            .then(() => this.iSaidSomething2(s))
            .then((s) => this.iSaidNothing2(s))
            .then((s) => this.whatDidISay2(s))
            .catch(e => console.log(`i got error ${e}`));
        console.log(`r is ${r}`); // this is an object
    }
    testPromise4() {
        let s = 'hello';
        let r = new Promise((resolve, reject) => resolve(this.iSaidSomething2(s)))
            .then((s) => this.iSaidNothing2(s))
            .then((s) => this.whatDidISay2(s))
            .catch(e => console.log(`i got error ${e}`));
        console.log(`r is ${r}`); // this is object
    }
    async testPromise5() {
        let s = 'hello';
        let r = new Promise((resolve, reject) => resolve(this.iSaidSomething2(s)))
            .then((s) => this.iSaidNothing2(s))
            .then((s) => this.whatDidISay2(s))
            .catch(e => console.log(`i got error ${e}`));
        await r;
        console.log(`r is ${r}`);   // this is an object
    }
    async testPromise6() {
        let s = 'hello';
        let r = await new Promise((resolve, reject) => resolve(this.iSaidSomething2(s)))
            .then((s) => this.iSaidNothing2(s))
            .then((s) => this.whatDidISay2(s))
            .catch(e => console.log(`i got error ${e}`));
        console.log(`r is ${r}`); // this is string value!
    }
    async testPromise7() {
        let s = 'hello';
        let r = new Promise((resolve, reject) => resolve(this.iSaidSomething2(s)))
            .then((s) => this.iSaidNothing2(s))
            .then((s) => this.whatDidISay2(s))
            .catch(e => console.log(`i got error ${e}`));
        let v = await r;
        console.log(`r is ${v}`);   // this is string value!
    }

    test() {
        let ctr = 0;
        
        //this.testAsync();

        //this.testMakeHttpRequestGet1();
        ctr++;
        console.log(`|-----------------------${ctr}`);

        //this.testMakeHttpRequestPost1();
        ctr++;
        console.log(`|-----------------------${ctr}`);

        //this.testJson1();
        ctr++;
        console.log(`|-----------------------${ctr}`);
    }
}

test = new TestAsync();
//testAsync.test();
//test.test2();
test.testPromise7();

