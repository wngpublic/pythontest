const express = require('express');
const fetch = require('node-fetch');
const bodyParser = require('body-parser');
const assert = require('assert');

const protobuf = require('protobufjs');
//const builder = protobuf.loadProtoFile('./protobuf_lib/testpayloads.proto');

const builder = protobuf.load('./protobuf_lib/testpayloads.proto')
    .then((r) => { return r; }); // this is promise though
//const requestMessage = builder.build('Request');
//const responseMessage = builder.build('Response');

// just use this because i dont know how to use testpayloads.proto
const ProtoPayload = require('./protobuf_lib/testpayloads_pb.js');

const app = express();
const PORT = 3000;

async function fproto(req, res) {
    const uint8Array = new Uint8Array(req.body);
    const request = ProtoPayload.Request.deserializeBinary(uint8Array);

    const json = request.toObject();
    console.log(json);

    const response = new ProtoPayload.Response();

    // this does not work
    //const response = ProtoPayload.Response.deserializeBinary(json);

    response.setId(request.getId());
    response.setIval(request.getIval());
    response.setSval(request.getSval());
    {
        const reqInnerpayload = request.getInnerpayload();
        const innerPayload = new ProtoPayload.Request.InnerPayload();
        innerPayload.setId(reqInnerpayload.getId());
        innerPayload.setKey(reqInnerpayload.getKey());
        innerPayload.setVal(reqInnerpayload .getVal());
        response.addInnerpayload(innerPayload);
    }
    {
        const innerPayload = new ProtoPayload.Request.InnerPayload();
        innerPayload.setId(102);
        innerPayload.setKey('k2');
        innerPayload.setVal('v2');
        response.addInnerpayload(innerPayload);
    }

    let serializedData = response.serializeBinary();
    //let responseObject = response.toObject();  // this is also ok

    // these both work
    //res.send(Buffer.from(serializedData));
    res.end(Buffer.from(serializedData));

    // these are wrong
    //res.send(serializedData);
    //res.end(Buffer.from(serializedData));
}

async function processJson(req, rsp) {
    let reqbody = req.body;
    //console.log(`data is ${JSON.stringify(reqbody)}`);
    assert(req.param('foo_undefined') === undefined);
    if(req.query !== undefined) {
        console.log(`req.query ${JSON.stringify(req.query)}`);
        if(req.query.q1 !== undefined) {
            reqbody['q1'] = req.query.q1;
        }
        if(req.query.q2 !== undefined) {
            reqbody['q2'] = req.query.q2;
        }
    }
    rsp.json(reqbody);
    rsp.end();
}

async function fjson(req, rsp) {
    let json = req.body();

    if('delayms' in json) {
        let ms = parseInt(json['delayms']);
        setTimeout(processJson, ms, req, rsp);
    } else {
        processJson(req, rsp);
    }
}

app.use(bodyParser.raw({type: 'application/octet-stream'}));
app.post('/proto', fproto);

// placement specific because not all calls are json
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.post('/json', fjson);

app.use((req,res) => {
    res.statusCode = 400;
    res.send('error: request handler not recognized\n');
    res.end();
});

app.listen(PORT, () => console.log(`started app on port ${PORT}`));
