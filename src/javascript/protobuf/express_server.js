const express = require('express');
const protobuf = require('protobufjs');
const builder = protobuf.loadProtoFile('./protobuf_lib/testpayloads.proto');
const requestMessage = builder.build('Request');
const responseMessage = builder.build('Response');

// @ dec 2020: does not currently work

async function fproto(req, res) {
    // curl -X POST 'localhost:3000/postjson1/v1/v2' -d '{ "k1":"v1" }' -H 'Content-Type: application/json'
    const reqMsg = requestMessage.decode(req.raw);

    const rspMsg = new responseMessage();
    // headers: {'Content-Type': 'application/octet-stream'}

    res.end();
}


const app = express();
const PORT = 3000;

app.post('/proto', fproto);
app.use((req,res) => {
    res.statusCode = 400;
    res.send('error: request handler not recognized\n');
    res.end();
});

app.listen(PORT, () => console.log(`started app on port ${PORT}`));
