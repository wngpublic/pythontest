let express = require('express');
let app = express();
let bodyParser = require('body-parser');

function postJson(req,rsp) {
    console.log(`postJson ${JSON.stringify(req.body)}`);
    let data = req.body;
    if(req.params.id1 !== undefined) {  // or req.param('id1')
        data['id1'] = req.params.id1;
    }
    if(req.params.id2 !== undefined) {
        data['id2'] = req.params.id2;
    }
    if(req.query !== undefined) {
        console.log(`req.query ${JSON.stringify(req.query)}`);
        if(req.query.q1 !== undefined) {
            data['q1'] = req.query.q1;
        }
        if(req.query.q2 !== undefined) {
            data['q2'] = req.query.q2;
        }
    }
    rsp.json(data);
    rsp.end();
}
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.post('/postjson/:id1/:id2',postJson);
app.post('/postjson',postJson);
app.get('/',(req,rsp) => rsp.send('hello world'));
app.use((req,rsp) => {
    rsp.statusCode = 400;
    rsp.send('error: request handler not recognized\n');
    rsp.end();
});

let fs = require('fs');
let privateKey = fs.readFileSync('../softlinkssh/keydecrypted.pem');
let certificate = fs.readFileSync('../softlinkssh/cert.pem');
let credentials = {key:privateKey, cert: certificate};
let http = require('http');
let https = require('https');
let httpServer = http.createServer(app);
let httpsServer = https.createServer(credentials, app);
httpServer.listen(8080);
httpsServer.listen(8443);