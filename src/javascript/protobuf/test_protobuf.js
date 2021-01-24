// not needed
const goog = require('google-closure-library');
// not needed
const protobuf = require('protobufjs');             
const fetch = require('node-fetch');
const message = require('./protobuf_lib/message-t1_pb.js');
const ProtoPayload = require('./protobuf_lib/testpayloads_pb.js');

const assert = require('assert');
const { SSL_OP_NO_TLSv1_1 } = require('constants');
const abortController = require('abort-controller');
const controller = new abortController();
const axios = require('axios').default;
const PORT = 3000;


class Test {
    debug = true;
    testProto() {
        const t1 = new message.Test1();
        t1.setId(100);
        t1.setIval2(20);
        const t1Inner = new message.Test1.InnerTest1();
        t1Inner.setId(200);
        t1Inner.setSval1('hello world');
        t1.setInnert1(t1Inner);
        assert(t1.getId() == 100);
        assert(t1Inner.getId() == 200);

        let serializedData = t1.serializeBinary();
        let deserializedData = message.Test1.deserializeBinary(serializedData);

        assert(deserializedData.getId() == 100);
        let t1InnerDS = deserializedData.getInnert1();
        assert(t1InnerDS.getId() == 200);
        assert(t1InnerDS.getSval1() === 'hello world');

        // convert to object then convert to JSON
        let dataObject = t1.toObject();
        let dataString = JSON.stringify(dataObject);
        let dataJSON = JSON.parse(dataString);          // doesnt seem to be needed
        assert(typeof dataObject === 'object');
        assert(typeof dataJSON === 'object');
        assert(dataObject['id'] === 100);
        assert(dataObject['innert1']['id'] === 200);
        assert(dataJSON['id'] === 100);
        assert(dataJSON['innert1']['id'] === 200);
        assert(dataString === '{"id":100,"rivalList":[],"ival2":20,"rsvalList":[],"innert1":{"id":200,"rivalList":[],"sval1":"hello world","rsvalList":[]},"rinnertList":[]}');

        const t2 = t1.cloneMessage();
        assert(t1.getId() === t2.getId());

        // this doesnt work
        const t3 = new message.Test1(serializedData);
        assert(t1.getId() !== t3.getId());

        // this doesnt work
        const t5 = new message.Test1(deserializedData);
        assert(t1.getId() !== t5.getId());

        // this works, and is how to create new object
        const t4 = message.Test1.deserializeBinary(serializedData);
        assert(t1.getId() === t4.getId());
        assert(t1.getIval2() === 20 && t1.getIval2() === t4.getIval2());
    }
    async testFetchJson() {
        const url = `http://localhost:${PORT}/json`;
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
        const body = {
            'k1': 'eieo',
            'k2': 'old macdonald'
        };
        const jsonstr = JSON.stringify(body);
        try {
            let rsp = await fetch(url, { 
                method: 'POST',
                headers: headers,
                body: jsonstr
            });
            if(!rsp.ok) {
                throw `rsp not ok: ${rsp.status}`;
            }
            let rspjson = await rsp.json();
            console.log(rspjson);
        } catch(e) {
            console.log(e);
        }
    }
    async testFetchJsonAbortController() {
        const url = `http://localhost:${PORT}/json`;
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
        const body = {
            'k1': 'eieo',
            'k2': 'old macdonald'
        };
        const jsonstr = JSON.stringify(body);
        let timeout = setTimeout(() => controller.abort(), 200);
        try {
            let rsp = await fetch(url, { 
                method: 'POST',
                headers: headers,
                body: jsonstr,
                signal: controller.signal   // for timeout signaling
            });
            if(!rsp.ok) {
                throw `rsp not ok: ${rsp.status}`;
            }
            let rspjson = await rsp.json();
            console.log(rspjson);
        } catch(e) {
            console.log(e);
            /*
            if(e instanceof fetch.AbortError) {
                console.log(`fetch aborterror: ${e}`);
            } else {
            }
            */
        } finally {
        }
        clearTimeout(timeout);
    }
    // this works
    async testFetchPostGetProto() {
        const req = new ProtoPayload.Request();
        req.setId(100);
        req.setIval(200);
        req.setSval('hello');
        const innerPayload = new ProtoPayload.Request.InnerPayload();
        innerPayload.setId(101);
        innerPayload.setKey('k1');
        innerPayload.setVal('v1');
        req.setInnerpayload(innerPayload);

        let serializedData = req.serializeBinary();
        try {
            const url = `http://localhost:${PORT}/proto`;
            const headers = {
                'Content-Type': 'application/octet-stream',
                'Accept': 'application/octet-stream'
            };
            let rsp = await fetch(url, {
                method: 'POST',
                headers: headers,
                body: serializedData
            });
            if(!rsp.ok) {
                throw `rsp not ok ${rsp.status}`;
            }
            const body = await rsp.buffer();
            const uint8Array = new Uint8Array(body)
            const buffer = Buffer.from(body);
            console.log(buffer.join(','));
            console.log(uint8Array.toString());
            //console.log(uint8Array);
            const response = ProtoPayload.Response.deserializeBinary(uint8Array);
            const json = response.toObject();
            console.log(json);
        
        } catch(e) {
            console.log('ERROR: ', e);
        }
        // this works, and is how to create new object
        const t4 = message.Test1.deserializeBinary(serializedData);
    }
    async post(url, data, options) {
        return new Promise((resolve,reject) => {
            axios.post(url, data, options, {timeout: this.timeoutms})
            .then(r => resolve(r))
            .catch(e => {
                console.log(`ERROR POST`, e.toJSON());
                reject(e.code);
            })
        })
    };
    async testAxiosPostGetProto() {
        const req = new ProtoPayload.Request();
        req.setId(100);
        req.setIval(200);
        req.setSval('hello');
        const innerPayload = new ProtoPayload.Request.InnerPayload();
        innerPayload.setId(101);
        innerPayload.setKey('k1');
        innerPayload.setVal('v1');
        req.setInnerPayload(innerPayload);
        let serializedData = req.serializeBinary();
        try {
            const url = `http://localhost:${PORT}/proto`;
            const headers = {
                'Content-Type': 'application/octet-stream',
                'Accept': 'application/octet-stream'
            };
            let rsp = await this.post(url, serializedData, {
                method: 'POST',
                headers: headers,
                responseType: 'arraybuffer'     // this is important!
            });
            /*
            let rsp = await axios.post(url, serializedData, {
                method: 'POST',
                headers: headers,
                responseType: 'blob'
            },
            {timeout: this.timeoutms})
            .then(r => r)
            .catch(e => {
                console.log('ERROR POST:', e.toJSON());
                reject(e.code);
            });
            */
           if(rsp.status !== 200) {
               throw `rsp not ok ${rsp.status}`;
           }
           const body = await rsp;
           const buffer = Buffer.from(body);
           const uint8Array = new Uint8Array(body);
           console.log(buffer.join(','));
           console.log(uint8Array.toString());
           {
               const response = ProtoPayload.Response.deserializeBinary(uint8Array);
               const json = response.toObject();
               console.log(json);
           }
           {
               const response = new ProtoPayload.Response(buffer);
               const json = response.toObject();
               console.log(json);
           }
        } catch(e) {
            console.log(`ERROR:`, e);
        }
        // this works, and is how to create new object
        const t4 = message.Test1.deserializeBinary(serializedData);
    }
    async test() {
        /*
        this.testFetchJson();
        this.testFetchPostGetProto();
        this.testFetchJsonAbortController();
        this.testProto();
        async(() => {
            console.log(`-------------FETCH`);
            await this.testFetchPostGetProto();
            console.log(`-------------AXIOS`);
            await this.testAxiosPostGetProto();
        })();
        */
        this.testFetchPostGetProto();
    }
}

const t = new Test();
t.test();